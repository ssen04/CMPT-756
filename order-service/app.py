from fastapi import FastAPI, HTTPException

from handlers import create_order_for_customer, get_order_by_id
from schemas import ErrorResponse, OrderResponse, PlaceOrderRequest
from service import ServiceError


app = FastAPI(title="Order Service", version="1.0.0")


@app.post(
    "/order",
    response_model=OrderResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def create_order(payload: PlaceOrderRequest) -> OrderResponse:
    try:
        return create_order_for_customer(payload.customer_id)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@app.get(
    "/order/{order_id}",
    response_model=OrderResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def read_order(order_id: int) -> OrderResponse:
    try:
        return get_order_by_id(order_id)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
