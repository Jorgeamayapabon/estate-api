import os
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from dotenv import load_dotenv

load_dotenv()

_pool: MySQLConnectionPool | None = None


def _get_pool() -> MySQLConnectionPool:
    global _pool
    if _pool is None:
        _pool = MySQLConnectionPool(
            pool_name="habi_pool",
            pool_size=5,
            host=os.environ["DB_HOST"],
            port=int(os.environ.get("DB_PORT", 3306)),
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )
    return _pool


def get_connection() -> mysql.connector.MySQLConnection:
    """Return a connection from the pool. Caller must close it after use."""
    return _get_pool().get_connection()
