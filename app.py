# import streamlit as st
# from PIL import Image

# page_icon = Image.open("pages/favicon.ico")
# st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
# logo = Image.open("pages/favicon.ico")

# # Streamlit UI
# st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

# st.markdown(
#     """
#     <style>
#         section[data-testid="stSidebar"] {
#             width: 400px !important; # Set the width to your desired value
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# def main():
#     with st.sidebar.container():
#         # Section 1: Apps
#         with st.expander("Apps"):
#             st.markdown('<a href="https://famiologydocdetector.streamlit.app/" target="_self">Document Detector</a>', unsafe_allow_html=True)
#             st.markdown('<a href="https://famiology-smart-fill.streamlit.app/" target="_self">Smart Fill</a>', unsafe_allow_html=True)
        

# if __name__ == "__main__":
#     main()




import streamlit as st
from PIL import Image

def document_detector():
    st.title("Document Detector Page")
if st.button("Click here to visit the document detector website"):
        # Redirect to the provided link
        st.markdown("[Document Detector Website](https://famiologydocdetector.streamlit.app/)")
def main():
    page_icon = Image.open("pages/favicon.ico")
    #st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
    logo = Image.open("pages/favicon.ico")

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
with st.sidebar.container():
        # Section 1: Apps
        with st.expander("Apps"):
            if st.button("Document Detector"):
                document_detector()
            if st.button("Smart Fill"):
                st.markdown("[Smart Fill Website](https://famiology-smart-fill.streamlit.app/)")

if __name__ == "__main__":
    main()
