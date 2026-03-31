from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/products")
def get_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            product_id, name, description, category,
            CAST(price AS DECIMAL(10,2)) AS price,
            stock_quantity,
            created_at
        FROM products
    """)
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return products


@router.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            product_id, name, description, category,
            CAST(price AS DECIMAL(10,2)) AS price,
            stock_quantity,
            created_at
        FROM products
        WHERE product_id = %s
    """, (product_id,))

    product = cursor.fetchone()

    cursor.close()
    conn.close()

    if not product:
        return {"detail": "Product not found"}

    return product