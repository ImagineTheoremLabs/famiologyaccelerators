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

page_icon = Image.open("pages/favicon.ico")
st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
logo = Image.open("pages/favicon.ico")

# Streamlit UI
# st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

file = open("FamiologyTextLogo.png", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((300, 75))  # x, y
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

# def main():
#     with st.sidebar.container():
#         # Section 1: Apps
#         with st.expander("Apps"):
#             st.markdown('<a href="https://famiologydocdetector.streamlit.app/" target="_self">Document Detector</a>', unsafe_allow_html=True)
#             st.markdown('<a href="https://famiology-smart-fill.streamlit.app/" target="_self">Smart Fill</a>', unsafe_allow_html=True)
        

# if __name__ == "__main__":
#     main()




