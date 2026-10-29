import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

try:
    with psycopg.connect(database_url, connect_timeout=10) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user;")
            print("Connection successful. Current database and user:", cursor.fetchone())

except psycopg.OperationalError as error:
    print("Connection failed:", error)