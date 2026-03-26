import os
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()  # carga variables de entorno desde .env

# Crear pool global
db_pool = pooling.MySQLConnectionPool(
    pool_name="catalog_pool",
    pool_size=5,
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 3306)),
    auth_plugin='mysql_native_password'
)

# Función que obtiene una conexión del pool
def get_connection():
    return db_pool.get_connection()