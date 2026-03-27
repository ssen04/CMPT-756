# Experiment Run Commands

## k6 Test Commands for cart-service

### 1. GET test

`Customer 1` was selected for the `GET /cart/{customer_id}` tests because this customer already has an active cart with existing items in the seed data, making it appropriate for consistent read-latency measurements.

#### VM
```bash
k6 run -e BASE_URL=http://136.109.180.133:8002 -e CUSTOMER_ID=1 k6/cart-service/cart-get-test.js
```

#### Cloud Run
```bash
k6 run -e BASE_URL=https://cart-service-1009382473191.us-west1.run.app -e CUSTOMER_ID=1 k6/cart-service/cart-get-test.js
```

#### Cloud Function
```bash
k6 run -e BASE_URL=https://us-west1-cmpt756-project-489717.cloudfunctions.net/cart-service-function -e CUSTOMER_ID=1 k6/cart-service/cart-get-test.js
```

### 2. POST test

`Customer 4` and `Product 1` were selected for the `POST /cart` tests because they represent a valid customer-product combination with sufficient stock, allowing stable and repeatable write-latency measurements without causing invalid-request errors.

#### VM
```bash
k6 run -e BASE_URL=http://136.109.180.133:8002 -e CUSTOMER_ID=4 -e PRODUCT_ID=1 -e QUANTITY=1 k6/cart-service/cart-post-test.js
```

#### Cloud Run
```bash
k6 run -e BASE_URL=https://cart-service-1009382473191.us-west1.run.app -e CUSTOMER_ID=4 -e PRODUCT_ID=1 -e QUANTITY=1 k6/cart-service/cart-post-test.js
```

#### Cloud Function
```bash
k6 run -e BASE_URL=https://us-west1-cmpt756-project-489717.cloudfunctions.net/cart-service-function -e CUSTOMER_ID=4 -e PRODUCT_ID=1 -e QUANTITY=1 k6/cart-service/cart-post-test.js
```

## Seed Data Reference

- Valid customers: `1`, `2`, `3`, `4`, `5`
- Valid products: `1`, `2`, `3`, `4`, `5`, `6`
- Customers with ACTIVE carts: `1`, `2`, `4`
- Customer `3` has `CHECKED_OUT` cart
- Customer `5` has `ABANDONED` cart
- Recommended GET test customer: `1`
- Recommended POST test customer: `4`
- Recommended POST test product: `1`

## Recommended Load Levels

- Low: `5` VUs for `30s`
- Medium: `10` VUs for `30s`
- High: `30` VUs for `30s`

## Suggested Reporting Metrics

- Average latency
- Median latency
- p95 latency
- p99 latency
- Requests per second
- Failed requests
- Error rate
