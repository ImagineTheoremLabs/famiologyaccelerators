# #!/usr/bin/env python
# # coding: utf-8

# # In[ ]:

# import streamlit as st
# import pandas as pd
# from faker import Faker
# import numpy as np

# def calculate_categorical_distribution(column):
#     """Calculate the percentage distribution of each unique category."""
#     value_counts = column.value_counts(normalize=True) * 100
#     return value_counts.to_dict()

# def main():
#     st.title('Synthetic Data-Generator')
#     fake = Faker()

#     # Faker functions for categorical data
#     faker_functions = {
#         'Name': fake.name,
#         'Email': fake.email,
#         'City': fake.city,
#         'Country': fake.country,
#         'Text': fake.text,
#         'Date': fake.date,
#         'Custom (comma-separated)': None  # Placeholder for custom user input
#     }

#     uploaded_file = st.file_uploader("Upload your input CSV or Excel file", type=['csv', 'xlsx'])

#     if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
#         numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
#         categorical_columns = df.select_dtypes(include=['object', 'category']).columns

#         # Handling Numeric Attributes inside a form
#         with st.form(key='numeric_form'):
#             numeric_data = {}
#             for col in numeric_columns:
#                 col1, col2, col3, col4 = st.columns(4)
#                 with col1:
#                     st.text(col)
#                 with col2:
#                     max_val = st.number_input(f"Max for {col}", value=int(df[col].max()), key=f"max_{col}")
#                 with col3:
#                     min_val = st.number_input(f"Min for {col}", value=int(df[col].min()), key=f"min_{col}")
#                 with col4:
#                     distribution_pct = st.number_input(f"Distribution % for {col}", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key=f"dist_{col}")
#                 numeric_data[col] = {'max': max_val, 'min': min_val, 'distribution': distribution_pct}
#             submit_numeric = st.form_submit_button("Update Numeric Data")

#         # Handling Categorical Attributes dynamically
#         categorical_data = {}
#         for col in categorical_columns:
#             col1, col2, col3 = st.columns([1, 2, 1])
#             with col1:
#                 st.text(col)
#             with col2:
#                 selected_function = st.selectbox(f"Select function for {col}", list(faker_functions.keys()), key=f"func_{col}")
#             with col3:
#                 if selected_function == 'Custom (comma-separated)':
#                     custom_values = st.text_input(f"Enter custom values for {col}", key=f"custom_{col}")
#                     if custom_values:
#                         custom_values_list = custom_values.split(',')
#                         equal_dist = 100.0 / len(custom_values_list)
#                         distribution_pct = st.number_input(f"Distribution % for {col}", value=equal_dist, key=f"dist_cat_{col}")
#                         categorical_data[col] = (custom_values_list, distribution_pct)
#                 else:
#                     dist_dict = calculate_categorical_distribution(df[col])
#                     dist_values = list(dist_dict.values())
#                     dist_keys = list(dist_dict.keys())
#                     distribution_pct = st.number_input(f"Distribution % for {col}", value=float(dist_values[0]), key=f"dist_cat_{col}")
#                     categorical_data[col] = (faker_functions[selected_function], distribution_pct, dist_keys, dist_values)

#         num_rows = st.number_input("Number of rows to generate:", min_value=1, value=100, step=1)

#         if st.button('Generate Synthetic-Data'):
#             synthetic_data = {}
#             for col, info in numeric_data.items():
#                 synthetic_data[col] = np.random.uniform(low=info['min'], high=info['max'], size=num_rows)
#             for col, values, dist, dist_keys, dist_values in categorical_data.items():
#                 print("This is Col", col)
#                 print("This is Values ", values)
#                 print("This is dist", dist)
#                 print("This is dist_keys", dist_keys)
#                 print("This is dist_values", dist_values)
    
#                 if isinstance(values, list):
#                     # Adjust the generation to respect the distribution percentage
#                     main_value_count = int(num_rows * (dist / 100))
#                     other_values_count = num_rows - main_value_count
#                     main_values = [values[0]] * main_value_count
#                     other_values = np.random.choice(values[1:], size=other_values_count)
#                     synthetic_data[col] = np.concatenate((main_values, other_values))
#                 else:
#                     # Generate data based on the distribution of actual data
#                     synthetic_data[col] = np.random.choice(dist_keys, size=num_rows, p=np.array(dist_values) / 100)

#             synthetic_df = pd.DataFrame(synthetic_data)
#             st.write("Generated Synthetic Data:")
#             st.dataframe(synthetic_df.head())

#             csv = synthetic_df.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="Download synthetic data new CSV",
#                 data=csv,
#                 file_name='synthetic_data.csv',
#                 mime='text/csv',
#             )

# if __name__ == '__main__':
#     main()



# import streamlit as st
# import pandas as pd
# from faker import Faker
# import numpy as np

# def calculate_categorical_distribution(column):
#     """Calculate the percentage distribution of each unique category."""
#     value_counts = column.value_counts(normalize=True) * 100
#     return value_counts.to_dict()

# def main():
#     st.title('Synthetic Data Generator')
#     fake = Faker()

#     # Faker functions for categorical data
#     faker_functions = {
#         'Name': fake.name,
#         'Email': fake.email,
#         'City': fake.city,
#         'Country': fake.country,
#         'Text': fake.text,
#         'Date': fake.date,
#         'Custom (comma-separated)': None  # Placeholder for custom user input
#     }

#     uploaded_file = st.file_uploader("Upload your input CSV or Excel file", type=['csv', 'xlsx'])

#     if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
#         numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
#         categorical_columns = df.select_dtypes(include=['object', 'category']).columns

#         # Handling Numeric Attributes inside a form
#         with st.form(key='numeric_form'):
#             numeric_data = {}
#             for col in numeric_columns:
#                 col1, col2, col3, col4 = st.columns(4)
#                 with col1:
#                     st.text(col)
#                 with col2:
#                     max_val = st.number_input(f"Max for {col}", value=int(df[col].max()), key=f"max_{col}")
#                 with col3:
#                     min_val = st.number_input(f"Min for {col}", value=int(df[col].min()), key=f"min_{col}")
#                 with col4:
#                     distribution_pct = st.number_input(f"Distribution % for {col}", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key=f"dist_{col}")
#                 numeric_data[col] = {'max': max_val, 'min': min_val, 'distribution': distribution_pct}
#             submit_numeric = st.form_submit_button("Update Numeric Data")

#         # Handling Categorical Attributes dynamically
#         categorical_data = {}
#         for col in categorical_columns:
#             col1, col2, col3 = st.columns([1, 2, 1])
#             with col1:
#                 st.text(col)
#             with col2:
#                 selected_function = st.selectbox(f"Select function for {col}", list(faker_functions.keys()), key=f"func_{col}")
#             with col3:
#                 if selected_function == 'Custom (comma-separated)':
#                     custom_values = st.text_input(f"Enter custom values for {col}", key=f"custom_{col}")
#                     if custom_values:
#                         custom_values_list = custom_values.split(',')
#                         equal_dist = 100.0 / len(custom_values_list)
#                         categorical_data[col] = {'values': custom_values_list, 'dist': equal_dist}
#                 else:
#                     dist_dict = calculate_categorical_distribution(df[col])
#                     dist_values = list(dist_dict.values())
#                     dist_keys = list(dist_dict.keys())
#                     categorical_data[col] = {'function': faker_functions[selected_function], 'dist_keys': dist_keys, 'dist_values': dist_values}

#         num_rows = st.number_input("Number of rows to generate:", min_value=1, value=100, step=1)

#         if st.button('Generate Synthetic Data'):
#             synthetic_data = {}
#             for col, info in numeric_data.items():
#                 synthetic_data[col] = np.random.uniform(low=info['min'], high=info['max'], size=num_rows)
            
#             for col, details in categorical_data.items():
#                 if 'values' in details:
#                     # Custom values
#                     values = details['values']
#                     dist = details['dist']
#                     main_value_count = int(num_rows * (dist / 100))
#                     other_values_count = num_rows - main_value_count
#                     main_values = [values[0]] * main_value_count
#                     other_values = np.random.choice(values[1:], size=other_values_count)
#                     synthetic_data[col] = np.concatenate((main_values, other_values))
#                 else:
#                     # Faker function values
#                     dist_keys = details['dist_keys']
#                     dist_values = details['dist_values']
#                     synthetic_data[col] = np.random.choice(dist_keys, size=num_rows, p=np.array(dist_values) / 100)

#             synthetic_df = pd.DataFrame(synthetic_data)
#             st.write("Generated Synthetic Data:")
#             st.dataframe(synthetic_df.head())

#             csv = synthetic_df.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="Download synthetic data as CSV",
#                 data=csv,
#                 file_name='synthetic_data.csv',
#                 mime='text/csv',
#             )

# if __name__ == '__main__':
#     main()


import streamlit as st
import pandas as pd
from faker import Faker
import numpy as np

def calculate_categorical_distribution(column):
    """Calculate the percentage distribution of each unique category."""
    value_counts = column.value_counts(normalize=True) * 100
    return value_counts.to_dict()

def main():
    st.title('Synthetic Data Generator')
    fake = Faker()

    # Faker functions for categorical data
    faker_functions = {
        'Name': fake.name,
        'Email': fake.email,
        'City': fake.city,
        'Country': fake.country,
        'Text': fake.text,
        'Date': fake.date,
        'Custom (comma-separated)': None  # Placeholder for custom user input
    }

    uploaded_file = st.file_uploader("Upload your input CSV or Excel file", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns

        # Handling Numeric Attributes inside a form
        with st.form(key='numeric_form'):
            numeric_data = {}
            for col in numeric_columns:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.text(col)
                with col2:
                    max_val = st.number_input(f"Max for {col}", value=int(df[col].max()), key=f"max_{col}")
                with col3:
                    min_val = st.number_input(f"Min for {col}", value=int(df[col].min()), key=f"min_{col}")
                with col4:
                    distribution_pct = st.number_input(f"Distribution % for {col}", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key=f"dist_{col}")
                numeric_data[col] = {'max': max_val, 'min': min_val, 'distribution': distribution_pct}
            submit_numeric = st.form_submit_button("Update Numeric Data")

        # Handling Categorical Attributes dynamically
        categorical_data = {}
        for col in categorical_columns:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.text(col)
            with col2:
                selected_function = st.selectbox(f"Select function for {col}", list(faker_functions.keys()), key=f"func_{col}")
            with col3:
                if selected_function == 'Custom (comma-separated)':
                    custom_values = st.text_input(f"Enter custom values for {col}", key=f"custom_{col}")
                    if custom_values:
                        custom_values_list = custom_values.split(',')
                        categorical_data[col] = {'values': custom_values_list, 'dist': None}
                        for value in custom_values_list:
                            dist = st.number_input(f"Distribution % for {value} in {col}", min_value=0.0, max_value=100.0, value=100.0/len(custom_values_list), step=0.1, key=f"dist_{col}_{value}")
                            categorical_data[col][value] = dist
                else:
                    dist_dict = calculate_categorical_distribution(df[col])
                    dist_values = list(dist_dict.values())
                    dist_keys = list(dist_dict.keys())
                    categorical_data[col] = {'function': faker_functions[selected_function], 'dist_keys': dist_keys, 'dist_values': dist_values}

        num_rows = st.number_input("Number of rows to generate:", min_value=1, value=100, step=1)

        if st.button('Generate Synthetic Data'):
            synthetic_data = {}
            for col, info in numeric_data.items():
                synthetic_data[col] = np.random.uniform(low=info['min'], high=info['max'], size=num_rows)
            
            for col, details in categorical_data.items():
                if 'values' in details:
                    # Custom values
                    values = details['values']
                    dist = [details[value] for value in values]
                    synthetic_data[col] = np.random.choice(values, size=num_rows, p=np.array(dist) / 100)
                else:
                    # Faker function values
                    dist_keys = details['dist_keys']
                    dist_values = details['dist_values']
                    synthetic_data[col] = np.random.choice(dist_keys, size=num_rows, p=np.array(dist_values) / 100)

            synthetic_df = pd.DataFrame(synthetic_data)
            st.write("Generated Synthetic Data:")
            st.dataframe(synthetic_df.head())

            csv = synthetic_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download synthetic data as CSV",
                data=csv,
                file_name='synthetic_data.csv',
                mime='text/csv',
            )

if __name__ == '__main__':
    main()
