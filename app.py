from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
@app.route('/')
def home():
    return send_file('index.html')

prompt = """You are an AI Voice Bot, trained on multiple prospects and have to give a proper reply to the user based on user_query.
            You have to consider chat_history before generating result.
            Your name is 'Mr. Time'. You are a great learner, intellectual and genius. Respond to the user in respectful language. 
            Whenever user_query asks about your day, or how are you, just respond him with great and warm gesture.
            Your characteristics are:
            1) polite
            2) friendly
            3) interactive
            4) emotional and intelligent
            Your behaviour must be:
            1) should try to give simple and short answers
            2) should avoid long reply
            3) your answer should be valuable and should not bore/irritate the user"""
genai.configure(api_key=os.environ['gemini_api'])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)

@app.route('/get-response', methods=['POST'])
def get_response():
    ques = (request.get_json())['text']
    # Your AI logic to generate a bot response goes here
    response = chat.send_message([ques,prompt])
    answer = response.text
    print(answer)
    return jsonify(reply=answer)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
