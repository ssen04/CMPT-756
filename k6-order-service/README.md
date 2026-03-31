## Dataset Preparation Note – Order Service Testing

To ensure valid preconditions for order placement during performance testing, a test product and corresponding customer carts were created.

### Test Data Setup

- A test product (`product_id = 102`) was introduced for controlled testing.

- For customer IDs **102 to 3147 (~3046 records)**:
  - An **ACTIVE cart** was created for each customer
  - Each cart was populated with exactly **one cart item**:
    - `product_id = 102`
    - `quantity = 1`
    - `unit_price = 9.99`

### Purpose

This setup guarantees that all test requests satisfy the required business condition — each customer has an active cart with items — thereby preventing application-level failures such as:

> "active cart not found"

during load testing.
