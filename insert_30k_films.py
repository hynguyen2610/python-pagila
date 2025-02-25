import psycopg2
from faker import Faker
import random

# Import the connection function
from db_connection import create_connection

# Create an instance of Faker
fake = Faker()

# Function to insert 30,000 fake films into the film table
def insert_films(num_films):
    conn = create_connection()
    
    if conn is not None:
        try:
            # Create a cursor object to interact with the database
            cur = conn.cursor()

            # Prepare the insert query
            insert_query = """
                INSERT INTO film (title, description, release_year, language_id) 
                VALUES (%s, %s, %s, %s)
            """
            
            # Generate 30,000 fake films
            films = [
                (
                    fake.catch_phrase(),  # Title
                    fake.text(max_nb_chars=200),  # Description
                    random.randint(2000, 2025),  # Release Year (random between 2000 and 2025)
                    random.randint(1, 5)  # Language ID (random between 1 and 5; adjust based on your language table)
                ) for _ in range(num_films)
            ]

            # Insert films in batches for better performance
            cur.executemany(insert_query, films)

            # Commit the transaction
            conn.commit()
            print(f"Successfully inserted {num_films} films.")

            # Close the cursor
            cur.close()
        except Exception as e:
            print(f"Error inserting films: {e}")
        finally:
            # Close the connection
            conn.close()
    else:
        print("Failed to connect to the database.")

# Insert 30,000 films
insert_films(30000)
