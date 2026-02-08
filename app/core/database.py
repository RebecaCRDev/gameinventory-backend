import mysql.connector
from mysql.connector import Error
from app.core.config import settings


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT,
            charset='utf8mb4'
        )
        return connection
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        raise


def get_cursor(dictionary=True):
    conn = get_connection()
    return conn.cursor(dictionary=dictionary), conn
