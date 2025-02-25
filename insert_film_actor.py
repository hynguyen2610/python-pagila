import random

# Import the connection function
from db_connection import create_connection

# Function to populate the film_actor table with random film-actor pairings
def insert_film_actor(num_pairings):
    conn = create_connection()
    
    if conn is not None:
        try:
            # Create a cursor object to interact with the database
            cur = conn.cursor()

            # Query to get all actor_ids and film_ids
            cur.execute("SELECT actor_id FROM actor;")
            actor_ids = [row[0] for row in cur.fetchall()]

            cur.execute("SELECT film_id FROM film;")
            film_ids = [row[0] for row in cur.fetchall()]

            # Prepare the insert query with ON CONFLICT to skip duplicate pairings
            insert_query = """
                INSERT INTO film_actor (actor_id, film_id) 
                VALUES (%s, %s)
                ON CONFLICT (actor_id, film_id) DO NOTHING;
            """
            
            # Generate random pairings between actors and films
            pairings = [
                (random.choice(actor_ids), random.choice(film_ids)) for _ in range(num_pairings)
            ]

            # Insert the pairings in batches for better performance
            cur.executemany(insert_query, pairings)

            # Commit the transaction
            conn.commit()
            print(f"Successfully inserted {num_pairings} film-actor pairings (duplicates skipped).")

            # Close the cursor
            cur.close()
        except Exception as e:
            print(f"Error inserting film-actor pairings: {e}")
        finally:
            # Close the connection
            conn.close()
    else:
        print("Failed to connect to the database.")

# Insert 100,000 film-actor pairings (adjust as needed)
insert_film_actor(100000)
