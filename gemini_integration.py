
import google.generativeai as genai
from api_key import API_KEY
import webbrowser

# Configure the Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def ask_gemini(prompt):
    """Sends a prompt to the Gemini API and returns the response."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return "Sorry, I'm having trouble connecting to my brain right now."

def handle_visual_prompt(prompt):
    """
    A placeholder for handling visual prompts.
    This could be extended to open images, display charts, etc.
    """
    try:
        # For now, let's assume the response is a URL to an image
        # In a real implementation, you would parse the response to identify a URL
        # or generate an image and save it locally.
        image_url = ask_gemini(f"Show me an image of {prompt}") # This is a simplified example
        webbrowser.open(image_url)
        return f"I've opened an image of {prompt} in your browser."
    except Exception as e:
        print(f"An error occurred with the visual prompt: {e}")
        return "Sorry, I couldn't display the visual content."
