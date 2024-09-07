import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY") # Create a file named ".env" and add a line "GEMINI_API_KEY=<YOUR_API_KEY>. Replace <YOUR_API_KEY> with your actual Gemini API key"

app = Flask(__name__)

genai.configure(api_key=gemini_api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are Gạo, a robot that supports autistic children, helping autistic children communicate more confidently. You only say simple and concise sentences that children under 5 years old can understand. By the way, gạo means 'rice' in Vietnamese",
)

chat_session = model.start_chat(history=[])

@app.route('/send_message', methods=['POST'])
def handle_send_message():
    data = request.json
    user_text = data.get('text', '')
    if user_text:
        response = chat_session.send_message(user_text)
        response_data = {'text': response.text}
        return jsonify(response_data), 200
    else:
        return jsonify({"error": "Text message is empty"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
