
# from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import fitz 
import io
import os
import base64
import json
from transformers import CLIPProcessor, CLIPModel

# Set the path to your logo image here
LOGO_PATH = "img/Theoremlabs_logo.png"  # Update this path as needed

# Load the page icon
page_icon = Image.open("pages/favicon.ico")

# Set page configuration
st.set_page_config(page_title="Document Detector", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")

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

# Function to load About page information from JSON file
def load_about_info(json_path):
    with open(json_path, 'r') as file:
        about_info = json.load(file)
    return about_info

# Function to convert PDF to image
def pdf_to_img(uploaded_file):
    pdf_data = uploaded_file.read()
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    first_page = pdf_document.load_page(0)
    pixmap = first_page.get_pixmap()
    img_bytes = pixmap.tobytes()
    image = Image.open(io.BytesIO(img_bytes))
    return image

# Function to perform image-to-text classification
def img2text(uploaded_file, options):
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")
    if isinstance(uploaded_file, Image.Image):
        image = uploaded_file
    else:
        image = Image.open(uploaded_file)

    array = ["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA", "1040-Tax-Return"]
    inputs = processor(text=array, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  
    probs = logits_per_image.softmax(dim=1)  

    probs = probs.tolist()
    flat_probs = [prob for sublist in probs for prob in sublist]
    max_prob = max(flat_probs)
    index_of_max = flat_probs.index(max_prob)
    messages = [
        "Your documents have been uploaded successfully. Thanks for submitting your Passport.",
        "Your documents have been uploaded successfully. Thanks for submitting your Driver License.",
        "Your documents have been uploaded successfully. Thanks for submitting your Green Card.",
        "Your documents have been uploaded successfully. Thanks for submitting your 401K Statement.",
        "Your documents have been uploaded successfully. Thanks for submitting your Will & POAs Document.",
        "Your documents have been uploaded successfully. Thanks for submitting your Life Insurance Policy.",
        "Your documents have been uploaded successfully. Thanks for submitting your W2 Form.",
        "Your documents have been uploaded successfully. Thanks for submitting your HSA Statement.",
        "Your documents have been uploaded successfully. Thanks for submitting your Income Statement Document."
    ]
    message = messages[index_of_max]
    styled_message = f"<div style='font-size:28px;font-weight:bold;border: 2px solid Green;padding:10px;'>{message}</div>"
    st.markdown(styled_message, unsafe_allow_html=True)
    st.subheader("The Probabilities are as follows")
    for i, option in enumerate(array):
        if option in options:
            st.write(f"{option} - {flat_probs[i]}")

def main():
    st.title("Document Detector")

    tabs = st.tabs(["About", "Document Detector"])

    with tabs[1]:
        with st.sidebar:
            st.header('Configuration')
            options = st.multiselect(
                label='Choose the Parameter to classify', 
                options=["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA", "1040-Tax-Return"]
            )

        uploaded_file = st.file_uploader("Choose a file to upload", type=['png', 'jpeg', 'jpg', 'pdf'])
        if uploaded_file is not None:
            if uploaded_file.type == 'application/pdf':
                uploaded_file = pdf_to_img(uploaded_file)
                st.image(uploaded_file, caption='Uploaded Document.', use_column_width=True)
                if st.button("Submit"):
                    img2text(uploaded_file, options)
            else:    
                st.image(uploaded_file, caption='Uploaded Document.', use_column_width=True)
                if st.button("Submit"):
                    img2text(uploaded_file, options)

    with tabs[0]:
        st.header("About")
        about_info = load_about_info("Document_Detector_about_info.json")
        for section in about_info["sections"]:
            with st.expander(section["title"], expanded=True):
                st.write(section["content"])

def create_static_directory():
    directory = 'static/'
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")

create_static_directory()

if __name__ == '__main__':
    main()