from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from datetime import datetime

app = FastAPI()

class NotificationRequest(BaseModel):
    order_id: int

def get_db_connection():

    return mysql.connector.connect(
        host="34.186.155.72",
        user="test",
        password="Canada@2021",
        database="ecomm_db",
        port = 3306
    )

@app.post("/notify")
def notify_customer(request: NotificationRequest):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id
        FROM orders
        WHERE order_id = %s
    """, (request.order_id,))

    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Order not found")

    customer_id = result[0]

    cursor.execute("""
        SELECT full_name, email
        FROM customers
        WHERE customer_id = %s
    """, (customer_id,))

    customer = cursor.fetchone()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    full_name, email = customer

    cursor.execute("""
        SELECT p.name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
    """, (request.order_id,))

    products = [row[0] for row in cursor.fetchall()]

    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    message = f"Hello {full_name}, your order for {', '.join(products)} has been confirmed."

    cursor.execute("""
        INSERT INTO notifications
        (order_id, customer_id, message, status, sent_at)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        request.order_id,
        customer_id,
        message,
        "SENT",
        datetime.now()
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "order_id": request.order_id,
        "customer": full_name,
        "products": products,
        "status": "SENT"
    }

@app.get("/health")
def health():
    return {"status": "running"}