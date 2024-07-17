import streamlit as st
import pandas as pd
import os
import shutil
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function
import google.generativeai as genai
import time
import json
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI


from few_shots import few_shots 
from populateData_gpt import InitializeTempSqliteDatabase

import sqlite3

GOOGLE_API_KEY="AIzaSyAgOpTjsMjAlH_llHLrXq-MbXPl8fiOa3Q"
genai.configure(api_key=GOOGLE_API_KEY)
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'

st.session_state.model = genai.GenerativeModel('gemini-pro')
st.session_state.chat = st.session_state.model.start_chat()

# Constants
CHROMA_PATHS = {
    "Excel": "chroma_excel",
    "JSON": "chroma_json",
    "SQLite": "chroma_db_directory"
}

DATA_PATH = "data"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Helper functions
def load_excel(file):
    xls = pd.ExcelFile(file)
    return xls

def clear_database(chroma_path):
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)

def add_to_chroma(chunks, chroma_path):
    db = Chroma(persist_directory=chroma_path, embedding_function=get_embedding_function())
    chunks_with_ids = calculate_chunk_ids(chunks)
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
        st.write(f"👉 Added new documents: {len(new_chunks)}")
    else:
        st.write("✅ No new documents to add")

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source", "None")
        page = chunk.metadata.get("page", "None")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk.metadata["id"] = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

    return chunks

def query_llm(prompt):
    model = Ollama(model="llama2")
    response_text = model.invoke(prompt)
    return response_text

def query_rag(query_text, chroma_path, conversation_history):
    db = Chroma(persist_directory=chroma_path, embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    additional_info = """You are a learning bot and you task is to understand and learn every aspect of the data that's given to you in the xlsx file.
    you must learn all the client names and attach it to the client ID to answer questions asked of you.
    each client first name and last name is corresponded to the specific client ID. where 'First Name' column corresponds to first name of the client and 'Last Name' column corresponds to last name of the client.
    A full name of the client is first name consequently followed by its last name. or also can also me mentioned by last name consequently followed by first name. Consider it is that client only
    each client address is corresponding to each client ID.
    each client date of birth is corresponding to each client ID.
    each client contact information is corresponding to each client ID.
    each client marital status is corresponding to each client ID.
    each client dependents is corresponding to each client ID.
    each client state is corresponding to each client ID.
    each client profession is corresponding to each client ID.
    each client networth is corresponding to each client ID.
    each client profession is corresponding to each client ID.
    each client financial goal is corresponding to each client ID.
    Age for a particular client is the difference between current year (2024) and birth year from date of birth.
    A clientID represents information about unique client in the sheet 'client Profile'
    sheet name 'Family members' and 'client profile' are linked with one another where clientID is the foreign key.
    In sheet 'Family members' information is given regarding clients from sheet 'client Profile'.
    Rows in the 'Family members' which have the same clientID as to the clinedID column  to the 'Client Profile' sheet, then in that case that row in 'Family Members' gives additional information regarding about the clinet with that clientID in the 'Client Profile'.
    Dont answer beyound the context provided."""
    complete_query = additional_info + query_text
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    # Add conversation history
    full_prompt = "\n\n".join(conversation_history + [prompt])
    
    response_text = query_llm(full_prompt)
    return response_text

# Streamlit UI
st.title("LLM AI Bot with Excel Data")

# Move upload part to the main section
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if st.button("Reset Database"):
    chroma_path = st.session_state.get('chroma_path', 'chroma_excel')
    clear_database(chroma_path)
    st.write("Database reset complete.")

if uploaded_file is not None:
    # Load and display the Excel file
    xls = load_excel(uploaded_file)
    sheet_names = xls.sheet_names

    # Add a column layout to place the sheet selector next to the "Excel Data" title
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("### Excel Data")
    with col2:
        sheet_select = st.selectbox("Select Sheet", sheet_names, label_visibility="collapsed")

    df = pd.read_excel(xls, sheet_name=sheet_select)

    # Add a container to make the table sticky
    st.markdown(
        """
        <style>
        .sticky-table-container {
            position: -webkit-sticky;
            position: sticky;
            top: 0;
            background: white;
            z-index: 100;
        }
        .sticky-table-container table {
            margin-top: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.write('<div class="sticky-table-container">', unsafe_allow_html=True)
    st.dataframe(df)
    st.write('</div>', unsafe_allow_html=True)

    # Convert DataFrame to Documents
    documents = [Document(page_content=" | ".join(map(str, row))) for row in df.values]
    chunks = documents  # Assuming each row is a chunk for simplicity

    chroma_path = CHROMA_PATHS["Excel"]
    add_to_chroma(chunks, chroma_path)
    print("Excel Uploaded and No initializing the data")
    InitializeTempSqliteDatabase(xls)
    
    def convert_excel_to_json(xls, json_file_path):
        # Load the entire Excel file
        # xls = pd.ExcelFile(excel_file_path)
        # Load the data from each sheet into a dictionary
        client_profile_df = pd.read_excel(xls, sheet_name='Client Profile')
        family_members_df = pd.read_excel(xls, sheet_name='Family Members')
        # Ensure that date fields are converted to strings
        client_profile_df['Date of Birth'] = client_profile_df['Date of Birth'].astype(str)
        family_members_df['Date of Birth'] = family_members_df['Date of Birth'].astype(str)
        # Process client profile data
        clients = []
        for index, row in client_profile_df.iterrows():
            client = {
            "ClientID": row["ClientID"],
            "First Name": row["First Name"].strip(),
            "Last Name": row["Last Name"].strip(),
            "Date of Birth": row["Date of Birth"],
            "Contact Information": row["Contact Information"].strip(),
            "Marital Status": row["Marital Status"].strip(),
            "Dependents": row["Dependents"],
            "Address": row["Address"].strip(),
            "State": row["State"].strip(),
            "Profession": row["Profession"].strip(),
            "Net Worth": row["Net Worth"],
            "Financial Goals": row["Financial Goals"].strip(),
            "Status": row["Status"].strip(),
            "Family Members": []
            }
            # Add family members to the client
            family_members = family_members_df[family_members_df["ClientID"] == row["ClientID"]]
            for _, family_row in family_members.iterrows():
                family_member = {
                "FamilyMemberID": family_row["FamilyMemberID"].strip(),
                "Relationship": family_row["Relationship"].strip(),
                "First Name": family_row["First Name"].strip(),
                "Last Name": family_row["Last Name"].strip(),
                "Date of Birth": family_row["Date of Birth"],
                "Contact Information": family_row["Contact Information"].strip()
                }
                client["Family Members"].append(family_member)
            clients.append(client)
        # Write to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(clients, json_file, ensure_ascii=False, indent=4)
        return json_file_path


    convert_excel_to_json(xls, "data/uploadedData.json")

    def split_documents(documents: list[Document], chunk_size=5): #updated so that it splits docs and groups every 'chunk_size' doc together
        chunks = []
        for i in range(0, len(documents), chunk_size):
            chunk_documents = documents[i:i+chunk_size]
            chunks.extend(chunk_documents)

        return chunks

    def addJsonToDB(chroma_path):
        documents = []

        json_file_path = os.path.join("data", 'uploadedData.json')  # Replace with your JSON file name
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                for item in json_data:
                    json_string = json.dumps(item)

                    print(json_string)

                    # metadata = {key: value for key, value in item.items() if key != 'content'}


                    metadata = {
                        "ClientID": str(item["ClientID"]).strip(),
                        "First Name": item["First Name"].strip(),
                        "Last Name": item["Last Name"].strip()
                    }               
                    print("metadata", metadata)
                    documents.append(Document(page_content=json_string, metadata=metadata))
            chunks = split_documents(documents)
            add_to_chroma(chunks, chroma_path)

    chroma_path = CHROMA_PATHS["JSON"]
    addJsonToDB(chroma_path)

    # Add radio buttons for selecting approach
    approach = st.radio("Select Data Processing Approach",  ["Excel", "JSON", "SQLite", "Gemini"], horizontal=True,)
    if approach == "Gemini":
        user_input = st.chat_input("Enter your question here")
        if user_input:
            st.session_state.conversation_history.append(f"User: {user_input}")

            file_path = 'data/Client_Family_Data_Combined.json'

            with open(file_path, 'r') as file:
                json_string = file.read()
                json_object = json.loads(json_string)
                prompt =  str(json_object[0]) + "  " + " Performa all the operations and find out the answer to the question. Current date is 19th June 2024. Directly give the answer dont explain the answer unless explicityly asked for it. " + " " + user_input
            print("prompt", prompt)
            ## Send message to AI
            response = st.session_state.chat.send_message(
                prompt,
                stream=True,
            )
            print("this is the response for the message", response)
            full_response = ''
            assistant_response = response
            # Streams in a chunk at a time
            for chunk in response:
                # Simulate stream of chunk
                # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
                for ch in chunk.text.split(' '):
                    print("chat in ch", ch)
                    full_response += ch + ' '
                    # time.sleep(0.05)
                    # Rewrites with a cursor at end
            st.session_state.conversation_history.append(f"Bot: {full_response}")
        st.write("### Conversation History")
        for i, message in enumerate(st.session_state.conversation_history):
            role = "assistant" if "Bot:" in message else "user"
            with st.chat_message(role):
                st.write(message)



    elif approach == "SQLite":
        user_input = st.chat_input("Enter your question here")
        if user_input:
            st.session_state.conversation_history.append(f"User: {user_input}")


            def getInformationFromDBLangchain(question, prompt_text):
                db = SQLDatabase.from_uri(f"sqlite:///data/database.db", sample_rows_in_table_info=3)
                # print(db.table_info)
                llm = Ollama(model="llama3")

                db_chain = SQLDatabaseChain.from_llm(llm, db)
                qns1 = ""

                to_vectorize = [" ".join(example.values()) for example in few_shots]

                embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

                vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

                example_selector = SemanticSimilarityExampleSelector(
                vectorstore=vectorstore,
                k=2,
                )

                from langchain.prompts.prompt import PromptTemplate
                from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt

                example_prompt = PromptTemplate(
                input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
                template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
                )

                few_shot_prompt = FewShotPromptTemplate(
                example_selector = example_selector,
                example_prompt=example_prompt,
                suffix=PROMPT_SUFFIX,
                input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
                )

                # db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt, return_direct=True)
                llm_gemini = ChatGoogleGenerativeAI(model="gemini-pro")

                db_chain = SQLDatabaseChain.from_llm(llm_gemini, db, verbose=True, prompt=few_shot_prompt, return_direct=True)
                qns1 = db_chain(question)

                print("qns1", qns1)

                prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
                sqlResults = json.dumps(qns1['result'])

                print("sqlResults", sqlResults)

                prompt = prompt_template.format(context=sqlResults + " This is the raw data I have, now perform any appropriate operation needed and give me answer to this question. Dont explain me the steps just give me the answers" , question=question)

                model = Ollama(model="llama3")

                response_text = model.invoke(prompt)

                print("response_text", response_text)
                return response_text

            promptInfoRegardingTheDB = [f"""This is the schema type of the database
        For table Client_Profile
        Client_Profile (ClientID INTEGER, First_Name TEXT, Last_Name TEXT, Date_of_Birth TEXT, Contact_Information TEXT, Marital_Status TEXT, Dependents INTEGER, Address TEXT, State TEXT, Profession TEXT, Net_Worth INTEGER, Financial_Goals TEXT, Status TEXT, Gender TEXT)
        'ClientID' is an primary key in table Client_Profile.

        Every Row in the Client_Profile table give information about the client
        Explaination of every Column in Client_Profile.
        ClientID - Unique Client ID of a Client.
        First_Name - First name of the Client in text format.
        Last_Name - Last name of the Client in text format.
        Date_of_Birth - Date of Birth of the Client in text format.
        Contact_Information - Contact_Information of the client which is an Email ID in text format.
        Marital_Status - Marital Status of the client where 'Married' means the client is married, 'Single' Means the CLient is single, 'Divorced' means Client is divorced in text format..
        Dependents - Number of dependents the client has, these are mainly Family members in the integer format.
        Address - Address of the client in text format..
        State - State of residence of the client in text format.
        Profession - Profession of the Client in text format.
        Net_Worth - Net Worth, that is earning of the client in the integer format.
        Financial_Goals - Financial Goals of the client where this states about the future goals client wants to pursue in text format..
        Status - This gives information about loyalty of the client in text format.
        Gender - Gender of the client, 'M' Being Male 'F' being Female in text format.


        for Table Family_Members
        Family_Members (FamilyMemberID TEXT, ClientID INTEGER, Relationship TEXT, First_Name TEXT, Last_Name TEXT, Date_of_Birth TEXT, Contact_Information TEXT);
        where ClientID is the Foreign Key from the Table Client_Profile.
        where each record in the Family_Members table gives additional information regarding the client associated with it by CientID.

        Every Row in the Family_Members table give information about the family members ofthe clients in the Client_Profile table.
        Explaination of every Column in Family_Members.

        FamilyMemberID -  Unique Family Member ID of a dependent.
        ClientID - Foreign key which connects with the Client_Profile table where this row gives information about the dependent of the client having this client_ID
        Relationship - Relationship of the CLient and the family member in text format.
        First_Name - First name of the Family Member in text format.
        Last_Name - Last name of the Family Member in text format.
        Date_of_Birth - Date of Birth of the Family Member in text format.
        Contact_Information - Contact_Information of the Family Member which is an Email ID in text format.


        I am using sqlite3 database for the given question.
        Consider that there can be spelling mistakes involved in the questions regarding the name of the facutal data present 
        so consider that and give me a command for this.
        Dont add additional text just give me commands.
        usually when user asks question it mentions name in a format such as First Name and Last Name.
        Try to add all the conditions in the command so that it wont give the incorrect data.

        convert the question into the actions which can be performed on the database depending on the information present in all the tables in the database.

        dont add newline character in the response.

        Just directly give me the string that I can Directly apply on the sqlite3 database.
        Dont give ` symbol on the start and end of the string, just directly give me command which I can process on the sqlite database. and remove the new lines from the output as well.
        
        Below are some examples of question and respective sql Queries
                                
        While comparing texts in the query do trim the spaces and comapre in lower case to avoid indiscripencies.
        
        """]
    
            sqlExamples = ""
            for ele in few_shots:
                sqlExamples += "\n\n Question = " + ele['Question'] + " \nSQL Query : " + ele['SQLQuery'] + "\n"
            print("sqlExamples", sqlExamples)
            promptInfoRegardingTheDB += sqlExamples

            promptInfoRegardingTheDB_old = """This is the schema type of the database
            For table Client_Profile
            Client_Profile (ClientID INTEGER, First_Name TEXT, Last_Name TEXT, Date_of_Birth TEXT, Contact_Information TEXT, Marital_Status TEXT, Dependents INTEGER, Address TEXT, State TEXT, Profession TEXT, Net_Worth INTEGER, Financial_Goals TEXT, Status TEXT, Gender TEXT)
            'ClientID' is an primary key in table Client_Profile.
    
            for Table Family_Members
            Family_Members (FamilyMemberID TEXT, ClientID REAL, Relationship TEXT, First_Name TEXT, Last_Name TEXT, Date_of_Birth TEXT, Contact_Information TEXT);
            where ClientID is the Foreign Key from the Table Client_Profile.
            where each record in the Family_Members table gives additional information regarding the client associated with it by CientID.
    
    
            I am using sqlite3 database for the given question.
            Consider that there can be spelling mistakes involved in the questions regarding the name of the facutal data present 
            so consider that and give me a command for this.
            Dont add additional text just give me commands.
            usually when user asks question it mentions name in a format such as First Name and Last Name.
            Try to add all the conditions in the command so that it wont give the incorrect data.
    
    
    
            Sample example for the record in  Client_Profile
            1	Alok	Desai	8/15/75	alok.desai@email.com	Married	3	123 Main St.	North Carolina	Entrepreneur	$2,500,000 	Save for children's education, retire at 60	Client.Active	M
    
            1 is the ClientIF
            where Alok is the first name and Desai is the last Name.
            Date Of Birth is 15th August 1975.
            alok.desai@email.com is the Contact_Information, that is mail ID.
            Married is the Marital_Status.
            there are 3 Dependents.
            123 Main St. is the address.
            North Carolina is the state.
            Entrepreneur is the profession.
            $2,500,000 is the Net_Worth.
            Save for children's education, retire at 60 is the Financial Goal.
            Client.Active is the status.
            'M' that is Male as a Gender, that is using 'M' for Male and 'F' for Female. Dont use Female as the gender term.
            
            use 'M' for male and 'F' for Female.
    
    
            Sample Row in the table Family_Members
            Fam-001	1	Self	Alok	Desai	8/15/75	alok.desai@email.com
    
            Where
            Fam-001 is the FamilyMemberID for that record in the table
            1 is the ClientID for that record in the table, so this record is associated with the client with ClientID 1
            Self is the Relationship that record has with the client. (Self suggests that this is the the record is the client it self, 
            Spouse suggests that the record is the spouse of the client mentioned with the ClientID, 
            Child suggests that the record is child of the client mentioned with the ClientID)
            Alok First_Name for that record in the table
            Desai Last_Name for that record in the table
            15th August 1975 is the  date of birth for that record in the table
            alok.desai@email.com is the contact information that is email-ID for that record in the table
    
    
            convert the question into the actions which can be performed on the database depending on the information present in all the tables in the database.
    
            dont add newline character in the response.
    
            Just directly give me the string that I can Directly apply on the sqlite database.
            Dont give ` symbol on the start and end of the string, just directly give me command which I can process on the sqlite database.
            
            """

            def get_gemini_response(question, prompt):
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content([prompt[0], question])
                return response.text

            response_sqlQuery = get_gemini_response(user_input, promptInfoRegardingTheDB)

            # print("sql query with response", response)

            def getDataFromDatabase(command: str):
                import sqlite3

                # Connect to the SQLite database
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()



                print("Applying commands on the db", command)
                # Execute the query
                cursor.execute(command)
                column_names = [description[0] for description in cursor.description]

                # Fetch and print the results
                results = cursor.fetchall()
                for row in results:
                    print(row)
                conn.close()

                return column_names, results

                # Close the connection

            responseDataFromTheDB = getDataFromDatabase(response_sqlQuery)

            print("responseDataFromTheDB", responseDataFromTheDB)

            ColumnsSepByComma = ', '.join(responseDataFromTheDB[0])
            SqlResult = json.dumps(responseDataFromTheDB[1])

            print("ColumnsSepByComma, SqlResult", ColumnsSepByComma, SqlResult)
            # response = get_gemini_response(user_input + "Answer the question keeping in mind that this sql query we used to caluculate the required value/ values " + response_sqlQuery + ". Providing the data that we have fetched from the database performing sql query. The data may have the Anser directly please use the columns specified accordingly", " Columns in the data are " + ColumnsSepByComma + " = " + SqlResult)
            response = get_gemini_response("Question = " + user_input + "Answer the question based on the data provided only and dont hallucinat and dont enhance or reduce the data show the complete result. Data to get answer might be present here. The data contains data of type " + ColumnsSepByComma + ". Data is = " + SqlResult, "Answer the question keeping in mind that this sql query we used to caluculate the required value/ values " + response_sqlQuery + ". Providing the data that we have fetched from the database performing sql query")


            # response = getInformationFromDBLangchain(user_input, promptInfoRegardingTheDB)
            st.session_state.conversation_history.append(f"Bot: {response}")

        # Display conversation history
        st.write("### Conversation History")
        for i, message in enumerate(st.session_state.conversation_history):
            role = "assistant" if "Bot:" in message else "user"
            with st.chat_message(role):
                st.write(message)
    
    else:
        chroma_path = CHROMA_PATHS[approach]
        st.session_state['chroma_path'] = chroma_path

        # Add to Chroma
        # add_to_chroma(chunks, chroma_path)
        st.write("Data has been added to the database.")

        # Initialize conversation history in session state
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []

        # Form to handle Enter key for submission
        user_input = st.chat_input("Enter your question here")
        if user_input:
            st.session_state.conversation_history.append(f"User: {user_input}")
            response = query_rag(user_input, chroma_path, st.session_state.conversation_history)
            st.session_state.conversation_history.append(f"Bot: {response}")

        # Display conversation history
        st.write("### Conversation History")
        for i, message in enumerate(st.session_state.conversation_history):
            role = "assistant" if "Bot:" in message else "user"
            with st.chat_message(role):
                st.write(message)
else:
    st.write("Please upload an Excel file to proceed.")

