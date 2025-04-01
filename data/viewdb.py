import sqlite3

db_name = "cardatabase.db"
table_name = "my_cars"

# Connect to SQLite database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Fetch data from table
cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
rows = cursor.fetchall()

# Print column names
columns = [description[0] for description in cursor.description]
print("Columns:", columns)

# Print rows
for row in rows:
    print(row)

# Close connection
conn.close()
