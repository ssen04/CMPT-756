from fastapi import FastAPI, HTTPException

from app import (
    AddToCartResponse,
    CartItemRequest,
    CartResponse,
    ErrorResponse,
    ServiceError,
    add_item_to_cart,
    get_cart_items,
)

# FastAPI entry point for VM and container deployments.
app = FastAPI(
    title="Add To Cart Service",
    description="Microservice for adding products to an active cart and retrieving cart contents.",
    version="1.0.0",
)


@app.get(
    "/",
    tags=["Health"],
    summary="Health check",
)
def health_check():
    # Simple endpoint to verify the service is up.
    return {"message": "Add To Cart Service is running"}


@app.post(
    "/cart",
    tags=["Cart"],
    summary="Add item to cart",
    description="Creates an ACTIVE cart if needed, then inserts or updates the requested product in that cart.",
    response_model=AddToCartResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid quantity or insufficient stock"},
        404: {"model": ErrorResponse, "description": "Customer or product not found"},
        422: {"description": "Validation error"},
    },
)
def add_item(payload: CartItemRequest):
    # Convert service errors into HTTP responses.
    try:
        return add_item_to_cart(payload.model_dump())
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@app.get(
    "/cart/{customer_id}",
    tags=["Cart"],
    summary="Get cart items",
    description="Returns the current ACTIVE cart and all items for the given customer.",
    response_model=CartResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Customer not found"},
    },
)
def get_cart(customer_id: int):
    # Convert service errors into HTTP responses.
    try:
        return get_cart_items(customer_id)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
