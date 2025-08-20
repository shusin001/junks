
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import smtplib
import time
import json
import threading

# --- Core Setup ---
# Initialize the speech recognition and text-to-speech engines.
# It's good practice to set up your voice and properties right at the start.
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Choosing a voice. Index 1 often sounds more "assistant-like" on Windows.
engine.setProperty('voice', voices[1].id)

# --- Configuration & Credentials ---
# Load commands and other settings from a config file. This keeps the code clean
# and makes it easy to change commands without touching the logic.
try:
    with open('config.json') as f:
        config = json.load(f)
        COMMANDS = config['commands']
        EMAIL_ADDRESS = config.get('email_address')
        EMAIL_PASSWORD = config.get('email_password')
        WEATHER_API_KEY = config.get('weather_api_key')
except FileNotFoundError:
    print("Error: 'config.json' not found. Please create one with your settings.")
    exit()
except json.JSONDecodeError:
    print("Error: 'config.json' is not a valid JSON file. Please check its format.")
    exit()

# --- Helper Functions ---
# A simple, reusable function for the AI to speak.
def talk(text):
    """Makes Ramu speak the given text."""
    print(f"Ramu: {text}")
    engine.say(text)
    engine.runAndWait()

# A more robust function to capture and process user commands.
def take_command():
    """Listens for a voice command and returns it as a lowercase string."""
    try:
        with sr.Microphone() as source:
            print('Listening for your command...')
            # Adjust for ambient noise to improve recognition accuracy.
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            # A common pattern: remove the wake word from the command.
            if 'ramu' in command:
                command = command.replace('ramu', '').strip()
                print(f"You said: {command}")
    except sr.UnknownValueError:
        # Gracefully handle cases where the speech is not understood.
        talk("Sorry, I couldn't quite catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        # Handle API connection errors.
        talk("My apologies, my speech recognition service is currently unavailable.")
        return ""
    except Exception as e:
        # Catch any other unexpected errors during the process.
        print(f"An unexpected error occurred during command capture: {e}")
        talk("I've encountered an issue. Please try again in a moment.")
        return ""
    return command

# Email sending function. Encapsulated for reusability and error handling.
def send_email(to, subject, body):
    """Sends an email using the configured Gmail account."""
    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD]):
        talk("Email credentials are not set up. Please configure your email in the config file.")
        return

    try:
        # Using a context manager for the SMTP server ensures it's properly closed.
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection.
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f'Subject: {subject}\n\n{body}'
            server.sendmail(EMAIL_ADDRESS, to, message)
        talk('Email sent successfully.')
    except smtplib.SMTPAuthenticationError:
        talk("Failed to log in. Please check your email address and password, and ensure 'Less secure app access' is enabled for your Gmail account.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        talk('I\'m sorry, but I was unable to send the email.')

def set_reminder(minutes, reminder_text):
    """Sets a timer and reminds the user after the specified duration."""
    try:
        # Using a separate thread to not block the main loop.
        def reminder_thread():
            time.sleep(minutes * 60)
            talk(f"Reminder: {reminder_text}")

        thread = threading.Thread(target=reminder_thread)
        thread.daemon = True # Allows the main program to exit even if the thread is running.
        thread.start()
        talk(f"Okay, I'll remind you about {reminder_text} in {minutes} minutes.")
    except ValueError:
        talk("That's not a valid number of minutes. Please specify a number.")
    except Exception as e:
        print(f"Failed to set reminder: {e}")
        talk("Sorry, I couldn't set that reminder for you.")

def get_weather(city):
    """Fetches and reports the current weather for a given city."""
    if not WEATHER_API_KEY or WEATHER_API_KEY == 'YOUR_API_KEY':
        talk("The weather API key is not configured. Please add it to your config file.")
        return

    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
    try:
        response = requests.get(url)
        # Using raise_for_status() is a clean way to handle HTTP errors.
        response.raise_for_status()
        data = response.json()
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text']
        talk(f'The weather in {city} is {condition} with a temperature of {temp} degrees Celsius.')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        talk(f'Sorry, I could not get the weather information for {city}.')
    except (KeyError, IndexError):
        talk(f"Could not parse the weather data for {city}. Please check the city name.")


# --- Main Logic ---
def run_ramu():
    """The main function to process and respond to commands."""
    command = take_command()
    if not command:
        return

    # Use a dictionary or a series of if/elif for command handling.
    # This structure is clear and easy to extend.
    if COMMANDS['play'] in command:
        song = command.replace(COMMANDS['play'], '').strip()
        talk(f'Playing {song} on YouTube.')
        pywhatkit.playonyt(song)
    elif COMMANDS['time'] in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'The current time is {current_time}.')
    elif COMMANDS['who_the_heck_is'] in command:
        try:
            person = command.replace(COMMANDS['who_the_heck_is'], '').strip()
            # Limiting the summary to one sentence for a concise answer.
            info = wikipedia.summary(person, sentences=1)
            talk(info)
        except wikipedia.exceptions.PageError:
            talk("I couldn't find any information on that person.")
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"There are multiple results. Could you be more specific? For example: {', '.join(e.options[:3])}")
    elif COMMANDS['date'] in command:
        talk('I\'m sorry, but that feature is not implemented yet. I\'m still learning new tricks!')
    elif COMMANDS['are_you_single'] in command:
        talk('I am happily in a relationship with the Wi-Fi. It\'s a very stable connection.')
    elif COMMANDS['joke'] in command:
        talk(pyjokes.get_joke())
    elif COMMANDS['add_to_do'] in command:
        todo = command.replace(COMMANDS['add_to_do'], '').strip()
        with open('todo_list.txt', 'a') as f:
            f.write(todo + '\n')
        talk(f'Added "{todo}" to your to-do list.')
    elif COMMANDS['list_to_do'] in command:
        try:
            with open('todo_list.txt', 'r') as f:
                todos = [line.strip() for line in f if line.strip()]
            if todos:
                talk('Your to-do list contains the following items:')
                for i, todo in enumerate(todos):
                    talk(f'Item {i+1}: {todo}')
            else:
                talk('Your to-do list is currently empty.')
        except FileNotFoundError:
            talk('Your to-do list is empty. You can add items by saying "add to-do".')
    elif COMMANDS['weather'] in command:
        city = command.replace(COMMANDS['weather'], '').strip()
        if city:
            get_weather(city)
        else:
            talk("Please specify a city for the weather.")
    elif COMMANDS['send_email'] in command:
        talk('Who is the recipient?')
        to = take_command()
        # You'd need to parse the recipient from the command. A more advanced
        # system would have a contact list. For now, this is a placeholder.
        talk('What is the subject of the email?')
        subject = take_command()
        talk('And what is the message?')
        body = take_command()
        # In a real-world app, you'd parse 'to' to be an actual email address.
        send_email(to, subject, body)
    elif COMMANDS['set_reminder'] in command:
        # A more robust solution would parse the time and text from a single command.
        talk('What should I remind you about?')
        reminder_text = take_command()
        talk('In how many minutes?')
        try:
            minutes = float(take_command().split()[0]) # Tries to get a number.
            set_reminder(minutes, reminder_text)
        except (ValueError, IndexError):
            talk("I couldn't understand the time. Please try again.")
    elif COMMANDS['smart_home'] in command:
        talk('This feature is currently a placeholder. Please connect your smart home API here.')
        # control_smart_home(device, action) # Placeholder for a real API call.
    else:
        talk('I\'m not sure how to handle that. Could you please rephrase your command?')

# --- Execution Loop ---
if __name__ == '__main__':
    talk("Hello! I'm Ramu, your personal assistant. What can I do for you?")
    while True:
        try:
            run_ramu()
        except Exception as e:
            # Catching and logging exceptions in the main loop to prevent crashing.
            print(f"An unexpected error occurred in the main loop: {e}")
            talk("I've encountered a critical error. Restarting my listening process.")
            time.sleep(1) # Small delay before restarting.
