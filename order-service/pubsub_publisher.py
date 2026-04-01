from google.cloud import pubsub_v1
import json
import os

PROJECT_ID = (
    os.getenv("GOOGLE_CLOUD_PROJECT")
    or os.getenv("GCP_PROJECT")
    or "cmpt756-project-489717"
)
TOPIC_ID = "order-created-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def publish_order_created_event(order):
    event = {
        "event_type": "order_created",
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "total_amount": float(order.total_amount),
        "status": order.order_status,
    }

    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data)

    print(f"[PUBSUB] Published event: {event}")

    return future.result()
