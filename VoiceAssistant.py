import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pywhatkit
import requests
import pyjokes
import openai
from transformers import pipeline
import nltk

# -------- API KEYS DIRECTLY IN CODE --------
openai.api_key = "api_key_here"  # --- Cannot upload due to security reasons ---
weather_api_key = "api_key_here"  # --- Cannot upload due to security reasons ---
news_api_key = "api_key_here"  # --- Cannot upload due to security reasons ---

nltk.download('punkt')
nlp_classifier = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student")

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
engine.setProperty('voice', voices[1].id)

WAKE_WORD = "jarvis"

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source, timeout=5)
            command = listener.recognize_google(audio)
            print("Heard:", command)
            return command.lower()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Speech service unavailable.")
        return ""

def get_intent(command):
    try:
        result = nlp_classifier(command)[0]
        label = result['label']
        print(f"Detected intent: {label}")
        return label
    except:
        return "unknown"

def get_weather(city):
    print(f"Fetching weather for: {city}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    try:
        res = requests.get(url).json()
        print(res)
        if res.get("main"):
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {desc}.")
        else:
            speak("Sorry, I couldn't find weather info for that city.")
    except Exception as e:
        print("Weather error:", e)
        speak("Failed to fetch weather data.")

def get_news():
    print("Fetching news...")
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"
    try:
        res = requests.get(url).json()
        print(res)
        if "articles" in res:
            speak("Here are the top news headlines:")
            for i, article in enumerate(res["articles"][:5]):
                speak(f"News {i+1}: {article['title']}")
        else:
            speak("No news found.")
    except Exception as e:
        print("News error:", e)
        speak("Failed to get news.")

def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response['choices'][0]['message']['content']
        speak(answer)
    except Exception as e:
        print("ChatGPT error:", e)
        speak("I had trouble connecting to ChatGPT.")

def process_command(command):
    print(f"Processing command: {command}")
    intent = get_intent(command)

    if "weather" in command:
        speak("Which city's weather would you like to know?")
        city = listen()
        if city:
            city = city.strip().title()
            print(f"User said city: {city}")
            get_weather(city)
        else:
            speak("I didn't catch the city name.")

    elif "news" in command:
        get_news()

    elif "time" in command:
        now = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {now}")

    elif "date" in command:
        if "tomorrow" in command:
            date = datetime.datetime.now() + datetime.timedelta(days=1)
            speak(f"Tomorrow's date is {date.strftime('%B %d, %Y')}")
        elif "yesterday" in command:
            date = datetime.datetime.now() - datetime.timedelta(days=1)
            speak(f"Yesterday's date was {date.strftime('%B %d, %Y')}")
        else:
            date = datetime.datetime.now().strftime('%B %d, %Y')
            speak(f"Today's date is {date}")

    elif "play" in command:
        song = command.replace("play", "").strip()
        pywhatkit.playonyt(song)
        speak(f"Playing {song}")

    elif "notepad" in command and "open" in command:
        print("Opening Notepad...")
        os.system("notepad.exe")
        speak("Opening Notepad.")

    elif "shutdown" in command:
        speak("Shutting down.")
        os.system("shutdown /s /t 1")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

    elif "greeting" in intent or "admiration" in intent:
        speak("Hello! How can I assist you?")

    elif "gratitude" in intent:
        speak("You're welcome!")

    elif "curiosity" in intent or "information_request" in intent:
        speak("Would you like me to search or ask ChatGPT?")
        next_cmd = listen()
        if "search" in next_cmd:
            webbrowser.open(f"https://www.google.com/search?q={command}")
            speak(f"Searching for {command}")
        else:
            ask_chatgpt(command)

    elif "amusement" in intent:
        speak(pyjokes.get_joke())

    elif "reminder" in intent or "note" in intent or "remember" in command:
        note = command.replace("remember", "").strip()
        with open("notes.txt", "a") as f:
            f.write(note + "\n")
        speak("Okay, noted.")

    else:
        speak("Let me check with ChatGPT.")
        ask_chatgpt(command)

def run_assistant():
    while True:
        command = listen()
        if command:
            if WAKE_WORD in command:
                speak("Yes? How can I help you?")
                command = listen()
                if command:
                    process_command(command)
            else:
                print(f"Command without wake word: {command}")
                process_command(command)

if __name__ == "__main__":
    run_assistant()