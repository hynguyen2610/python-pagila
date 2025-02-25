from db_connection import create_connection

# Create a connection to the PostgreSQL database
conn = create_connection()

if conn is not None:
    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Execute a query to fetch all data from the 'actor' table
    cur.execute("SELECT * FROM actor;")

    # Fetch all rows from the result of the query
    rows = cur.fetchall()

    # Print the column names
    column_names = [desc[0] for desc in cur.description]
    print("Column Names:", column_names)

    # Print all the rows
    for row in rows:
        print(row)

    # Close the cursor and connection
    cur.close()
    conn.close()
else:
    print("Failed to connect to the database.")
