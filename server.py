from flask import Flask, request, jsonify
import openai
import pyttsx3
import os

app = Flask(__name__)

# שימוש במפתח OpenAI (מומלץ להירשם לחשבון חינמי)
openai.api_key = "YOUR_OPENAI_API_KEY"

# אתחול מנוע דיבור
engine = pyttsx3.init()

def text_to_speech(text):
    """המרת טקסט לדיבור ושמירתו בקובץ"""
    audio_file = "response.mp3"
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    return audio_file

@app.route('/api/ivr', methods=['GET'])
def ivr_response():
    phone_number = request.args.get('ani', 'לא ידוע')
    user_input = request.args.get('text', 'שלום')

    # קבלת תשובה מה-AI (GPT)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "אתה עוזר טלפוני חכם"},
                  {"role": "user", "content": user_input}]
    )
    ai_response = response["choices"][0]["message"]["content"]

    # המרת התשובה לקובץ קול
    audio_file = text_to_speech(ai_response)

    return jsonify({"text": ai_response, "audio_url": f"https://yourserver.com/{audio_file}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
