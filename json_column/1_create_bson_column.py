import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent  # Moves two levels up from the current file (json_column directory)
sys.path.append(str(project_root))

from db_connection import create_connection


conn = create_connection()
cursor = conn.cursor()

# Define SQL to add the profile column if it doesn't exist
alter_table_sql = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'actor' AND column_name = 'profile') THEN
        ALTER TABLE actor ADD COLUMN profile JSONB;
    END IF;
END $$;
"""

# Execute the SQL to add the column if it doesn't exist
cursor.execute(alter_table_sql)

# Commit the changes
conn.commit()

# Now, query the information_schema to check if the column exists
check_column_sql = """
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'actor' AND column_name = 'profile';
"""

# Execute the query to check if the column exists
cursor.execute(check_column_sql)

# Fetch the result
result = cursor.fetchone()

if result:
    print("The 'profile' column exists in the 'actor' table.")
else:
    print("The 'profile' column does not exist in the 'actor' table.")

# Close the cursor and connection
cursor.close()
conn.close()
