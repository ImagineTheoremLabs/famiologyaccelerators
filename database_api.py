from flask import Flask, jsonify, request
from transformers import pipeline
import mysql.connector

app = Flask(__name__)

# Initialize the Hugging Face conversational model
# chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

def connect_db():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Atharva$123',
        database='test'
    )
    return connection

@app.route('/get_data/<table_name>', methods=['GET'])
def get_data(table_name):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(result)

@app.route('/post-data', methods=['POST'])
def post_data():
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # Check if the required data is present
        if not data or 'user_input' not in data or 'uuid' not in data:
            return jsonify({'error': 'Missing data'}), 400

        user_input = data['user_input']

        # Use the user_input to interact with your model
        # response = chatbot(user_input)
        response= "hello"
        print("sending the response")
        # Check if the chatbot generated a response
        if response and len(response) > 0:
            bot_response = response #[0]['generated_text']
            return jsonify({'message': bot_response}), 200
        else:
            return jsonify({'message': 'No response generated from the bot.'}), 500
    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
