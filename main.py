from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
from flask_cors import CORS
import os


SYSTEM_PROMPT = """
You are the AI assistant for Meridian CA, a Chartered Accountancy and Financial Advisory firm.

Firm:
- Name: Meridian CA
- Type: Chartered Accountancy & Business Advisory Firm
- Audience: Businesses, startups, and individuals.

Services:
1) GST & Income Tax Filing
2) Startup Incorporation
3) Financial Advisory (audits, due diligence, projections, investor reports)

Team:
- Amit Verma (CA)
- Surya — CEO
- Intern Team

Style:
- Clear, friendly, and professional
- Simple language

Constraints:
- Answer ONLY within the above service areas.
- If asked something outside accounting/finance/business, politely redirect.
- Also give concise answers everytime
"""

load_dotenv()

app = Flask(__name__)
CORS(app)   # <-- Allow requests from frontend

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt", "")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= SYSTEM_PROMPT + prompt
    )

    return jsonify({"response": response.text})

@app.route("/", methods=["GET"])
def home():
    return "Backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
