from src.db_connect import get_connection

def main():
    # Open DB-connection
    conn = get_connection()
    if conn is None:
        print("Exiting program...")
        return


    # Close DB-connection
    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
