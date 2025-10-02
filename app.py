import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Get OpenAI API key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/flashcards_page")
def flashcards_page():
    return render_template("flashcards.html")

@app.route("/notes_page")
def notes_page():
    return render_template("notes.html")

@app.route("/bridge_page")
def bridge_page():
    return render_template("bridge.html")

# ------------------ AI ENDPOINTS ------------------

@app.route("/flashcards", methods=["POST"])
def generate_flashcards():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates simple study flashcards."},
                {"role": "user", "content": f"Generate 5 concise flashcards from this text:\n{text}"}
            ],
            temperature=0.6,
            max_tokens=500
        )
        cards_text = response['choices'][0]['message']['content'].split("\n")
        cards = [c.strip() for c in cards_text if c.strip()]
        return jsonify({"cards": cards})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/notes_ai", methods=["POST"])
def generate_notes():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"notes": ""})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that summarizes text into concise study notes."},
                {"role": "user", "content": f"Generate clear, organized notes from this text:\n{text}"}
            ],
            temperature=0.5,
            max_tokens=800
        )
        notes = response['choices'][0]['message']['content']
        return jsonify({"notes": notes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ RUN APP ------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
