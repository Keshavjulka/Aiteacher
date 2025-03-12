from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import cv2
import mediapipe as mp
import threading
import time

app = Flask(__name__)

# Configure Gemini API Key
genai.configure(api_key="AIzaSyC9M3kgtjIPHdP0nS5tG8IKpgiKInfaGDY")

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

@app.route('/speech-to-text', methods=['POST'])
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            user_text = recognizer.recognize_google(audio)
            return jsonify({"text": user_text})
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio"})
        except sr.RequestError:
            return jsonify({"error": "Check internet connection"})

@app.route('/ask-gemini', methods=['POST'])
def chat_with_gemini():
    data = request.json
    user_question = data.get("question")
    if not user_question:
        return jsonify({"error": "No question provided"})
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_question)
    return jsonify({"response": response.text})

# Hand Gesture Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)
hand_raised = False

def detect_hand_raise():
    global hand_raised
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                wrist_y = hand_landmarks.landmark[0].y
                finger_tips_y = [hand_landmarks.landmark[i].y for i in [8, 12, 16, 20]]
                if all(tip < wrist_y for tip in finger_tips_y):
                    hand_raised = True
                    print("Hand raised detected!")
                    cv2.waitKey(60)
                else:
                    hand_raised = False
            
            cv2.imshow('Hand Gesture Detection', img)
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/hand-status', methods=['GET'])
def get_hand_status():
    return jsonify({"hand_raised": hand_raised})

if __name__ == '__main__':
    hand_detection_thread = threading.Thread(target=detect_hand_raise)
    hand_detection_thread.start()
    app.run(debug=True)