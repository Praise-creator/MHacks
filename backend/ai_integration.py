import requests
from gtts import gTTS
import os
import tempfile

def generate_caption(image_url):
    """Generates a caption for the given image URL."""
    api_url = 'https://0d7a-146-152-233-62.ngrok-free.app/generate_caption'
    
    try:
        response = requests.post(api_url, json={'image_url': image_url})
        response.raise_for_status()  
        caption = response.json().get('caption')
        return caption
    except requests.RequestException as e:
        print(f"Error generating caption: {e}")
        return None

def text_to_speech(text):
    """Converts the provided text to speech and returns the file path."""
    try:
        tts = gTTS(text=text, lang='en')
        # Create a temporary file for the audio
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False)  
        tts.save(temp_audio_file.name)
        temp_audio_file.close()  
        return temp_audio_file.name  # Return the path of the temporary file
    except Exception as e:
        print(f"Error converting text to speech: {e}")
        return None


def cleanup_audio_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting audio file: {e}")