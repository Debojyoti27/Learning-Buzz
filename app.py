import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
import os
openai.api_key = os.environ.get("OPENAI_API_KEY")
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your API key

@app.route("/flashcards", methods=["POST"])
def flashcards():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Simple AI call to generate flashcards
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that generates simple flashcards."},
            {"role": "user", "content": f"Generate 5 flashcards from this text:\n{text}"}
        ]
    )

    cards = response['choices'][0]['message']['content'].split("\n")
    return jsonify({"cards": cards})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
