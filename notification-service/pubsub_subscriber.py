from google.cloud import pubsub_v1
import json
import os

PROJECT_ID = (
    os.getenv("GOOGLE_CLOUD_PROJECT")
    or os.getenv("GCP_PROJECT")
    or "cmpt756-project-489717"
)
SUBSCRIPTION_ID = "notification-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)


def callback(message):
    data = json.loads(message.data.decode("utf-8"))

    print(f"[PUBSUB] Received: {data}")

    if data.get("event_type") == "order_created":
        handle_order_created(data)

    message.ack()


def handle_order_created(event):
    order_id = event["order_id"]
    customer_id = event["customer_id"]

    print(f"[NOTIFICATION] Processing order {order_id}")

    # Reuse the existing notification creation path.
    from main import NotificationRequest, notify_customer

    notify_customer(NotificationRequest(order_id=order_id))


def start_subscriber():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    print(f"Listening on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
