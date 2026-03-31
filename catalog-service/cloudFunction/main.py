import os
import mysql.connector
from flask import jsonify

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
    )

def catalog_function_serverless(request):
    path = (request.path or "").rstrip("/")
    if not path:
        path = "/"

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method != "GET":
            return jsonify({"error": "Only GET allowed"}), 405

        if path == "/products":
            cursor.execute("SELECT * FROM products")
            return jsonify(cursor.fetchall()), 200

        if path.startswith("/products/"):
            product_id = int(path.rsplit("/", 1)[-1])
            cursor.execute(
                "SELECT * FROM products WHERE product_id=%s",
                (product_id,)
            )
            product = cursor.fetchone()

            if not product:
                return jsonify({"error": "Not found"}), 404

            return jsonify(product), 200

        return jsonify({"message": "Catalog running"}), 200

    except Exception as e:
        # súper importante para debug en GCP
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass