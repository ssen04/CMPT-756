from app import app
from function_main import order_service
from handlers import get_root_payload


@app.get("/")
def root():
    return get_root_payload()
