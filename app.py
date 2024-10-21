from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import pyttsx3
from dotenv import load_dotenv
import speech_recognition as sr
load_dotenv()
engine = pyttsx3.init()
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
def voice_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for user query... Please Speak.")
        # Capture the audio from the microphone
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            # Recognize the speech using Google's free service
            print("Processing speech...")
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
        except sr.UnknownValueError:
            text = ("Sorry, I could not understand the audio.")
        except sr.RequestError:
            text = ("Could not request results from the service. Check your internet connection.")
    return text

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
    app.run(debug=True)