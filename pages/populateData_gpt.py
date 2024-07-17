import sqlite3
import pandas as pd
import numpy as np


# Path to your Excel file
excel_file_path = 'data/FamilyOfficeEntityDataSampleV1.1.xlsx'



# Load the Excel file
excel_data = pd.ExcelFile(excel_file_path)

# Connect to SQLite database (or create it if it doesn't exist)


def create_table_from_dataframe(conn, dataframe, table_name):
    cursor = conn.cursor()
    
    # Define the table schema
    columns = dataframe.columns
    column_types = dataframe.dtypes
    column_definitions = []

    trimmed_columns = [column.lstrip().rstrip() for column in columns]

    print("trimmed_columns", trimmed_columns)

    
    for column, dtype in zip(trimmed_columns, column_types):
        print("column", column, str(dtype))
        if 'int' in str(dtype):
            column_definitions.append(f"{column.replace(' ', '_')} INTEGER")
        elif 'float' in str(dtype):
            column_definitions.append(f"{column.replace(' ', '_')} REAL")
        else:
            column_definitions.append(f"{column.replace(' ', '_')} TEXT")
        # if np.issubdtype(dtype, np.integer):
        #     column_definitions.append(f"{column.replace(' ', '_')} INTEGER")
        # elif np.issubdtype(dtype, np.floating):
        #     column_definitions.append(f"{column.replace(' ', '_')} REAL")
        # elif np.issubdtype(dtype, np.datetime64):
        #     column_definitions.append(f"{column.replace(' ', '_')} DATETIME")
        # else:
        #     column_definitions.append(f"{column.replace(' ', '_')} TEXT")
    
    column_definitions_str = ', '.join(column_definitions)

    print("column_definitions", column_definitions)

    table_name = table_name.replace(' ', '_')

    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions_str});"
    print("create_table_sql", create_table_sql)

    
    # Create the table
    cursor.execute(create_table_sql)

    
    
    # Insert data into the table
    for row in dataframe.itertuples(index=False, name=None):
        placeholders = ', '.join(['?' for _ in columns])
        row = tuple(
            r.strftime('%Y-%m-%d %H:%M:%S') if isinstance(r, pd.Timestamp) and r is not pd.NaT else None if pd.isna(r) else r 
            for r in row
        )
        insert_sql = f"INSERT INTO {table_name} ({','.join(trimmed_columns).replace(' ', '_')}) VALUES ({placeholders})"
        print("insert_sql", row)
        for r in row:
            print("rType", type(r))
        cursor.execute(insert_sql, row)
    
    conn.commit()


def InitializeTempSqliteDatabase(ExcelData):
    conn = sqlite3.connect('data/database.db')

    sheetNames = ["Client Profile", "Family Members"]

    # Iterate through each sheet in the Excel file
    for sheet_name in sheetNames: #ExcelData.sheet_names:
        # Load the sheet into a DataFrame
        df = excel_data.parse(sheet_name)

        print("sheet_name", sheet_name)

        # Create table and insert data
        create_table_from_dataframe(conn, df, sheet_name)
    conn.close()


# InitializeTempSqliteDatabase(excel_data)
# Close the connection
