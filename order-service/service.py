from decimal import Decimal

from mysql.connector.errors import Error as MySQLError

from db import DatabaseConnectionError, get_connection, get_dict_cursor
from schemas import OrderItemResponse, OrderResponse


class ServiceError(Exception):
    """Base application error with an associated HTTP status code."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def _fetch_order_items(cursor, order_id: int) -> list[OrderItemResponse]:
    cursor.execute(
        """
        SELECT product_id, quantity, unit_price
        FROM order_items
        WHERE order_id = %s
        ORDER BY order_item_id
        """,
        (order_id,),
    )
    rows = cursor.fetchall()
    return [OrderItemResponse(**row) for row in rows]


def place_order(customer_id: int) -> OrderResponse:
    try:
        connection = get_connection()
    except DatabaseConnectionError as exc:
        raise ServiceError(status_code=500, detail=str(exc)) from exc

    cursor = get_dict_cursor(connection)

    try:
        cursor.execute(
            "SELECT customer_id FROM customers WHERE customer_id = %s",
            (customer_id,),
        )
        customer = cursor.fetchone()
        if not customer:
            raise ServiceError(status_code=404, detail="customer not found")

        cursor.execute(
            """
            SELECT cart_id, customer_id, status, created_at, updated_at
            FROM cart
            WHERE customer_id = %s AND status = 'ACTIVE'
            ORDER BY updated_at DESC, created_at DESC
            LIMIT 1
            """,
            (customer_id,),
        )
        cart = cursor.fetchone()
        if not cart:
            raise ServiceError(status_code=404, detail="active cart not found")

        cursor.execute(
            """
            SELECT cart_item_id, cart_id, product_id, quantity, unit_price
            FROM cart_items
            WHERE cart_id = %s
            ORDER BY cart_item_id
            """,
            (cart["cart_id"],),
        )
        cart_items = cursor.fetchall()
        if not cart_items:
            raise ServiceError(status_code=400, detail="empty cart")

        total_amount = Decimal("0")

        connection.start_transaction()

        validated_items: list[dict] = []
        for item in cart_items:
            # Lock the product row so stock checks and updates stay consistent.
            cursor.execute(
                """
                SELECT product_id, stock_quantity
                FROM products
                WHERE product_id = %s
                FOR UPDATE
                """,
                (item["product_id"],),
            )
            product = cursor.fetchone()
            if not product or product["stock_quantity"] < item["quantity"]:
                raise ServiceError(status_code=400, detail="out of stock")

            line_total = Decimal(str(item["unit_price"])) * item["quantity"]
            total_amount += line_total
            validated_items.append(item)

        cursor.execute(
            """
            INSERT INTO orders (customer_id, order_status, total_amount, created_at)
            VALUES (%s, 'CONFIRMED', %s, NOW())
            """,
            (customer_id, total_amount),
        )
        order_id = cursor.lastrowid

        for item in validated_items:
            cursor.execute(
                """
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    order_id,
                    item["product_id"],
                    item["quantity"],
                    item["unit_price"],
                ),
            )
            cursor.execute(
                """
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE product_id = %s
                """,
                (item["quantity"], item["product_id"]),
            )

        cursor.execute(
            """
            UPDATE cart
            SET status = 'CHECKED_OUT', updated_at = NOW()
            WHERE cart_id = %s
            """,
            (cart["cart_id"],),
        )

        connection.commit()

        cursor.execute(
            """
            SELECT order_id, customer_id, order_status, total_amount, created_at
            FROM orders
            WHERE order_id = %s
            """,
            (order_id,),
        )
        order_row = cursor.fetchone()

        return OrderResponse(
            **order_row,
            items=_fetch_order_items(cursor, order_id),
        )
    except ServiceError:
        if connection.in_transaction:
            connection.rollback()
        raise
    except MySQLError as exc:
        if connection.in_transaction:
            connection.rollback()
        raise ServiceError(status_code=500, detail="database operation failed") from exc
    finally:
        cursor.close()
        connection.close()


def get_order_details(order_id: int) -> OrderResponse:
    try:
        connection = get_connection()
    except DatabaseConnectionError as exc:
        raise ServiceError(status_code=500, detail=str(exc)) from exc

    cursor = get_dict_cursor(connection)

    try:
        cursor.execute(
            """
            SELECT order_id, customer_id, order_status, total_amount, created_at
            FROM orders
            WHERE order_id = %s
            """,
            (order_id,),
        )
        order_row = cursor.fetchone()
        if not order_row:
            raise ServiceError(status_code=404, detail="order not found")

        return OrderResponse(
            **order_row,
            items=_fetch_order_items(cursor, order_id),
        )
    except MySQLError as exc:
        raise ServiceError(status_code=500, detail="database operation failed") from exc
    finally:
        cursor.close()
        connection.close()
