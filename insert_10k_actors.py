from faker import Faker

# Import the connection function
from db_connection import create_connection

# Create an instance of Faker
fake = Faker()

# Function to insert 10,000 fake actors into the actor table
def insert_actors(num_actors):
    conn = create_connection()
    
    if conn is not None:
        try:
            # Create a cursor object to interact with the database
            cur = conn.cursor()

            # Prepare the insert query
            insert_query = "INSERT INTO actor (first_name, last_name) VALUES (%s, %s)"
            
            # Generate 10,000 fake actors
            actors = [(fake.first_name(), fake.last_name()) for _ in range(num_actors)]

            # Insert actors in batches for better performance
            cur.executemany(insert_query, actors)

            # Commit the transaction
            conn.commit()
            print(f"Successfully inserted {num_actors} actors.")

            # Close the cursor
            cur.close()
        except Exception as e:
            print(f"Error inserting actors: {e}")
        finally:
            # Close the connection
            conn.close()
    else:
        print("Failed to connect to the database.")

# Insert 10,000 actors
insert_actors(10000)
