from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel

app = FastAPI(title="Register Customer Service")

# Database connection
db = mysql.connector.connect(
    host="34.186.155.72",
    user="root",
    password="Canada@2021",
    database="ecomm_db"
)
cursor = db.cursor(dictionary=True)


# Pydantic model for request
class Customer(BaseModel):
    name: str
    email: str
    password: str


@app.post("/register")
def register_customer(customer: Customer):
    # Check if email exists
    cursor.execute("SELECT * FROM customers WHERE email=%s", (customer.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert new customer
    cursor.execute(
        "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)",
        (customer.name, customer.email, customer.password)
    )
    db.commit()
    return {"message": "Customer registered successfully", "email": customer.email}