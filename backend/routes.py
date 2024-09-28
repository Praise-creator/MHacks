from flask import Blueprint, request, jsonify
from ai_integration import generate_alt_text, text_to_speech

main = Blueprint('main', __name__)

@main.route('/process-image', methods=['POST'])
def process_image():
    image_url = request.json.get('image_url')
    if not image_url:
        return jsonify({'error': 'No image URL provided.'}), 400

    alt_text = generate_alt_text(image_url)  # Call your AI function here
    speech = text_to_speech(alt_text)        # Convert alt text to speech

    return jsonify({
        'alt_text': alt_text,
        'speech_url': speech  # Return the speech audio URL or data
    })
