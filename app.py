import streamlit as st
from PIL import Image

page_icon = Image.open("./favicon.ico")
st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
logo = Image.open("./favicon.ico")

# Streamlit UI
st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

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



def main():
    with st.sidebar.container():
        # Section 1: Apps
        with st.expander("Apps"):
            st.markdown('<a href="https://famiologydocdetector.streamlit.app/" target="_self">Document Detector</a>', unsafe_allow_html=True)
            st.markdown('<a href="https://famiology-smart-fill.streamlit.app/" target="_self">Smart Fill</a>', unsafe_allow_html=True)
        

if __name__ == "__main__":
    main()
