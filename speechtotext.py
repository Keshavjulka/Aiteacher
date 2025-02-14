import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the microphone as the audio source
with sr.Microphone() as source:
    print("Adjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source, duration=5)
    print("Please speak now:")
    
    # Listen to the user's speech
    audio = recognizer.listen(source)

    try:
        # Use Google's speech recognition to convert speech to text
        print("Recognizing... Please wait.")
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
