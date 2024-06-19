import streamlit as st
import pdfplumber
from PIL import Image
from pdf2image import convert_from_bytes
import io
import fitz 
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import base64

# logo on tab
page_icon = Image.open("pages/favicon.ico")
st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
logo = Image.open("pages/favicon.ico")

# set width of sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 338px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# logo on sidebar
# st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

# logo specifically on top of sidebar
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
                padding-top: 80px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

html = """
<div style="text-align: center;">
    <img src="FamiologyTextLogo.png" alt="Logo" width="700">
    <h1>Famiology Accelerators</h1>
</div>
"""
st.markdown(html, unsafe_allow_html=True)

# Add a subheading
st.subheader("Welcome to Famiology, the ultimate Life Management Solution for Generation GenX. ")

# Add some introductory text
st.write("""
Our platform offers unparalleled convenience by streamlining financial and life document management. Simplify your life and stay organized effortlessly with Famiology.""")

# def main():
#     with st.sidebar.container():
#         # Section 1: Apps
#         with st.expander("Apps"):
#             st.markdown('<a href="https://famiologydocdetector.streamlit.app/" target="_self">Document Detector</a>', unsafe_allow_html=True)
#             st.markdown('<a href="https://famiology-smart-fill.streamlit.app/" target="_self">Smart Fill</a>', unsafe_allow_html=True)
        

# if __name__ == "__main__":
#     main()
