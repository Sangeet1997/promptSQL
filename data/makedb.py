import sqlite3
import pandas as pd
import sys

def csv_to_sqlite(csv_file, db_name, table_name):
    # Load CSV into a Pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Infer column names and data types
    columns = df.columns
    column_types = []
    
    for col in columns:
        sample_value = df[col].dropna().iloc[0] if not df[col].dropna().empty else ''
        if isinstance(sample_value, int):
            col_type = "INTEGER"
        elif isinstance(sample_value, float):
            col_type = "REAL"
        else:
            col_type = "TEXT"
        column_types.append(f'"{col}" {col_type}')
    
    # Create table query
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_types)});"
    cursor.execute(create_table_query)
    
    # Insert data into table
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Commit and close
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created successfully with table '{table_name}'")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <csv_file> <database_name> <table_name>")
    else:
        csv_file = sys.argv[1]
        db_name = sys.argv[2]
        table_name = sys.argv[3]
        csv_to_sqlite(csv_file, db_name, table_name)
