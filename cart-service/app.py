from decimal import Decimal

import mysql.connector
from pydantic import BaseModel, ConfigDict, Field


class ServiceError(Exception):
    # Reusable service-level error for HTTP handlers.
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class CartItemRequest(BaseModel):
    # Request body for adding an item to a cart.
    customer_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_id": 1,
                "product_id": 101,
                "quantity": 2,
            }
        }
    )
class AddToCartResponse(BaseModel):
    # Success response for POST /cart.
    message: str
    cart_id: int
    customer_id: int
    product_id: int
    quantity: int
    unit_price: float


class CartLineItemResponse(BaseModel):
    # Single item returned in cart details.
    cart_item_id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    line_total: float


class CartResponse(BaseModel):
    # Response body for GET /cart/{customer_id}.
    customer_id: int
    cart_id: int | None
    items: list[CartLineItemResponse]
    total_amount: float
class ErrorResponse(BaseModel):
    # Standard error payload for API documentation.
    detail: str
# Shared MySQL connection used by the cart service.
db = mysql.connector.connect(
    host="34.186.155.72",
    user="test",
    password="Canada@2021",
    database="ecomm_db",
)
cursor = db.cursor(dictionary=True)


def get_customer(customer_id: int):
    # Load the customer to validate the request.
    cursor.execute(
        "SELECT customer_id, full_name, email FROM customers WHERE customer_id = %s",
        (customer_id,),
    )
    return cursor.fetchone()


def get_product(product_id: int):
    # Load the product to validate price and stock.
    cursor.execute(
        """
        SELECT product_id, name, price, stock_quantity
        FROM products
        WHERE product_id = %s
        """,
        (product_id,),
    )
    return cursor.fetchone()


def get_active_cart(customer_id: int):
    # Find the most recent active cart for the customer.
    cursor.execute(
        """
        SELECT cart_id, status
        FROM cart
        WHERE customer_id = %s AND status = 'ACTIVE'
        ORDER BY updated_at DESC, cart_id DESC
        LIMIT 1
        """,
        (customer_id,),
    )
    return cursor.fetchone()


def get_or_create_active_cart(customer_id: int):
    # Reuse the active cart or create a new one.
    cart = get_active_cart(customer_id)
    if cart:
        return cart

    cursor.execute(
        """
        INSERT INTO cart (customer_id, status, created_at, updated_at)
        VALUES (%s, 'ACTIVE', NOW(), NOW())
        """,
        (customer_id,),
    )
    db.commit()
    return {"cart_id": cursor.lastrowid, "status": "ACTIVE"}


def add_item_to_cart(payload: dict):
    # Add a new product or increase quantity for an existing cart item.
    item = CartItemRequest(**payload)

    customer = get_customer(item.customer_id)
    if not customer:
        raise ServiceError(404, "Customer not found")

    product = get_product(item.product_id)
    if not product:
        raise ServiceError(404, "Product not found")

    if product["stock_quantity"] < item.quantity:
        raise ServiceError(400, "Insufficient stock")

    cart = get_or_create_active_cart(item.customer_id)

    cursor.execute(
        """
        SELECT cart_item_id, quantity
        FROM cart_items
        WHERE cart_id = %s AND product_id = %s
        """,
        (cart["cart_id"], item.product_id),
    )
    existing_item = cursor.fetchone()

    new_quantity = item.quantity
    if existing_item:
        new_quantity += existing_item["quantity"]
        if product["stock_quantity"] < new_quantity:
            raise ServiceError(400, "Requested quantity exceeds available stock")

        cursor.execute(
            """
            UPDATE cart_items
            SET quantity = %s, unit_price = %s
            WHERE cart_item_id = %s
            """,
            (new_quantity, product["price"], existing_item["cart_item_id"]),
        )
    else:
        cursor.execute(
            """
            INSERT INTO cart_items (cart_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            """,
            (cart["cart_id"], item.product_id, item.quantity, product["price"]),
        )

    cursor.execute(
        "UPDATE cart SET updated_at = NOW() WHERE cart_id = %s",
        (cart["cart_id"],),
    )
    db.commit()

    return {
        "message": "Item added to cart successfully",
        "cart_id": cart["cart_id"],
        "customer_id": item.customer_id,
        "product_id": item.product_id,
        "quantity": new_quantity,
        "unit_price": float(product["price"]),
    }


def get_cart_items(customer_id: int):
    # Return the active cart with item details and total amount.
    customer = get_customer(customer_id)
    if not customer:
        raise ServiceError(404, "Customer not found")

    cart = get_active_cart(customer_id)
    if not cart:
        return {
            "customer_id": customer_id,
            "cart_id": None,
            "items": [],
            "total_amount": 0.0,
        }

    cursor.execute(
        """
        SELECT
            ci.cart_item_id,
            ci.product_id,
            p.name AS product_name,
            ci.quantity,
            ci.unit_price,
            (ci.quantity * ci.unit_price) AS line_total
        FROM cart_items ci
        JOIN products p ON p.product_id = ci.product_id
        WHERE ci.cart_id = %s
        ORDER BY ci.cart_item_id
        """,
        (cart["cart_id"],),
    )
    items = cursor.fetchall()

    total_amount = sum(
        (
            row["line_total"]
            if isinstance(row["line_total"], Decimal)
            else Decimal(str(row["line_total"]))
        )
        for row in items
    )

    normalized_items = [
        {
            "cart_item_id": row["cart_item_id"],
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "quantity": row["quantity"],
            "unit_price": float(row["unit_price"]),
            "line_total": float(row["line_total"]),
        }
        for row in items
    ]

    return {
        "customer_id": customer_id,
        "cart_id": cart["cart_id"],
        "items": normalized_items,
        "total_amount": float(total_amount),
    }
