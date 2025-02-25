import psycopg2
from psycopg2 import OperationalError

# Function to create and return the database connection
def create_connection():
    try:
        # Update these values with your actual PostgreSQL connection details
        conn = psycopg2.connect(
            dbname="pagila",    # Database name
            user="postgres",               # Your PostgreSQL username
            password="123456",       # Your PostgreSQL password
            host="localhost",               # Host, usually localhost
            port="5432"                     # PostgreSQL default port
        )
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None
