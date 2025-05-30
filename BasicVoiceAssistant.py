import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize recognizer and text-to-speech
listener = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)  # Reduces background noise
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice)
            print("User said:", command)
            return command.lower()
    except sr.WaitTimeoutError:
        print("No speech detected within timeout")
        return ""
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return ""

def run_assistant():
    while True:  # Added loop to keep assistant running
        speak("Hello! How can I help you?")
        command = listen()

        if not command:
            continue
            
        if "hello" in command:
            speak("Hello there!")
        elif "time" in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The time is {time}")
        elif "date" in command:
            date = datetime.datetime.now().strftime('%B %d, %Y')
            speak(f"Today's date is {date}")
        elif "search" in command:
            search_query = command.replace("search", "").strip()
            if search_query:  # Only search if there's a query
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
                speak(f"Here is what I found for {search_query}")
            else:
                speak("What would you like me to search for?")
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            speak("I can't help with that yet.")

if __name__ == "__main__":
    run_assistant()