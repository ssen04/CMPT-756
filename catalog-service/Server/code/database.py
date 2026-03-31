import os
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()  # carga variables de entorno desde .env

# Crear pool global
db_pool = pooling.MySQLConnectionPool(
    pool_name="catalog_pool",
    pool_size=5,
    host=os.getenv("34.186.155.72"),
    user=os.getenv("test"),
    password=os.getenv("Canada@2021"),
    database=os.getenv("ecomm_db"),
    port=int(os.getenv("DB_PORT", 3306)),
    auth_plugin='mysql_native_password'
)

# Función que obtiene una conexión del pool
def get_connection():
    return db_pool.get_connection()