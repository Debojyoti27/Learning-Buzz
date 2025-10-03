from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/flashcards", methods=["POST"])
def generate_flashcards():
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates simple flashcards."},
                {"role": "user", "content": f"Generate 5 flashcards from this text:\n{text}"}
            ]
        )

        cards = response['choices'][0]['message']['content'].split("\n")
        return jsonify({"cards": cards})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/notes", methods=["POST"])
def generate_notes():
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Simple AI modification (optional)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that summarizes text into notes."},
                {"role": "user", "content": f"Summarize this text into concise notes:\n{text}"}
            ]
        )

        notes = response['choices'][0]['message']['content']
        return jsonify({"notes": notes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check
@app.route("/")
def home():
    return jsonify({"message": "API is running!"})
