from flask import Flask, request
import telegram
import json
import os

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Load medical knowledge base
with open("medical_knowledge.json") as f:
    knowledge_base = json.load(f)

@app.route('/')
def home():
    return "MediCore+ is running!"

@app.route('/webhook', methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    user_message = update.message.text.lower()

    response = "❓ I couldn't find that concept. Please try something else."

    for concept, details in knowledge_base["concepts"].items():
        if concept in user_message:
            response = f"📘 *{concept.title()}*

🧠 {details['definition']}

💡 Symptoms: {', '.join(details['symptoms'])}
🧪 Diagnosis: {', '.join(details['diagnosis'])}
💊 Treatments: {', '.join(details['treatments'])}"
            break

    bot.send_message(chat_id=chat_id, text=response, parse_mode=telegram.ParseMode.MARKDOWN)
    return "ok"