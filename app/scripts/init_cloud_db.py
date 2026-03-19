import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("Conectando a Aiven...")
try:
    with open('app/sql/acapulco_database.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()

    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mysql-acapulcoapi-castroluisd007-2d85.d.aivencloud.com'),
        port=int(os.getenv('DB_PORT', '19598')),
        user=os.getenv('DB_USER', 'avnadmin'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'defaultdb')
    )

    cursor = conn.cursor()

    # Split statements to execute them one by one
    statements = sql_script.split(';')
    for statement in statements:
        if statement.strip():
            print(f"Ejecutando: {statement.strip()[:60]}...")
            cursor.execute(statement)
            # Fetch results if any so we don't get "Commands out of sync"
            try:
                cursor.fetchall()
            except mysql.connector.errors.InterfaceError:
                pass # No results to fetch

    conn.commit()
    cursor.close()
    conn.close()
    print("¡Base de datos inicializada exitosamente!")
    
except Exception as e:
    print(f"Ha ocurrido un error: {e}")
