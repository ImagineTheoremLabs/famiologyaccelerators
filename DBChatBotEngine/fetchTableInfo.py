import sqlite3

# Path to your SQLite database file
database_path = '../database.db'

def returnTables():
    

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    print("In return tables")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # print("Got tales", tables)

    tablesList = [tple[0] for tple in tables]
    return tablesList

def returnDDL():
# Connect to the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Query to get the DDL for all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    ddl_queries = {}

    print("tables", tables)
    # Extract the DDL for each table
    for table_name in tables:
        table_name = table_name[0]  # Get the table name from the tuple
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        ddl_query = cursor.fetchone()[0]
        ddl_queries[table_name] = ddl_query

    # Close the connection
    connection.close()

    # Output the DDL queries
    for table, ddl in ddl_queries.items():
        print(f"Table: {table}")
        print(ddl)
        print()


if __name__ == "__main__":
    returnDDL()