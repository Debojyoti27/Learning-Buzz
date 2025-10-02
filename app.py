import os
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import openai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
CORS(app)

# Load API key securely
openai.api_key = os.environ.get("OPENAI_API_KEY")

# ---------- ROUTES FOR FRONTEND PAGES ----------
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
def flashcards():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates simple study flashcards."},
                {"role": "user", "content": f"Generate 5 flashcards from this text:\n{text}"}
            ]
        )
        cards = response['choices'][0]['message']['content'].split("\n")
        return jsonify({"cards": cards})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/notes", methods=["POST"])
def generate_notes():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that summarizes text into clear, structured notes."},
                {"role": "user", "content": f"Summarize the following text into notes:\n{text}"}
            ]
        )
        notes = response['choices'][0]['message']['content']

        # Create PDF in memory
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.setFont("Helvetica", 12)

        y = 750
        for line in notes.split("\n"):
            c.drawString(50, y, line.strip())
            y -= 20
            if y < 50:  # New page if content is too long
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 750

        c.save()
        pdf_buffer.seek(0)

        return send_file(pdf_buffer, as_attachment=True, download_name="notes.pdf", mimetype="application/pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- RUN APP ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
