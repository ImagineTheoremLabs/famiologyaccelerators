import streamlit as st

st.sidebar.selectbox('Apps', options=['Document Detector', 'Smart Fill'], index=0)

def main():
    with st.sidebar():
        st.markdown('<a href="https://famiologydocdetector.streamlit.app/" target="_self">Document Detector</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()


    
