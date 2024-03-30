from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai
from flask_cors import CORS
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("API_KEY")

@app.route('/translate', methods=['POST'])
def translate_italian_to_english():
    data = request.json
    italian_text = data.get('text', '')

    if not italian_text:
        return jsonify({'error': 'No Italian text provided for translation.'}), 400

    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a sophisticated translation agent capable of translating Italian text to English."},
            {"role": "user", "content": italian_text}
        ]
    }

    try:
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            translated_text = response_data['choices'][0]['message']['content']

            return jsonify({'translated_text': translated_text}), 200
        else:
            return jsonify({'error': 'Failed to translate text, OpenAI API error.'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
