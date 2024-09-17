# pip install ctgan
# !pip install table_evaluator
# !pip install sqlite3

import pandas as pd
import numpy as np
import sqlite3
from ctgan import CTGAN
import hashlib

def generateDataForTable(tableName, NUMBER_OF_RECORDS_TO_GENERATE = 5):
    # Connect to your SQLite database
    conn = sqlite3.connect('database.db')

    # Load your data from a specific table in the SQLite database
    data = pd.read_sql_query(f'SELECT * FROM {tableName}', conn)

    # Check the data types of your columns
    print(data.dtypes)

    # Example: Converting date columns to a proper datetime format or excluding them if not needed
    for column in data.columns:
        if data[column].dtype == 'object':
            try:
                data[column] = pd.to_datetime(data[column])
            except ValueError:
                print(f"Column {column} could not be converted to datetime.")

    # Alternatively, you might want to exclude non-numeric columns:
    numeric_data = data.select_dtypes(include=[np.number])
    categorical_features = [col for col in data.columns if col not in numeric_data.columns]

    # categorical_features


    def hash_column(column):
        return column.apply(lambda x: hashlib.sha256(x.encode()).hexdigest())

    pii_columns = ['Contact_Information']  # Correct column name

    for column in pii_columns:
        data[column] = hash_column(data[column])

    # Fill missing values for categorical columns with the mode
    for col in categorical_features:
        if data[col].isnull().any():
            mode = data[col].mode()[0]
            data[col].fillna(mode, inplace=True)

    # Create and fit the CTGAN model
    ctgan = CTGAN(verbose=True)
    ctgan.fit(data, categorical_features, epochs=200)

    # Generate synthetic data
    synthetic_data = ctgan.sample(NUMBER_OF_RECORDS_TO_GENERATE)

    # Postprocess to enforce constraints
    def enforce_constraints(df):
        def check_family(df):
            families = df.groupby('ClientID')
            new_rows = []

            for client_id, family in families:
                # Ensure one "Self" and one "Spouse" per family
                num_self = len(family[family['Relation'] == 'Self'])
                num_spouse = len(family[family['Relation'] == 'Spouse'])

                if num_self == 0:
                    new_rows.append({'ClientID': client_id, 'Relation': 'Self', 'Age': 27})
                elif num_self > 1:
                    family = family.drop(family[family['Relation'] == 'Self'].index[1:], inplace=False)

                if num_spouse == 0:
                    new_rows.append({'ClientID': client_id, 'Relation': 'Spouse', 'Age': 27})
                elif num_spouse > 1:
                    family = family.drop(family[family['Relation'] == 'Spouse'].index[1:], inplace=False)

                # Ensure 0 to 5 "Child" entries per family
                num_children = np.random.randint(0, 6)  # Randomly pick the number of children from 0 to 5
                actual_children = family[family['Relation'] == 'Child']

                if len(actual_children) > num_children:
                    actual_children = actual_children.iloc[:num_children]
                elif len(actual_children) < num_children:
                    for _ in range(num_children - len(actual_children)):
                        new_rows.append({'ClientID': client_id, 'Relation': 'Child', 'Age': np.random.randint(1, 18)})

                family = pd.concat([family[family['Relation'] != 'Child'], actual_children])
                new_rows.extend(family.to_dict(orient='records'))

            df = pd.DataFrame(new_rows)

            return df

        # Ensure state is the same for members of the same family
        if 'State' in df.columns:
            df['State'] = df.groupby('ClientID')['State'].transform(lambda x: x.mode()[0])

        df = check_family(df)

        # Ensure ClientID is unique and positive starting from 1, and consistent within families
        unique_client_ids = df['ClientID'].unique()
        id_mapping = {old_id: new_id for new_id, old_id in enumerate(unique_client_ids, start=1)}
        df['ClientID'] = df['ClientID'].map(id_mapping)

        # Set age constraints and handle NaN values
        df.loc[df['Relation'] == 'Self', 'Age'] = df.loc[df['Relation'] == 'Self', 'Age'].apply(lambda x: max(x, 27) if not pd.isna(x) else 27)
        df.loc[df['Relation'] == 'Spouse', 'Age'] = df.loc[df['Relation'] == 'Spouse', 'Age'].apply(lambda x: max(x, 27) if not pd.isna(x) else 27)
        df.loc[df['Relation'] == 'Child', 'Age'] = df.loc[df['Relation'] == 'Child', 'Age'].apply(lambda x: max(x, 1) if not pd.isna(x) else np.random.randint(1, 18))

        # Ensure no NaN values
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)

        return df

    if 'Relation' not in synthetic_data.columns:
        print("The 'Relation' column does not exist in the synthetic data.")
    else:
        # Apply constraints if 'Relation' column exists
        synthetic_data = enforce_constraints(synthetic_data)
        print(synthetic_data.head())

    # Save or use the synthetic data
    print(synthetic_data.head())
    print("synthetic_data", type(synthetic_data))

    # Assuming 'df' is your DataFrame
    list_of_tuples = [tuple(row) for row in synthetic_data.to_records(index=False)]

    # Print or use the list of tuples
    print(list_of_tuples)
    return list_of_tuples

    # synthetic_data

# generateDataForTable("client_profile")