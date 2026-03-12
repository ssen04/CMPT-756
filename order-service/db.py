import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict
from mysql.connector.errors import Error as MySQLError

from config import settings


class DatabaseConnectionError(Exception):
    """Raised when the application cannot connect to MySQL."""


def get_connection() -> MySQLConnection:
    """Create a new MySQL connection for each request."""
    try:
        connection = mysql.connector.connect(
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
        )
        # Keep simple read queries outside an explicit transaction.
        connection.autocommit = True
        return connection
    except MySQLError as exc:
        raise DatabaseConnectionError("Unable to connect to the database.") from exc


def get_dict_cursor(connection: MySQLConnection) -> MySQLCursorDict:
    """Return a dictionary cursor for readable query results."""
    return connection.cursor(dictionary=True)
