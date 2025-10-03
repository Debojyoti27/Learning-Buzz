from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app)

# ROUTES FOR PAGES
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

# API ENDPOINT (example flashcard generator)
@app.route("/api/flashcards", methods=["POST"])
def flashcards_api():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    # Here you could connect to OpenAI or custom logic
    cards = [f"Flashcard {i+1} from: {text}" for i in range(5)]
    return jsonify({"cards": cards})

# ✅ Handler for Vercel
def handler(request, *args, **kwargs):
    return app(request.environ, lambda s, h: (s, h))
