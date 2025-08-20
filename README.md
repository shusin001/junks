# Voice Assistant

This is a voice assistant project created using Python. It can perform various tasks based on voice commands.

## Features

- Responds to greetings
- Tells the time and date
- Searches the web
- Manages a to-do list
- Gets weather updates
- Sends emails (requires configuration)
- Sets reminders
- Controls smart home devices (placeholder)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/voice-assistant.git
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the assistant:**
   - Open the `voice_assistant.py` file and replace the following placeholder values with your own:
     - `WEATHER_API_KEY`: Your API key from [weatherapi.com](https://www.weatherapi.com/)
     - `EMAIL_ADDRESS`: Your email address
     - `EMAIL_PASSWORD`: Your email password
   - Open the `config.json` file to customize the voice commands.

4. **Run the voice assistant:**
   ```bash
   python voice_assistant.py
   ```

## Usage

To use the voice assistant, simply run the `voice_assistant.py` script and say "Alexa" followed by your command.

For example:
- "Alexa, what's the time?"
- "Alexa, play a song by Queen"
- "Alexa, add 'buy groceries' to my to-do list"
- "Alexa, what's the weather in London?"

## Privacy and Security

Please be aware of the privacy and security implications of using a voice assistant. The assistant will have access to your microphone and may store your voice commands. If you configure the email feature, the assistant will also have access to your email credentials.

## Future Improvements

- **Natural Language Processing:** The current implementation uses simple string matching to understand commands. To improve this, you could use a library like [Rasa](https://rasa.com/) or [spaCy](https://spacy.io/) to add natural language processing capabilities.
- **Smart Home Control:** The smart home control feature is currently a placeholder. To make it functional, you would need to replace the placeholder function with your own smart home API calls.