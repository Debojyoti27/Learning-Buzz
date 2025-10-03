import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# ✅ Use Render environment variable for security
openai.api_key = os.environ.get("OPENAI_API_KEY")

# ---------- ROUTES FOR PAGES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/flashcards")
def flashcards_page():
    return render_template("flashcards.html")

@app.route("/notes")
def notes_page():
    return render_template("notes.html")

@app.route("/bridge")
def bridge_page():
    return render_template("bridge.html")

# ---------- API ENDPOINTS ----------
@app.route("/api/flashcards", methods=["POST"])
def generate_flashcards():
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

@app.route("/api/notes", methods=["POST"])
def generate_notes():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that generates concise study notes."},
            {"role": "user", "content": f"Summarize this text into structured notes:\n{text}"}
        ]
    )

    notes = response['choices'][0]['message']['content']
    return jsonify({"notes": notes})

# ---------- MAIN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
