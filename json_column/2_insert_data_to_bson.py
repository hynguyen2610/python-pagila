import sys
from pathlib import Path
import json
from faker import Faker

project_root = Path(__file__).resolve().parent.parent  # Moves two levels up from the current file (json_column directory)
sys.path.append(str(project_root))

from db_connection import create_connection

#################################################################

# Initialize the Faker instance
fake = Faker()

# Create a connection to the PostgreSQL database
def get_db_connection():
    return create_connection()

# Generate random optional data (phoneNumber and email)
def generate_optional_data():
    return {
        "phoneNumber": fake.phone_number() if fake.boolean() else None,  # Randomly include phone number
        "email": fake.email() if fake.boolean() else None  # Randomly include email
    }

# Update the profile for the first 10,000 actors
def update_first_10k_actors():
    # Create a new connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the first 10,000 actors (or fewer if there are less than 10,000)
    cursor.execute("SELECT actor_id, profile FROM actor ORDER BY actor_id LIMIT 10000;")
    actors = cursor.fetchall()

    total_updated = 0
    with_optional_data = 0
    without_optional_data = 0

    # Loop through each actor and update the profile column
    for actor in actors:
        actor_id, current_profile = actor
        if current_profile is None:
            current_profile = {}
        new_optional_data = generate_optional_data()

        # Merge the existing profile with new optional data
        updated_profile = {**current_profile, **new_optional_data}

        # Update the profile for the actor
        update_sql = """
        UPDATE actor
        SET profile = %s
        WHERE actor_id = %s;
        """
        cursor.execute(update_sql, (json.dumps(updated_profile), actor_id))
        conn.commit()

        # Update counters for the report
        total_updated += 1
        if new_optional_data["phoneNumber"] or new_optional_data["email"]:
            with_optional_data += 1
        else:
            without_optional_data += 1

    print(f"Processed {total_updated} records: {with_optional_data} with optional data, {without_optional_data} without.")
    cursor.close()
    conn.close()

# Run the update for the first 10,000 records
update_first_10k_actors()
