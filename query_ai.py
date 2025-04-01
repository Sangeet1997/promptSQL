import sqlite3
import ollama
from tabulate import tabulate

def generate_sql_query(user_prompt):
    """Uses LLaMA 3.2 to generate an SQL query based on natural language input."""
    model_prompt = f"""
    Convert the following user request into a SQL query for a SQLite database. 
    Assume the database has a table 'my_cars' with columns 'car_ID', 'symboling', 'CarName', 'fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel', 'enginelocation', 'wheelbase', 'carlength', 'carwidth', 'carheight', 'curbweight', 'enginetype', 'cylindernumber', 'enginesize', 'fuelsystem', 'boreratio', 'stroke', 'compressionratio', 'horsepower', 'peakrpm', 'citympg', 'highwaympg', 'price'.
    
    User request: {user_prompt}
    SQL query:
    ***RETURN ONLY THE QUERY AND NOTHING ELSE***
    """
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": model_prompt}])
    sql_query = response["message"]["content"].strip()

    # Ensure query is safe
    if any(kw in sql_query.upper() for kw in ["DELETE", "DROP", "INSERT", "UPDATE", "ALTER"]):
        return "ERROR: Unsafe query detected. Only SELECT statements are allowed."
    
    return sql_query

def execute_query(sql_query):
    """Executes the generated SQL query on the local SQLite database."""
    try:
        conn = sqlite3.connect("data/cardatabase.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]  # Get column names
        conn.close()

        if results:
            return tabulate(results, headers, tablefmt="pretty")
        else:
            return "No results found."
    except Exception as e:
        return f"SQL Execution Error: {e}"

def handle_query(user_prompt):
    """Generates and executes an SQL query with retry logic for errors."""
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        sql_query = generate_sql_query(user_prompt)
        if "ERROR" in sql_query:
            return sql_query
        
        result = execute_query(sql_query)
        if not result.startswith("SQL Execution Error"):
            return f"\nGenerated SQL Query:\n{sql_query}\n\nExecution Result:\n{result}"
        
        attempt += 1
    
    return "Execution failed after multiple attempts. Please refine your query."

def main():
    while True:
        user_input = input("\nEnter a query prompt (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        result = handle_query(user_input)
        print(result)

if __name__ == "__main__":
    main()
