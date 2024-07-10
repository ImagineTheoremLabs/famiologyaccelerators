import streamlit as st
import base64
from PIL import Image
import io
import json
import os
import streamlit.components.v1 as components  # Ensure this import is included

# Load JSON content
with open("content.json", "r") as file:
    content = json.load(file)

# Load image function
def load_image(image_path):
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        st.error(f"Image file {image_path} not found.")
        return None

# Load the page icon
page_icon = load_image(content.get("page_icon"))

# Set page configuration as the first Streamlit command
if page_icon:
    st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
else:
    st.set_page_config(page_title="Famiology", layout="wide", initial_sidebar_state="expanded")

# Load CSS content
with open("styles.css", "r") as css_file:
    css_content = css_file.read()

# Apply CSS styles
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Load and display the sidebar logo
file_path = content.get("sidebar_logo")
if file_path:
    file = open(file_path, "rb")
    contents = file.read()
    img_str = base64.b64encode(contents).decode("utf-8")
    buffer = io.BytesIO()
    file.close()
    img_data = base64.b64decode(img_str)
    img = Image.open(io.BytesIO(img_data))
    resized_img = img.resize((300, 60))  # x, y
    resized_img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Apply the sidebar logo style
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Title, subheader, text
title = content.get('title')
subheader = content.get('subheader')
description = content.get('description')

if title or subheader or description:
    html = '<div style="text-align: center; color: white; padding: 20px;">'
    if title:
        html += f'<h1 style="font-weight: bold;">{title}</h1>'
    if subheader:
        html += f'<h2 style="font-weight: bold;">{subheader}</h2>'
    if description:
        html += f'<p>{description}</p>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# Central section with video or image
featured_video = content.get('featured_video')
if featured_video:
    st.markdown('<h2 style="text-align: center;">Featured Video</h2>', unsafe_allow_html=True)  # Center the heading
    if os.path.isfile(featured_video):
        # If it's a local file, use st.video() directly
        st.video(featured_video)
    else:
        # If it's a URL, use st.video() directly
        st.video(featured_video)

# Load accelerator data from JSON content
accelerators = content.get("accelerators", [])

# Calculate the height of the accelerator section based on the number of items
if accelerators:
    num_accelerators = len(accelerators)
    rows = (num_accelerators + 3) // 4  # Calculate number of rows needed
    base_height = 550  # Base height for one row
    additional_height_per_row = 500  # Additional height for each extra row
    total_height = base_height + (rows - 1) * additional_height_per_row

    # Featured accelerators section
    st.subheader("Explore Famiology Accelerators")

    # Create HTML for accelerator cards with a grid layout and hover effects
    accelerator_html = '''
    <style>
    .accelerator-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-top: 50px;
    }
    .accelerator-card {
        text-align: center;
        border-radius: 10px;
        padding: 20px;
        transition: all 0.3s ease;
        background-color: rgba(26, 32, 44, 0.4);  /* Darker, more transparent background */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);  /* Adds a slight blur effect */
    }
    .accelerator-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        background-color: rgba(26, 32, 44, 0.6);  /* Slightly more opaque on hover */
    }
    .accelerator-card img {
        width: 100%;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .accelerator-card:hover img {
        transform: scale(1.05);
    }
    .accelerator-card h3 {
        margin-top: 15px;
        font-weight: bold;
        color: #3498db;
    }
    .accelerator-card p {
        color: #ecf0f1;
    }
    .accelerator-card a {
        display: inline-block;
        margin-top: 10px;
        padding: 5px 10px;
        background-color: #3498db;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }
    .accelerator-card a:hover {
        background-color: #2980b9;
    }
    </style>
    <div class="accelerator-grid">
    '''

    for acc in accelerators:
        img = load_image(acc['image'])
        if img:
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            accelerator_html += f"""
            <div class="accelerator-card">
                <img src="data:image/png;base64,{img_b64}" alt="{acc['title']}">
                <h3>{acc['title']}</h3>
                <p>{acc['description']}</p>
                <a href="{acc['link']}" target="_blank">Learn More</a>
            </div>
            """

    accelerator_html += '</div>'
    components.html(accelerator_html, height=total_height)