from flask import jsonify
from pydantic import ValidationError

from handlers import create_order_for_customer, get_order_by_id, get_root_payload
from service import ServiceError


def order_service(request):
    """Cloud Functions HTTP entry point."""
    path = (request.path or "").rstrip("/")
    if not path:
        path = "/"

    try:
        if request.method == "GET" and path == "/":
            return jsonify(get_root_payload()), 200

        if request.method == "POST" and path.endswith("/order"):
            payload = request.get_json(silent=True) or {}
            customer_id = int(payload["customer_id"])
            return jsonify(create_order_for_customer(customer_id).model_dump(mode="json")), 200

        if request.method == "GET" and "/order/" in path:
            order_id = int(path.rsplit("/", 1)[-1])
            return jsonify(get_order_by_id(order_id).model_dump(mode="json")), 200

        return jsonify({"detail": "Route not found"}), 404
    except KeyError:
        return jsonify({"detail": "customer_id is required"}), 400
    except ValidationError as exc:
        return jsonify({"detail": exc.errors()}), 422
    except ValueError:
        return jsonify({"detail": "Invalid numeric value"}), 400
    except ServiceError as exc:
        return jsonify({"detail": exc.detail}), exc.status_code
