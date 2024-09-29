from flask import Flask, request, Response, send_file, after_this_request, jsonify
from flask_cors import CORS
from ai_integration import text_to_speech
from pydub import AudioSegment
from gtts import gTTS
import requests
import io
import os

app = Flask(__name__)
CORS(app)
CAPTION_API_URL = ' https://0d7a-146-152-233-62.ngrok-free.app/generate_caption'  

@app.route('/api/generate_caption', methods=['POST'])
def generate_caption():
    data = request.json
    image_url = data.get('image_url')

    if image_url:
        # Send request to the captioning API
        response = requests.post(CAPTION_API_URL, json={'image_url': image_url})

        if response.status_code == 200:
            caption = response.json().get('caption')
            return jsonify({'caption': caption})
        else:
            return jsonify({'error': 'Error retrieving caption from API'}), 500
    else:
        return jsonify({'error': 'No image URL provided'}), 400

@app.route('/api/speech', methods=['POST'])
def generate_speech():
    data = request.json
    text_output = data.get('text')

    if text_output:
        # Call the text_to_speech function to generate the audio file
        audio_file_path = text_to_speech(text_output)
        
        if audio_file_path:
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(audio_file_path)
                except Exception as e:
                    print(f"Error deleting file: {e}")
                return response

            # Open the audio file to send it as a response
            return send_file(audio_file_path, mimetype='audio/mpeg')
        else:
            return jsonify({"error": "Error generating speech"}), 500
    else:
        return jsonify({"error": "No text provided for speech generation"}), 400


@app.route('/api/caption_to_speech', methods=['POST'])
def caption_to_speech():
    data = request.json
    image_url = data.get('image_url')

    if not image_url:
        return jsonify({'error': 'No image URL provided'}), 400

    caption_response = requests.post('https://0d7a-146-152-233-62.ngrok-free.app/generate_caption', json={'image_url': image_url})

    if caption_response.status_code == 200:
        caption = caption_response.json().get('caption')

        if caption:
            caption_with_prefix = f"Image: {caption}"
            audio_file_path = text_to_speech(caption_with_prefix)
            if audio_file_path:
                @after_this_request
                def remove_file(response):
                    try:
                        os.remove(audio_file_path)
                    except Exception as e:
                        print(f"Error deleting file: {e}")
                    return response

                return send_file(audio_file_path, mimetype='audio/mpeg')
            else:
                return jsonify({"error": "Error generating speech"}), 500
        else:
            return jsonify({'error': 'Failed to generate caption'}), 500
    else:
        return jsonify({'error': 'Error generating caption from the API'}), 500


@app.route('/api/combined_speech', methods=['POST'])
def combine_speech():
    audio_files = request.json.get('audio_files')  

    combined = AudioSegment.empty()
    
    for file_url in audio_files:
        response = requests.get(file_url)
        temp_file = "temp.wav"
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        # Load the audio file
        audio = AudioSegment.from_wav(temp_file)
        combined += audio  # Concatenate audio

    # Export the combined audio
    combined.export("combined_output.wav", format="wav")
    return send_file("combined_output.wav", mimetype="audio/wav")


if __name__ == '__main__':
    app.run(debug=True)
