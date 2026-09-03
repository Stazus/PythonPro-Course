import os
import time

import psycopg2


db_host = os.getenv("DB_HOST", "database")
db_name = os.getenv("DB_NAME", "appdb")
db_user = os.getenv("DB_USER", "appuser")
db_password = os.getenv("DB_PASSWORD", "apppassword")

for attempt in range(10):
    try:
        connection = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )
        print("Połączono z bazą PostgreSQL!")
        connection.close()
        break
    except psycopg2.OperationalError:
        print("Baza jeszcze nie jest gotowa, ponawiam próbę...")
        time.sleep(2)
else:
    print("Nie udało się połączyć z bazą.")
