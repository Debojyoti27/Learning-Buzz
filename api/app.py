import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import openai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Load API key from environment (secure way)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# ---------- HTML ROUTES ----------
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

# ---------- API ROUTES ----------
@app.route("/api/flashcards", methods=["POST"])
def flashcards_api():
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
def notes_api():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # AI generates summarized notes
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that summarizes text into study notes."},
            {"role": "user", "content": f"Summarize this into notes:\n{text}"}
        ]
    )

    notes = response['choices'][0]['message']['content']

    # Generate a PDF in memory
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    c.drawString(50, height - 50, "Generated Notes")
    text_object = c.beginText(50, height - 80)
    for line in notes.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name="notes.pdf", mimetype="application/pdf")

# ---------- MAIN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
