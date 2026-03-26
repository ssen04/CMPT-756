from schemas import OrderResponse
from service import get_order_details, place_order


def get_root_payload() -> dict[str, str]:
    return {"message": "order-service is running"}


def create_order_for_customer(customer_id: int) -> OrderResponse:
    return place_order(customer_id)


def get_order_by_id(order_id: int) -> OrderResponse:
    return get_order_details(order_id)
