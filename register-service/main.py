from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
import hashlib

app = FastAPI(title="Register Customer Service")

# Hardcoded database connection
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",         # your DB host
        user="test",              # your DB username
        password="Canada@2021",   # your DB password
        database="ecomm_db"       # your database name
    )

class Customer(BaseModel):
    full_name: str
    email: str
    password: str

@app.get("/")
def home():
    return {"message": "Register Service Running"}

@app.post("/register")
def register_customer(customer: Customer):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers WHERE email=%s", (customer.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = hashlib.sha256(customer.password.encode()).hexdigest()

    cursor.execute(
        "INSERT INTO customers (full_name, email, password_hash) VALUES (%s, %s, %s)",
        (customer.full_name, customer.email, password_hash)
    )
    db.commit()

    cursor.execute("SELECT customer_id FROM customers WHERE email=%s", (customer.email,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    return {
        "message": "Customer registered successfully",
        "customer_id": user["customer_id"],
        "email": customer.email
    }
