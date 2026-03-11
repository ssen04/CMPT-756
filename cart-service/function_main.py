from flask import jsonify
from pydantic import ValidationError

from app import ServiceError, add_item_to_cart, get_cart_items


def cart_service(request):
    # Cloud Functions HTTP entry point.
    path = (request.path or "").rstrip("/")
    if not path:
        path = "/"

    try:
        if request.method == "POST" and path.endswith("/cart"):
            # Handle add-to-cart requests.
            payload = request.get_json(silent=True) or {}
            return jsonify(add_item_to_cart(payload)), 200

        if request.method == "GET" and "/cart/" in path:
            # Handle cart lookup requests.
            customer_id = int(path.rsplit("/", 1)[-1])
            return jsonify(get_cart_items(customer_id)), 200

        return jsonify({"detail": "Route not found"}), 404
    except ValidationError as exc:
        return jsonify({"detail": exc.errors()}), 422
    except ValueError:
        return jsonify({"detail": "Invalid customer_id"}), 400
    except ServiceError as exc:
        return jsonify({"detail": exc.detail}), exc.status_code
