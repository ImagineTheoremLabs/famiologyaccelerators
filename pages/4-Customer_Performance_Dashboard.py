import datetime
import numpy as np
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
import io
import os

# Set the path to your logo image here
LOGO_PATH = "img/Theoremlabs_logo.png"  # Update this path as needed

# Load the page icon
page_icon = Image.open("./pages/favicon.ico")

# Set page configuration
st.set_page_config(page_title="Customer Performance Dashboard", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")

# Improved CSS styles
css = """


/* Sidebar styling */
[data-testid="stSidebar"] {
    width: 338px !important;
}

/* Main content area */
.main .block-container {
    max-width: 1200px;
    padding: 2rem;
}

/* Text styles */
h1, h2, h3, h4, h5, h6 {
    font-weight: bold;
    margin-bottom: 1rem;
}

/* Card-like containers */
.stMetric, div[data-testid="stMetricValue"] {
    background-color: #262730;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.stMetric:hover, div[data-testid="stMetricValue"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

/* Button styling */
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.stButton > button:hover {
    background-color: #45a049;
}

/* Selectbox styling */
.stSelectbox {
    background-color: #262730;
    border-radius: 5px;
    padding: 0.25rem;
}

/* Graph container */
[data-testid="stPlotlyChart"] {
    background-color: #262730;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
"""

# Apply CSS styles
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Load and display the sidebar logo
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as file:
        contents = file.read()
    img_str = base64.b64encode(contents).decode("utf-8")
    
    # Apply the sidebar logo style
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_str}');
                background-repeat: no-repeat;
                background-position: 20px 20px;
                background-size: auto 160px;
                padding-top: 200px;
                background-color: rgba(0, 0, 0, 0);
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Load data
file_path = "data/FamilyOfficeEntityDataSampleV1.2.xlsx"
df_clProfile = pd.read_excel(file_path, sheet_name="Client Profile")
df_familyMem = pd.read_excel(file_path, sheet_name="Family Members")

# Print column names for debugging
print("Columns in df_clProfile:", df_clProfile.columns)

# Data preprocessing
now = datetime.now()
df_clProfile['Date of Birth'] = pd.to_datetime(df_clProfile['Date of Birth'], format='%m/%d/%y')
df_clProfile['Age'] = ((now - df_clProfile['Date of Birth']).dt.days / 365.25).astype(int)
df_clProfile['Net Worth'] = df_clProfile['Net Worth'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Set the maximum age value
max_age_value = 52

# Ensure the calculated ages do not exceed the maximum age value
df_clProfile['Age'] = df_clProfile['Age'].apply(lambda x: x if x <= max_age_value else max_age_value)

# Dashboard title
st.title("Customer Performance Dashboard")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    selected_state = st.selectbox("Select State", ["ALL STATES"] + sorted(df_clProfile['State'].unique()))

with col2:
    age_range = st.slider("Age Range", min_value=df_clProfile['Age'].min(), max_value=max_age_value, value=(df_clProfile['Age'].min(), max_age_value))

with col3:
    status_options = ["ALL"] + list(df_clProfile['Status'].unique())
    selected_status = st.selectbox("Customer Status", status_options)

# Filter data based on selections
filtered_df = df_clProfile.copy()
if selected_state != "ALL STATES":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]
filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]
if selected_status != "ALL":
    filtered_df = filtered_df[filtered_df["Status"] == selected_status]

# Key Metrics
col1, col2, col3 = st.columns(3)

with col1:
    total_revenue = filtered_df['Net Worth'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

with col2:
    total_customers = len(filtered_df)
    st.metric("Total Customers", f"{total_customers:,}")

with col3:
    avg_age = filtered_df['Age'].mean()
    st.metric("Average Age", f"{avg_age:.1f}")

# Charts
col1, col2, col3 = st.columns(3)

with col1:
    # Revenue by Age Group
    df_sorted = filtered_df.copy()
    df_sorted['AgeGroup'] = pd.cut(df_sorted['Age'], bins=[0, 40, 50, 60, 100], labels=['<40', '40-50', '50-60', '60+'])
    revenue_by_age = df_sorted.groupby('AgeGroup')['Net Worth'].sum().reset_index()
    
    fig = px.pie(revenue_by_age, values='Net Worth', names='AgeGroup', title='Revenue by Age Group')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    # Revenue by Customer Status
    revenue_by_status = filtered_df.groupby('Status')['Net Worth'].sum().reset_index()
    fig = px.bar(revenue_by_status, x='Status', y='Net Worth', title='Revenue by Customer Status')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(
            title='Net Worth (Millions)',
            range=[0, revenue_by_status['Net Worth'].max() * 1.1]  # Set y-axis range
        )
    )
    fig.update_traces(marker_color='lightblue')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col3:
    # Revenue from customers with children
    merged_df = pd.merge(filtered_df, df_familyMem, on="ClientID", how="left")
    child_records = merged_df[merged_df["Relationship"] == "Child"]
    total_revenue = filtered_df['Net Worth'].sum()
    revenue_with_children = child_records['Net Worth'].sum()
    revenue_without_children = total_revenue - revenue_with_children

    fig = px.pie(
        values=[revenue_with_children, revenue_without_children],
        names=['With Children', 'Without Children'],
        title='Revenue from Customers with Children'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Top 5 Customers
st.subheader("Top 5 Customers by Revenue")
top_5_customers = filtered_df.nlargest(5, 'Net Worth')[['ClientID', 'Net Worth', 'Age', 'Status']]
st.table(top_5_customers.style.format({'Net Worth': '${:,.0f}'}))

# Add some interactivity
if st.button("Refresh Data"):
    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit")