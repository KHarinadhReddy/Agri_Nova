import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("API Key not found in .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Serve the single master interface
@app.route('/')
def home():
    return render_template('index.html')

# Handle the AI scanning logic
@app.route('/scan', methods=['POST'])
def scan_plant():
    try:
        data = request.get_json()
        base64_image = data.get('image')

        if not base64_image:
            return jsonify({'error': 'No image received by server.'}), 400

        prompt = """
        Analyze this plant leaf. You must reply strictly in this format and nothing else:
        STATUS | Disease Name | Confidence%
        If healthy, STATUS must be HEALTHY. If sick, STATUS must be INFECTED.
        Example 1: HEALTHY | No Disease | 99
        Example 2: INFECTED | Powdery Mildew | 85
        """

        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": base64_image}])
        return jsonify({'candidates': [{'content': {'parts': [{'text': response.text}]}}]})

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=========================================")
    print("🌱 AGRI NOVA | SPA SERVER BOOTING...")
    print("=========================================")
    app.run(host='0.0.0.0', port=5000)