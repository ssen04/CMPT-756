import os
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "34.186.155.72")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Canada@2021")
DB_NAME = os.environ.get("DB_NAME", "ecomm_db")

@app.route("/", methods=["GET"])
def catalog():
    try:
        # Conectar a MySQL
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products LIMIT 5;")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(items)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)