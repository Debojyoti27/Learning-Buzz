import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Use environment variable for safety
openai.api_key = os.environ.get("OPENAI_API_KEY")

# -------------------------
# ROUTES
# -------------------------

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Flashcards Page
@app.route("/flashcards-page")
def flashcards_page():
    return render_template("flashcards.html")

# Notes Page
@app.route("/notes-page")
def notes_page():
    return render_template("notes.html")

# -------------------------
# API ENDPOINTS
# -------------------------

# Flashcards AI
@app.route("/flashcards", methods=["POST"])
def flashcards():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates simple flashcards."},
                {"role": "user", "content": f"Generate 5 Q&A style flashcards from this text:\n{text}"}
            ]
        )
        cards = response["choices"][0]["message"]["content"].split("\n")
        return jsonify({"cards": cards})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Notes AI
@app.route("/notes", methods=["POST"])
def notes():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that summarizes and organizes notes clearly."},
                {"role": "user", "content": f"Summarize and organize these notes in bullet points:\n{text}"}
            ]
        )
        notes_text = response["choices"][0]["message"]["content"]
        return jsonify({"notes": notes_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# MAIN ENTRY
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
