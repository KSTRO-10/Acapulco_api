import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "12345"),
        database=os.getenv("DB_NAME", "acapulco_api")
    )

    return conn