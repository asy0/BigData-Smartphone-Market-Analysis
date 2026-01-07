import psycopg2
from dotenv import load_dotenv
import os

# Load .env on import
load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("PGHOST"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            database=os.getenv("PGDATABASE"),
            port=os.getenv("PGPORT"),
            sslmode="require"
        )
    except psycopg2.OperationalError as e:
        print("ERROR: Could not connect to the database!")
        print("Reason:", e)
        return None
    except Exception as e:
        print("ERROR: Unexpected error during connection:")
        print(e)
        return None

    # Run test query
    try:
        cur = conn.cursor()
        cur.execute("SELECT current_database(), current_user, NOW();")
        result = cur.fetchone()

        print("SUCCESS: Connection successful!")
        print("Database:", result[0])
        print("User:", result[1])
        print("Server time:", result[2], "\n")

        cur.close()
    except Exception as e:
        print("ERROR: Connected, but failed test query:")
        print(e)
        conn.close()
        return None

    return conn
