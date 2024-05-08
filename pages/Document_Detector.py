# import streamlit as st
# def main():
#     st.markdown("<a href='https://famiologydocdetector.streamlit.app/' target='_blank'>Go to Document Detector Website</a>", unsafe_allow_html=True)

# if __name__ == "__main__":
#      main()


import streamlit as st
from PIL import Image

def main():
    page_icon = Image.open("pages/favicon.ico")
    st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
    logo = Image.open("pages/favicon.ico")

    # Streamlit UI
    st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 400px !important; # Set the width to your desired value
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                outline: none;
                color: #fff;
                background-color: #007bff;
                border: none;
                border-radius: 15px;
                box-shadow: 0 9px #0069d9;
            }
            .button:hover {background-color: #0069d9}
            .button:active {
                background-color: #0069d9;
                box-shadow: 0 5px #666;
                transform: translateY(4px);
            }
        </style>
        """,
    unsafe_allow_html=True,
    )

    #with st.sidebar.container():
        # Section 1: Apps
    #with st.expander("Apps"):
    if st.button("<a href='https://famiologydocdetector.streamlit.app/' target='_blank' class='button'>Document Detector</a>", unsafe_allow_html=True)
            #st.markdown("<a href='https://famiologydocdetector.streamlit.app/' target='_blank' class='button'>Go to Document Detector Website</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
