import argparse
import re
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
import time
from fetchTableInfo import returnTables
from dbhelper_tester import getSQLQueryFromModel
from sdvDataGen import generateDataForTable
from DB_init.sqlite_databasefinder import returnAvailabledatabases

model = Ollama(model="llama3")

last_userInput = ""
def botResponse(user_input):


    
    nlu_prompt = """You are a Natural Language Understanding Unit, where depending upon the user you analyze the task and then give me action number to take.
        You are Natural language language understanding unit for Database chatbot which performs some actions depending upon the user requests.
        Here are the actions which I want to perform
        0. User is just initiating the conversation with greetings, such as Hi Hello etc, action label is ACTION_GREET. If this is the action label, then greet back and return the action label as well as greeting, and return the greeting with the starting label GREET_BACK dont add any thing after this.
        1. User can ask which databases the program has connections or similar questions, action label is ACTION_CONNECTIONS, Every time user asks this you have to respond in this manner only. 
        2. User can ask which database it wants to use now, action label you should return is ACTION_USEDB, The words from user can be 'use this database' with the name followed by it, return the databse name that user wants to use with the starting label as DATABASE_TO_USE followed by database name enclosed in curly brackets.
        3. User could ask in natural language to return the data from the database, that us Data Query language only, Remember that only to take this action label when user wants to show the data and not for database modification queries. action label is ACTION_DQL.
        4. User can ask to create/generate/populate additional any number of rows to particular database, then use this action item, action label is ACTION_GENDATA, and return the table name for which user wants to generate the data by lable TABLE_NAME_DATA_GEN start the name with = and terminate the name with |.
        5. User can ask to perform some sql queries other than Data Query Language, then return this action item, action label is ACTION_MANIPULATION.
        6. User can refer to the earlier message and response to that message, earlier message sent by the bot is Given as the CHATBOT_HISTORY. Then user action label ACTION_REFHISTORY.
        7. User can say something which does not fit in any category up above then return action label ACTION_NOTSPEC.
        you have to return action label
        """
    
    DATABASE_SCHEMA = "DATABASE :- famiology_dataset, Tables :- "
    # print("Gwriting the tables")
    tables = returnTables()
    database_connections = returnAvailabledatabases()

    keys_list = list(database_connections.keys())

    print("tables", tables)
    
    DATABASE_SCHEMA += ", ".join(keys_list)
    start_time = time.time()
    response_text = model.invoke("These are the available databases = "+ DATABASE_SCHEMA + " | " + nlu_prompt + "\n\nUser Input :- " + user_input)
    end_time = time.time()

    columnOfTable = []
    rowsOfTable = []
    response_ans = ""

    if response_text.find("ACTION_GREET") != -1:
        result = response_text.split("GREET_BACK")[-1].strip()

        # Further split on '=' to isolate the content
        result = result.split('=', 1)[-1].strip()

        response_ans = result
    if response_text.find("ACTION_CONNECTIONS") != -1:

        # Need to return the database and its connections 
        print("ACTION_CONNECTIONS")
        
        response = model.invoke("Available database connections = "+ DATABASE_SCHEMA + " | " + "These are the databases present Now user wants which databases are present and we can connect to, humanize the answer. "  + user_input)
        response_ans = response
        # print("bot Response", response)
    if response_text.find("ACTION_USEDB") != -1:
        match = re.search(r'\{(.*?)\}', response_text)

        if match:
            result = match.group(1)
            print("Used Database is ", result)
            response_ans = result
        # response_ans = response_text
    if response_text.find("ACTION_DQL") != -1:
        print("ACTION_DQL")
        responseResult = getSQLQueryFromModel(user_input, True)
        print("responseResult", responseResult)
        response_ans = "Heres the table"
        columnOfTable = responseResult["COLUMN"]
        rowsOfTable = responseResult["Result"]
        for row in rowsOfTable:
            # print("row", type(row))
            print(row)
            # print(row)
        # CALL TO SQLCODER MODEL
        
        
    if response_text.find("ACTION_MANIPULATION") != -1:
        print("ACTION_MANIPULATION")
        response_ans = getSQLQueryFromModel(user_input, False)
        print("sql_command", response_ans)
        # CALL TO SQLCODER MODEL
    if response_text.find("ACTION_GENDATA") != -1:
        #call gen data
        print("inside gen data")
        action_label = "TABLE_NAME_DATA_GEN: client_profile|"
        table_name = response_text.split('=')[-1].split('|')[0].strip()

        print("table_name", table_name)
        response_ans = "Here is the generated data"
        rowsOfTable = generateDataForTable(table_name)
        # print("rowsOfTable", rowsOfTable)
        columnOfTable = ['ID', 'FirstName', 'LastName', 'BirthDate', 'Email', 'MaritalStatus', 'Children', 'Address', 'State', 'Occupation', 'AnnualIncome', 'FinancialGoals', 'ClientStatus', 'Gender']
        

    if response_text.find("ACTION_NOTSPEC") != -1:
        responseResult = getSQLQueryFromModel(user_input, True)
        if responseResult is not False:
            if len(responseResult["Result"]) > 1:
                for row in responseResult["Result"]:
                    print(row)
                columnOfTable = responseResult["COLUMN"]
                rowsOfTable = responseResult["Result"]
                response_ans = "Here is the required data."
            else:
                print("responseResult", responseResult)

                response_db = ", ".join(responseResult["Result"][0])
                
                response_ans = model.invoke("This is the answer fetched from the database for the question user asked :- "+ response_db + " Now answer this question in well formatted way, the user just wants the short answer, and you are directly answering user so dont add unnecessary messages. Following is the user's question :- " + user_input)
                print("response", response)
        else:
            print("ACTION_NOTSPEC")
            print("Can you please repeat the question ?")
            response_ans = "Can you please repeat the question/requirement ?"

    print("\nBot :- ", response_text)
    print("\nTime took ", end_time - start_time, "\n-------------------------------------------------------------------------------\n-------------------------------------------------------------------------------\n")
    last_userInput = user_input
    botResponse_data = { "COLUMN_NAME" : columnOfTable,  "ROWS" : rowsOfTable,  "RESPONSE_ANS" : response_ans, "isTable": True if len(columnOfTable) > 0 else False}
    # print("botResponse_data", botResponse_data)
    return botResponse_data

# while 3<4:
#     user_input = input("USER INPUT\n")
#     botResponse_data = botResponse(user_input)
#     print("botResponse_data", botResponse_data)
