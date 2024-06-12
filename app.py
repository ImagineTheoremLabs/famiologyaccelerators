import streamlit as st
from PIL import Image

page_icon = Image.open("pages/favicon.ico")
st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
logo = Image.open("pages/favicon.ico")

# Streamlit UI
file = open("FamiologyTextLogo.png", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((400, 100))  # x, y
resized_img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

# st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
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




