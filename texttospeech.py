# import pyttsx3

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Function to convert text to speech
# def text_to_speech(text):
#     engine.say(text)  # Speak the given text
#     engine.runAndWait()  # Wait for the speech to finish

# # Example usage
# text = input("Enter the text to speak: ")
# text_to_speech(text)
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set speech rate (default is around 200, lower it to slow down)
engine.setProperty("rate", 100)  # Adjust value (e.g., 100 for very slow, 150 for normal)

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)  # Speak the given text
    engine.runAndWait()  # Wait for the speech to finish

# Example usage
text = input("Enter the text to speak: ")
text_to_speech(text)
