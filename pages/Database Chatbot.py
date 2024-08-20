
import streamlit as st
from transformers import pipeline, Conversation
import pandas as pd
import requests
import uuid  # Import UUID library

CORRECT_USERNAME = 'root'
CORRECT_PASSWORD = 'Atharva$123'

# Initialize the Hugging Face conversational model
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

st.set_page_config(page_title="Database Chatbot", layout="wide")

def main():
    # Custom CSS for chat UI
    st.markdown("""
        <style>
        .user-input {
            text-align: right;
            color: white;
            background-color: #1f77b4;
            padding: 8px 16px;
            border-radius: 25px;
            max-width: 60%;
            margin-left: auto;
            margin-right: 10px;
        }
        .bot-response {
            text-align: left;
            color: black;
            background-color: #e2e2e2;
            padding: 8px 16px;
            border-radius: 25px;
            max-width: 60%;
            margin-right: auto;
            margin-left: 10px;
        }
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f5f5f5;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display the logo in the sidebar with adjusted size
    image_path = "/Users/atharvabapat/Desktop/Theoremlabs-project/Database-Chatbot/Theoremlabs_logo.png"
    st.sidebar.image(image_path, use_column_width=True)

    # Check if the database is connected
    if "connected" not in st.session_state:
        st.session_state.connected = False

    # Main content area with increased width
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Dynamically create the tabs based on the connection status
        if st.session_state.connected:
            tabs = st.tabs(["About", "Database Connection", "Database Chatbot"])
        else:
            tabs = st.tabs(["About", "Database Connection"])

        with tabs[0]:
            st.markdown("""
             <h2>About</h2>
            <p>This advanced chatbot simplifies database interaction, allowing you to ask questions in natural language and receive answers in human-readable or table formats. No need for complex query languages—just connect your database and start querying.</p>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        with tabs[1]:
            with st.form("database_form"):
                st.write("Please select your preferred database:")

                # Radio button to select between Oracle and MySQL
                database_choice = st.radio(
                    "LIST OF DATABASES THAT WE CAN CONNECT: ",
                    ("SELECT A DATABASE", "MySQL", "Oracle")
                )
                username = None
                password = None

                if database_choice == "MySQL":
                    # Input fields for username and password when MySQL is selected
                    username = st.text_input("MySQL Username")
                    password = st.text_input("MySQL Password", type="password")

                submitted = st.form_submit_button("Submit")

                if submitted:
                    if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
                        st.success("Connected to MySQL database!")
                        st.session_state.connected = True
                        st.rerun()  # Rerun the app to create the "Database Chatbot" tab
                    else:
                        st.error("Invalid MySQL credentials. Please try again.")
                        st.session_state.connected = False

                    if database_choice == "Oracle":
                        st.write("ORACLE NOT YET IMPLEMENTED.")
                        st.session_state.connected = False
            if st.session_state.connected:
                # Add a text input for table name and a button to fetch data
                table_name = st.text_input("Enter the table name to fetch data", "")
                if st.button("Fetch Data"):
                    if table_name:
                        # Call the Flask API to get data
                        response = requests.get(f"http://127.0.0.1:5000/get_data/{table_name}")
                        if response.status_code == 200:
                            data = response.json()
                            df = pd.DataFrame(data)
                            st.write(df)
                        else:
                            st.error("Failed to fetch data. Please check the table name or Flask API.")
        
        if st.session_state.connected:
            with tabs[2]:
                st.markdown("## Database Chatbot")
                st.subheader("Let's chat with the connected database")

                # Initialize conversation history
                if "conversation_history" not in st.session_state:
                    st.session_state.conversation_history = []

                # Chat container
                
                # Get user input
                user_input = st.text_input("You:", "")
                if st.button("Send"):
                    if user_input:
                        # Generate a UUID for the conversation
                        user_uuid = str(uuid.uuid4())

                        # Add user input to conversation history
                        st.session_state.conversation_history.append({"user": True, "message": user_input})

                        # Send the user input and UUID to the Flask API via POST request
                        data = {'user_input': user_input, 'uuid': user_uuid}
                        response = requests.post('http://127.0.0.1:5000/post-data', json=data)

                        if response.status_code == 200:
                            bot_response = response.json().get('message', 'Bot did not reply')
                            if bot_response:
                                print("bot got message from server.")
                                st.session_state.conversation_history.append({"user": False, "message": bot_response})
                            else:
                                st.error('Bot did not generate a response.')
                        else:
                            st.write("Reponse.json", response.json())
                            st.error(f'Failed to get a response from the bot: {response.json().get("error", "Unknown error")}')
                            if "details" in response.json():
                                st.error(f'Details: {response.json()["details"]}')
                                
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for message in st.session_state.conversation_history:
                    if message["user"]:
                        st.markdown(f'<div class="user-input">{message["message"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="bot-response">{message["message"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
