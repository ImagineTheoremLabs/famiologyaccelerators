import streamlit as st
import pdfplumber
from PIL import Image
from pdf2image import convert_from_bytes
import io
import base64
import json
import os

# Set the path to your logo image here
LOGO_PATH = "img/Theoremlabs_logo.png"  # Update this path as needed

# Load the page icon
page_icon = Image.open("pages/favicon.ico")

# Set page configuration
st.set_page_config(page_title="Smart Fill", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")

# Hardcoded CSS styles
css = """
/* Sidebar width */
section[data-testid="stSidebar"] {
    width: 338px !important;
}

/* Main content area */
.main .block-container {
    max-width: 1200px;
    padding-top: 1rem;
    padding-right: 1rem;
    padding-left: 1rem;
    padding-bottom: 1rem;
}

/* Text colors */
.stText, .stMarkdown, .stTitle, .stSubheader {
    color: white;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    font-weight: bold;
}

/* Sidebar logo */
[data-testid="stSidebarNav"] {
    background-repeat: no-repeat;
    padding-top: 80px;
    background-position: 20px 20px;
}
"""

# Apply CSS styles
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Load and display the sidebar logo
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as file:
        contents = file.read()
    img_str = base64.b64encode(contents).decode("utf-8")
    img = Image.open(io.BytesIO(base64.b64decode(img_str)))
    
    # Calculate new dimensions while maintaining aspect ratio
    max_width = 550
    max_height = 220
    img.thumbnail((max_width, max_height))
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Apply the sidebar logo style
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                background-position: 20px 20px;
                background-size: auto 160px;
                padding-top: 140px;
                background-color: rgba(0, 0, 0, 0);
            }}
            [data-testid="stSidebarNav"]::before {{
                content: "";
                display: block;
                height: 140px;
            }}
            [data-testid="stSidebarNav"] > ul {{
                padding-top: 0px;
            }}
            .css-17lntkn {{
                padding-top: 0px !important;
            }}
            .css-1544g2n {{
                padding-top: 0rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to extract attributes from PDF document using pdfplumber
def extract_attributes_from_pdf(file_path, selected_attributes, attribute_mappings):
    attributes = {}
    with pdfplumber.open(file_path) as pdf:
        first_page = pdf.pages[0]  # Assuming attributes are on the first page
        text = first_page.extract_text()
        for user_friendly_attribute in selected_attributes:
            possible_attribute_names = attribute_mappings[user_friendly_attribute]
            for attribute_name in possible_attribute_names:
                if attribute_name in text:
                    attribute_index = text.index(attribute_name)
                    end_index = text.find("\n", attribute_index)
                    attribute_value = text[attribute_index + len(attribute_name):end_index].strip()
                    # Store using the attribute name as it appears in the document
                    attributes[attribute_name] = attribute_value
                    break  
    return attributes

# Function to render PDF preview
def render_pdf_preview(file_path):
    images = convert_from_bytes(file_path.read(), size=(800, None))
    return images

# Function to convert image to PDF
def convert_image_to_pdf(image_data):
    pdf_bytes = io.BytesIO()
    image_data.save(pdf_bytes, format='PDF')
    pdf_bytes.seek(0)
    return pdf_bytes

# Function to load About page information from JSON file
def load_about_info(json_path):
    with open(json_path, 'r') as file:
        about_info = json.load(file)
    return about_info

def main():
    st.title("Smart Fill")

    tabs = st.tabs(["About", "Smartfill"])

    with tabs[1]:
        with st.sidebar.expander("Configuration:", expanded=True):
            attribute_mappings = {
                "Property": ["Property", "Property Address", "Address"],
                "Borrower(s)": ["Borrower", "Borrower(s)", "Applicant(s)"],
                "Seller(s)": ["Seller", "Seller(s)"],
                "Loan Amount": ["Loan Amount", "Amount"],
                "Loan Term": ["Loan Term", "Term"],
                "Lender": ["Lender", "Lender Name"],
                "Cash to Close": ["Cash to Close", "Closing Costs", "Cash Required"]
            }
            selected_attributes = st.multiselect("Select Attributes", list(attribute_mappings.keys()))
            if not selected_attributes:
                selected_attributes = list(attribute_mappings.keys())

        # File upload
        uploaded_file = st.file_uploader("Upload document", type=["pdf", "png", "jpg", "jpeg"])

        if uploaded_file:
            if uploaded_file.type in ['image/png', 'image/jpeg']:
                # Resize image
                image = Image.open(uploaded_file)
                image_resized = image.resize((800, 800))
                col1, col2 = st.columns(2)
                preview_clicked = col1.button("Preview")
                extract_clicked = col2.button("Extract Information")
                if extract_clicked:
                    col1.image(image_resized, use_column_width=True, caption="Page Preview")
                    pdf_data = convert_image_to_pdf(image_resized)
                    pdf_image = render_pdf_preview(pdf_data)
                    st.write("Image converted to PDF successfully!")
                    # Extract attributes from PDF document using pdfplumber
                    attributes = extract_attributes_from_pdf(pdf_data, selected_attributes, attribute_mappings)
                    if attributes:
                        for key, value in attributes.items():
                            col2.text_input(key, value)  
                    else:
                        st.info("No attributes identified.")
                elif preview_clicked:
                    col1.image(image_resized, use_column_width=True, caption="Page Preview")
            elif uploaded_file.type == 'application/pdf':
                col1, col2 = st.columns(2)
                preview_clicked = col1.button("Preview")
                extract_clicked = col2.button("Extract Information")
                if extract_clicked:
                    pdf_images = render_pdf_preview(uploaded_file)
                    for image in pdf_images:
                        col1.image(image, use_column_width=True, caption="Page Preview")
                    # Extract attributes from PDF document using pdfplumber
                    attributes = extract_attributes_from_pdf(uploaded_file, selected_attributes, attribute_mappings)
                    if attributes:
                        for key, value in attributes.items():
                            col2.text_input(key, value)  
                    else:
                        st.info("No attributes identified.")
                elif preview_clicked:
                    pdf_images = render_pdf_preview(uploaded_file)
                    for image in pdf_images:
                        col1.image(image, use_column_width=True, caption="Page Preview")

    with tabs[0]:
        st.header("About")
        about_info = load_about_info("Smart_fill_about_info.json")
        for section in about_info["sections"]:
            with st.expander(section["title"], expanded=True):
                st.write(section["content"])

if __name__ == "__main__":
    main()