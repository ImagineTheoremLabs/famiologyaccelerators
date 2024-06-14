# import streamlit as st
# import pandas as pd
# from faker import Faker
# from faker.providers import BaseProvider
# import numpy as np
# import math
# from datetime import datetime
# from io import BytesIO

# class CustomEmailProvider(BaseProvider):
#     def email(self, first_name, last_name, domain="example.com"):
#         return f"{first_name.lower()}.{last_name.lower()}@{domain}"

# def create_excel(dataframe):
#     output = BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
#     writer.close()
#     processed_data = output.getvalue()
#     return processed_data

# def custom_email(first_name, last_name, domain="example.com"):
#     return f"{first_name.lower()}.{last_name.lower()}@{domain}"

# def generate_custom_data(values, percentages, num_rows):
#     custom_data = []
#     for value, percentage in zip(values, percentages):
#         count = int((percentage / 100) * num_rows)
#         custom_data.extend([value] * count)
#     if len(custom_data) < num_rows:
#         custom_data.extend([values[-1]] * (num_rows - len(custom_data)))
#     return custom_data

# def generate_unique_numbers(num_rows):
#     return list(range(1, num_rows + 1))

# def calculate_categorical_distribution(column):
#     """Calculate the percentage distribution of each unique category."""
#     value_counts = column.value_counts(normalize=True) * 100
#     return value_counts.to_dict()

# def generate_unique_values(func, num_rows):
#     """Generate a list of unique values using the given Faker function."""
#     values = set()
#     while len(values) < num_rows:
#         values.add(func())
#     return list(values)

# def calculate_age(dob):
#     """Calculate age from date of birth."""
#     today = datetime.today()
#     return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# def generate_family_member_ids(num_rows):
#     """Generate unique FamilyMemberID values in the format 'Fam-001', 'Fam-002', etc."""
#     return [f"Fam-{str(i).zfill(3)}" for i in range(1, num_rows + 1)]

# def generate_client_spouse_children(num_clients):
#     """Generate client, spouse, and children ensuring each client has one spouse and one self."""
#     client_ids = []
#     relationships = []
#     total_rows = 0
#     for i in range(1, num_clients + 1):
#         client_id = f"{str(i).zfill(3)}"
#         client_ids.append(client_id)
#         relationships.append('Self')
#         client_ids.append(client_id)
#         relationships.append('Spouse')
#         num_children = np.random.randint(0, 5)  # Random number of children between 0 and 4
#         total_rows += 2 + num_children  # Count self, spouse, and children
#         for _ in range(num_children):
#             client_ids.append(client_id)
#             relationships.append('Child')
#     return client_ids, relationships, total_rows

# def main():
#     st.title('Synthetic Data Generator')
#     fake = Faker()
#     fake.add_provider(CustomEmailProvider)

#     option = st.selectbox('Choose an option:', ['Upload Excel Sheet', 'Create Data Manually'])

#     if option == 'Upload Excel Sheet':
#         uploaded_file = st.file_uploader("Upload your input CSV or Excel file", type=['csv', 'xlsx'])

#         if uploaded_file is not None:
#             df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
#             numeric_columns = df.select_dtypes(include=['int', 'float']).columns
#             categorical_columns = df.select_dtypes(include=['object', 'category']).columns
#             date_columns = df.select_dtypes(include=['datetime64']).columns

#             # Check if specific columns are present
#             first_name_column_present = 'First Name' in df.columns
#             last_name_column_present = 'Last Name' in df.columns
#             email_column_present = 'Email' in df.columns
#             dob_column_present = 'Date of Birth' in df.columns
#             age_column_present = 'Age' in df.columns
#             family_member_id_column_present = 'FamilyMemberID' in df.columns
#             client_id_column_present = 'ClientID' in df.columns
#             spouse_id_column_present = 'SpouseID' in df.columns
#             relationship_column_present = 'Relationship' in df.columns

#             # Handling Numeric Attributes inside a form
#             with st.form(key='numeric_form'):
#                 numeric_data = {}
#                 for idx, col in enumerate(numeric_columns):
#                     col1, col2, col3, col4 = st.columns(4)
#                     with col1:
#                         st.text(col)
#                     with col2:
#                         max_val = st.number_input(f"Max for {col}", value=int(math.ceil(df[col].max())), key=f"max_{col}")
#                     with col3:
#                         min_val = st.number_input(f"Min for {col}", value=int(df[col].min()), key=f"min_{col}")
#                     numeric_data[col] = {'max': max_val, 'min': min_val, 'unique': idx != 0}
#                 submit_numeric = st.form_submit_button("Update Numeric Data")

#             # Handling Date Attributes
#             date_data = {}
#             for col in date_columns:
#                 col1, col2, col3 = st.columns(3)
#                 with col1:
#                     st.text(col)
#                 with col2:
#                     start_date = st.date_input(f"Start date for {col}", value=pd.to_datetime(df[col].min()), key=f"start_{col}")
#                 with col3:
#                     end_date = st.date_input(f"End date for {col}", value=pd.to_datetime(df[col].max()), key=f"end_{col}")
#                 date_data[col] = {'start_date': start_date, 'end_date': end_date}

#             # Faker functions for categorical data
#             faker_functions = {
#                 'First Name': fake.first_name,
#                 'Last Name': fake.last_name,
#                 'Email': 'email',  # Placeholder for custom email generation
#                 'City': fake.city,
#                 'Country': fake.country,
#                 'Text': fake.text,
#                 'Date': fake.date_between,  # Ensure this is used correctly in the date handling section
#                 'Net Worth': lambda: fake.random_int(min=5000, max=1000000),  # Added Net Worth Faker function
#                 'Custom (comma-separated)': None  # Placeholder for custom user input
#             }

#             # Handling Categorical Attributes dynamically
#             categorical_data = {}
#             for col in categorical_columns:
#                 col1, col2, col3 = st.columns([1, 2, 1])
#                 with col1:
#                     st.text(col)
#                 with col2:
#                     selected_function = st.selectbox(f"Select function for {col}", list(faker_functions.keys()), key=f"func_{col}")
#                 with col3:
#                     if selected_function == 'Custom (comma-separated)':
#                         custom_values = st.text_input(f"Enter custom values for {col}", key=f"custom_{col}")
#                         if custom_values:
#                             custom_values_list = custom_values.split(',')
#                             custom_counts = [st.number_input(f"Number of entries for {value}", min_value=0, max_value=None, value=1, step=1, key=f"count_{col}_{value}") for value in custom_values_list]
#                             categorical_data[col] = {'values': custom_values_list, 'counts': custom_counts}
#                     else:
#                         dist_dict = calculate_categorical_distribution(df[col])
#                         dist_values = list(dist_dict.values())
#                         dist_keys = list(dist_dict.keys())
#                         categorical_data[col] = {'function': selected_function, 'dist_keys': dist_keys, 'dist_values': dist_values}

#             num_rows = st.number_input("Number of rows to generate:", min_value=1, value=100, step=1)

#             if st.button('Generate Synthetic Data'):
#                 synthetic_data = {}
#                 client_ids, relationships, total_rows = generate_client_spouse_children(num_rows)

#                 for idx, (col, info) in enumerate(numeric_data.items()):
#                     range_size = info['max'] - info['min'] + 1
#                     if col == 'ClientID':
#                         synthetic_data[col] = client_ids
#                     elif info['unique']:
#                         if total_rows <= range_size:
#                             synthetic_data[col] = generate_unique_values(lambda: np.random.randint(info['min'], info['max']), total_rows)
#                         else:
#                             synthetic_data[col] = np.random.choice(np.arange(info['min'], info['max'] + 1), size=total_rows, replace=True)
#                     else:
#                         synthetic_data[col] = np.random.randint(low=info['min'], high=info['max'], size=total_rows)

#                 for col, details in date_data.items():
#                     start_date = details['start_date']
#                     end_date = details['end_date']
#                     synthetic_data[col] = [fake.date_between(start_date=start_date, end_date=end_date) for _ in range(total_rows)]

#                 if first_name_column_present:
#                     first_names = generate_unique_values(fake.first_name, total_rows) if 'First Name' in numeric_data else [fake.first_name() for _ in range(total_rows)]
#                     synthetic_data['First Name'] = first_names
#                 if last_name_column_present:
#                     last_names = generate_unique_values(fake.last_name, total_rows) if 'Last Name' in numeric_data else [fake.last_name() for _ in range(total_rows)]
#                     synthetic_data['Last Name'] = last_names

#                 if relationship_column_present and client_id_column_present:
#                     synthetic_data['ClientID'] = client_ids
#                     synthetic_data['Relationship'] = relationships

#                 for col, details in categorical_data.items():
#                     if col == 'Email' and first_name_column_present and last_name_column_present:
#                         emails = [fake.email(fn, ln) for fn, ln in zip(synthetic_data['First Name'], synthetic_data['Last Name'])]
#                         synthetic_data['Email'] = emails
#                     elif col == 'Email' and not (first_name_column_present and last_name_column_present):
#                         continue
#                     elif 'values' in details:
#                         values = details['values']
#                         counts = details['counts']
#                         synthetic_data[col] = []
#                         for value, count in zip(values, counts):
#                             synthetic_data[col].extend([value] * count)
#                         while len(synthetic_data[col]) < total_rows:
#                             synthetic_data[col].extend(values)
#                         synthetic_data[col] = synthetic_data[col][:total_rows]
#                     elif 'function' in details:
#                         function = faker_functions[details['function']]
#                         if function == 'email':
#                             if first_name_column_present and last_name_column_present:
#                                 synthetic_data['Email'] = [fake.email(fn, ln) for fn, ln in zip(synthetic_data['First Name'], synthetic_data['Last Name'])]
#                         else:
#                             synthetic_data[col] = [function() for _ in range(total_rows)]

#                 if dob_column_present and age_column_present:
#                     dob_list = synthetic_data['Date of Birth']
#                     age_list = [calculate_age(dob) for dob in dob_list]
#                     synthetic_data['Age'] = age_list

#                 if family_member_id_column_present:
#                     synthetic_data['FamilyMemberID'] = generate_family_member_ids(total_rows)

#                 synthetic_df = pd.DataFrame(synthetic_data)

#                 for col in numeric_columns:
#                     synthetic_df[col] = synthetic_df[col].round()

#                 st.write("Generated Synthetic Data:")
#                 st.dataframe(synthetic_df.head())

#                 csv = synthetic_df.to_csv(index=False).encode('utf-8')
#                 st.download_button(
#                     label="Download synthetic data as CSV",
#                     data=csv,
#                     file_name='synthetic_data.csv',
#                     mime='text/csv',
#                 )

#     elif option == 'Create Data Manually':
#         st.write("Enter column names separated by commas (e.g., 'First Name, Last Name, Email')")
#         columns_input = st.text_input("Column Names")

#         if columns_input:
#             columns = [col.strip() for col in columns_input.split(',')]
#             num_rows = st.number_input("Number of rows to generate:", min_value=1, value=10, step=1)
#             fake = Faker()

#             # Create a dictionary to store faker functions for each column
#             faker_functions = {
#                 'First Name': fake.first_name,
#                 'Last Name': fake.last_name,
#                 'Phone Number': fake.phone_number,
#                 'Address': fake.address,
#                 'City': fake.city,
#                 'Country': fake.country,
#                 'Text': fake.text,
#                 'Date': fake.date,
#                 'Job': fake.job,
#                 'Company': fake.company,
#                 'Credit Card': fake.credit_card_number,
#                 'Passport': fake.passport_number,
#                 'Net Worth': lambda: fake.random_int(min=5000, max=1000000),
#                 'Contact': lambda: None,  # Placeholder for contact generation
#                 'Client ID': lambda: None,  # Placeholder for unique client IDs
#                 'Custom': None  # Placeholder for custom user input
#             }

#             data = {}
#             first_names = []
#             last_names = []
#             for column in columns:
#                 if column in ['Email', 'Contact', 'Client ID']:
#                     continue
#                 st.write(f"Select faker function for {column}:")
#                 selected_function = st.selectbox(f"Faker function for {column}", list(faker_functions.keys()), key=column)
#                 if selected_function == 'Custom':
#                     custom_values = st.text_input(f"Enter custom values for {column}, separated by commas:", key=f"custom_{column}")
#                     custom_percentages = st.text_input(f"Enter percentages for each custom value, separated by commas:", key=f"percent_{column}")
#                     if custom_values and custom_percentages:
#                         custom_values_list = custom_values.split(',')
#                         custom_percentages_list = list(map(float, custom_percentages.split(',')))
#                         if sum(custom_percentages_list) == 100:
#                             data[column] = generate_custom_data(custom_values_list, custom_percentages_list, num_rows)
#                         else:
#                             st.error("The percentages must sum up to 100.")
#                 else:
#                     faker_func = faker_functions[selected_function]
#                     data[column] = [faker_func() for _ in range(num_rows)]
#                     if column == 'First Name':
#                         first_names = data[column]
#                     if column == 'Last Name':
#                         last_names = data[column]

#             if 'First Name' in columns and 'Last Name' in columns:
#                 if 'Email' in columns:
#                     data['Email'] = [custom_email(fn, ln) for fn, ln in zip(data['First Name'], data['Last Name'])]
#                 if 'Contact' in columns:
#                     data['Contact'] = [custom_email(fn, ln) for fn, ln in zip(first_names, last_names)]

#             if 'Client ID' in columns:
#                 data['Client ID'] = generate_unique_numbers(num_rows)

#             df = pd.DataFrame(data)
            
#             st.write("Preview of the dataframe:")
#             st.dataframe(df)

#             if st.button('Generate Excel'):
#                 excel_data = create_excel(df)
#                 st.download_button(
#                     label="Download Excel file",
#                     data=excel_data,
#                     file_name='generated_sheet.xlsx',
#                     mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#                 )

# if __name__ == '__main__':
#     main()
import streamlit as st
import pandas as pd
from faker import Faker
from faker.providers import BaseProvider
import numpy as np
import math
from datetime import datetime, timedelta
from io import BytesIO
import base64
import io
from PIL import Image

page_icon = Image.open("pages/favicon.ico")
st.set_page_config(page_title="Smart Fill", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
logo = Image.open("pages/favicon.ico")

#setting Famiology Logo at top of sidebar
file = open("FamiologyTextLogo.png", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((300, 60))  # x, y
resized_img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )



class CustomEmailProvider(BaseProvider):
    def email(self, first_name, last_name, domain="example.com"):
        return f"{first_name.lower()}.{last_name.lower()}@{domain}"

def create_excel(dataframe):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def custom_email(first_name, last_name, domain="example.com"):
    return f"{first_name.lower()}.{last_name.lower()}@{domain}"

def generate_custom_data(values, percentages, num_rows):
    custom_data = []
    for value, percentage in zip(values, percentages):
        count = int((percentage / 100) * num_rows)
        custom_data.extend([value] * count)
    if len(custom_data) < num_rows:
        custom_data.extend([values[-1]] * (num_rows - len(custom_data)))
    return custom_data

def generate_unique_numbers(num_rows):
    return list(range(1, num_rows + 1))

def calculate_categorical_distribution(column):
    """Calculate the percentage distribution of each unique category."""
    value_counts = column.value_counts(normalize=True) * 100
    return value_counts.to_dict()

def generate_unique_values(func, num_rows):
    """Generate a list of unique values using the given Faker function."""
    values = set()
    while len(values) < num_rows:
        values.add(func())
    return list(values)

def calculate_age(dob):
    """Calculate age from date of birth."""
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def generate_family_member_ids(num_rows):
    """Generate unique FamilyMemberID values in the format 'Fam-001', 'Fam-002', etc."""
    return [f"Fam-{str(i).zfill(3)}" for i in range(1, num_rows + 1)]

def generate_client_spouse_children(num_clients):
    """Generate client, spouse, and children ensuring each client has one spouse and one self."""
    client_ids = []
    relationships = []
    ages = []
    total_rows = 0
    fake = Faker()
    for i in range(1, num_clients + 1):
        client_id = f"{str(i).zfill(3)}"
        age_self = np.random.randint(30, 50)
        age_spouse = np.random.randint(age_self - 5, age_self - 1)
        client_ids.append(client_id)
        relationships.append('Self')
        ages.append(age_self)
        client_ids.append(client_id)
        relationships.append('Spouse')
        ages.append(age_spouse)
        num_children = np.random.randint(0, 5)  # Random number of children between 0 and 4
        total_rows += 2 + num_children  # Count self, spouse, and children
        for _ in range(num_children):
            age_child = np.random.randint(0, age_spouse - 18)
            client_ids.append(client_id)
            relationships.append('Child')
            ages.append(age_child)
    return client_ids, relationships, ages, total_rows

def pad_column(column, length):
    """Pad the column to the specified length with None values."""
    return column + [None] * (length - len(column))

def main():
    st.title('Synthetic Data Generator')
    fake = Faker()
    fake.add_provider(CustomEmailProvider)

    option = st.selectbox('Choose an option:', ['Upload Excel Sheet', 'Create Data Manually'])

    if option == 'Upload Excel Sheet':
        uploaded_file = st.file_uploader("Upload your input CSV or Excel file", type=['csv', 'xlsx'])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            numeric_columns = df.select_dtypes(include=['int', 'float']).columns
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns
            date_columns = df.select_dtypes(include=['datetime64']).columns

            # Check if specific columns are present
            first_name_column_present = 'First Name' in df.columns
            last_name_column_present = 'Last Name' in df.columns
            email_column_present = 'Email' in df.columns
            dob_column_present = 'Date of Birth' in df.columns
            age_column_present = 'Age' in df.columns
            family_member_id_column_present = 'FamilyMemberID' in df.columns
            client_id_column_present = 'ClientID' in df.columns
            spouse_id_column_present = 'SpouseID' in df.columns
            relationship_column_present = 'Relationship' in df.columns

            # Handling Numeric Attributes inside a form
            with st.form(key='numeric_form'):
                numeric_data = {}
                for idx, col in enumerate(numeric_columns):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.text(col)
                    with col2:
                        max_val = st.number_input(f"Max for {col}", value=int(math.ceil(df[col].max())), key=f"max_{col}")
                    with col3:
                        min_val = st.number_input(f"Min for {col}", value=int(df[col].min()), key=f"min_{col}")
                    numeric_data[col] = {'max': max_val, 'min': min_val, 'unique': idx != 0}
                submit_numeric = st.form_submit_button("Update Numeric Data")

            # Handling Date Attributes
            date_data = {}
            for col in date_columns:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text(col)
                with col2:
                    start_date = st.date_input(f"Start date for {col}", value=pd.to_datetime(df[col].min()), key=f"start_{col}")
                with col3:
                    end_date = st.date_input(f"End date for {col}", value=pd.to_datetime(df[col].max()), key=f"end_{col}")
                date_data[col] = {'start_date': start_date, 'end_date': end_date}

            # Faker functions for categorical data
            faker_functions = {
                'First Name': fake.first_name,
                'Last Name': fake.last_name,
                'Email': 'email',  # Placeholder for custom email generation
                'City': fake.city,
                'Country': fake.country,
                'Text': fake.text,
                'Date': fake.date_between,  # Ensure this is used correctly in the date handling section
                'Net Worth': lambda: fake.random_int(min=5000, max=1000000),  # Added Net Worth Faker function
                'Custom (comma-separated)': None  # Placeholder for custom user input
            }

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
                            custom_counts = [st.number_input(f"Number of entries for {value}", min_value=0, max_value=None, value=1, step=1, key=f"count_{col}_{value}") for value in custom_values_list]
                            categorical_data[col] = {'values': custom_values_list, 'counts': custom_counts}
                    else:
                        dist_dict = calculate_categorical_distribution(df[col])
                        dist_values = list(dist_dict.values())
                        dist_keys = list(dist_dict.keys())
                        categorical_data[col] = {'function': selected_function, 'dist_keys': dist_keys, 'dist_values': dist_values}

            num_rows = st.number_input("Number of rows to generate:", min_value=1, value=100, step=1)

            if st.button('Generate Synthetic Data'):
                synthetic_data = {}
                client_ids, relationships, ages, total_rows = generate_client_spouse_children(num_rows)

                for idx, (col, info) in enumerate(numeric_data.items()):
                    range_size = info['max'] - info['min'] + 1
                    if col == 'ClientID':
                        synthetic_data[col] = client_ids
                    elif info['unique']:
                        if total_rows <= range_size:
                            synthetic_data[col] = generate_unique_values(lambda: np.random.randint(info['min'], info['max']), total_rows)
                        else:
                            synthetic_data[col] = np.random.choice(np.arange(info['min'], info['max'] + 1), size=total_rows, replace=True)
                    else:
                        synthetic_data[col] = np.random.randint(low=info['min'], high=info['max'], size=total_rows)

                for col, details in date_data.items():
                    start_date = details['start_date']
                    end_date = details['end_date']
                    synthetic_data[col] = [fake.date_between(start_date=start_date, end_date=end_date) for _ in range(total_rows)]

                if first_name_column_present:
                    first_names = generate_unique_values(fake.first_name, total_rows) if 'First Name' in numeric_data else [fake.first_name() for _ in range(total_rows)]
                    synthetic_data['First Name'] = first_names
                if last_name_column_present:
                    last_names = generate_unique_values(fake.last_name, total_rows) if 'Last Name' in numeric_data else [fake.last_name() for _ in range(total_rows)]
                    synthetic_data['Last Name'] = last_names

                if relationship_column_present and client_id_column_present:
                    synthetic_data['ClientID'] = client_ids
                    synthetic_data['Relationship'] = relationships

                for col, details in categorical_data.items():
                    if col == 'Email' and first_name_column_present and last_name_column_present:
                        emails = [fake.email(fn, ln) for fn, ln in zip(synthetic_data['First Name'], synthetic_data['Last Name'])]
                        synthetic_data['Email'] = emails
                    elif col == 'Email' and not (first_name_column_present and last_name_column_present):
                        continue
                    elif 'values' in details:
                        values = details['values']
                        counts = details['counts']
                        synthetic_data[col] = []
                        for value, count in zip(values, counts):
                            synthetic_data[col].extend([value] * count)
                        while len(synthetic_data[col]) < total_rows:
                            synthetic_data[col].extend(values)
                        synthetic_data[col] = synthetic_data[col][:total_rows]
                    elif 'function' in details:
                        function = faker_functions[details['function']]
                        if function == 'email':
                            if first_name_column_present and last_name_column_present:
                                synthetic_data['Email'] = [fake.email(fn, ln) for fn, ln in zip(synthetic_data['First Name'], synthetic_data['Last Name'])]
                        else:
                            synthetic_data[col] = [function() for _ in range(total_rows)]

                if dob_column_present and age_column_present:
                    synthetic_data['Age'] = ages

                if family_member_id_column_present:
                    synthetic_data['FamilyMemberID'] = generate_family_member_ids(total_rows)

                # Ensure all columns are padded to the same length
                max_length = max(len(v) for v in synthetic_data.values())
                for col in synthetic_data:
                    synthetic_data[col] = pad_column(synthetic_data[col], max_length)

                synthetic_df = pd.DataFrame(synthetic_data)

                for col in numeric_columns:
                    synthetic_df[col] = synthetic_df[col].round()

                st.write("Generated Synthetic Data:")
                st.dataframe(synthetic_df.head())

                csv = synthetic_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download synthetic data as CSV",
                    data=csv,
                    file_name='synthetic_data.csv',
                    mime='text/csv',
                )

    elif option == 'Create Data Manually':
        st.write("Enter column names separated by commas (e.g., 'First Name, Last Name, Email')")
        columns_input = st.text_input("Column Names")

        if columns_input:
            columns = [col.strip() for col in columns_input.split(',')]
            num_rows = st.number_input("Number of rows to generate:", min_value=1, value=10, step=1)
            fake = Faker()

            # Create a dictionary to store faker functions for each column
            faker_functions = {
                'First Name': fake.first_name,
                'Last Name': fake.last_name,
                'Phone Number': fake.phone_number,
                'Address': fake.address,
                'City': fake.city,
                'Country': fake.country,
                'Text': fake.text,
                'Date': fake.date,
                'Job': fake.job,
                'Company': fake.company,
                'Credit Card': fake.credit_card_number,
                'Passport': fake.passport_number,
                'Net Worth': lambda: fake.random_int(min=5000, max=1000000),
                'Contact': lambda: None,  # Placeholder for contact generation
                'Client ID': lambda: None,  # Placeholder for unique client IDs
                'Custom': None  # Placeholder for custom user input
            }

            data = {}
            first_names = []
            last_names = []
            total_rows = num_rows
            for column in columns:
                if column in ['Email', 'Contact', 'Client ID']:
                    continue
                st.write(f"Select faker function for {column}:")
                selected_function = st.selectbox(f"Faker function for {column}", list(faker_functions.keys()), key=column)
                if selected_function == 'Custom':
                    custom_values = st.text_input(f"Enter custom values for {column}, separated by commas:", key=f"custom_{column}")
                    custom_percentages = st.text_input(f"Enter percentages for each custom value, separated by commas:", key=f"percent_{column}")
                    if custom_values and custom_percentages:
                        custom_values_list = custom_values.split(',')
                        custom_percentages_list = list(map(float, custom_percentages.split(',')))
                        if sum(custom_percentages_list) == 100:
                            data[column] = generate_custom_data(custom_values_list, custom_percentages_list, num_rows)
                        else:
                            st.error("The percentages must sum up to 100.")
                else:
                    faker_func = faker_functions[selected_function]
                    data[column] = [faker_func() for _ in range(num_rows)]
                    if column == 'First Name':
                        first_names = data[column]
                    if column == 'Last Name':
                        last_names = data[column]

            if 'First Name' in columns and 'Last Name' in columns:
                if 'Email' in columns:
                    data['Email'] = [custom_email(fn, ln) for fn, ln in zip(data['First Name'], data['Last Name'])]
                if 'Contact' in columns:
                    data['Contact'] = [custom_email(fn, ln) for fn, ln in zip(first_names, last_names)]

            if 'Client ID' in columns:
                data['Client ID'] = generate_unique_numbers(num_rows)

            if 'Relation' in columns or 'Relationship' in columns:
                client_ids, relationships, ages, total_rows = generate_client_spouse_children(num_rows)
                if 'Relation' in columns:
                    data['Relation'] = relationships[:total_rows]
                if 'Relationship' in columns:
                    data['Relationship'] = relationships[:total_rows]
                if 'Age' in columns:
                    data['Age'] = ages[:total_rows]

            # Ensure all columns have the same length
            max_length = max(len(v) for v in data.values())
            for column in columns:
                if column not in data:
                    data[column] = [None] * max_length
                else:
                    data[column] = pad_column(data[column], max_length)

            df = pd.DataFrame(data)
            
            st.write("Preview of the dataframe:")
            st.dataframe(df)

            if st.button('Generate Excel'):
                excel_data = create_excel(df)
                st.download_button(
                    label="Download Excel file",
                    data=excel_data,
                    file_name='generated_sheet.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

if __name__ == '__main__':
    main()
