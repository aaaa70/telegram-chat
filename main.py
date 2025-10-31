import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise RuntimeError("Environment variables TELEGRAM_TOKEN and OPENROUTER_API_KEY must be set.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 من با مدل Google Gemma 7B کار می‌کنم. پیام بده تا پاسخ بدم 😊")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "google/gemma-7b-it",
        "messages": [
            {"role": "system", "content": "You are a helpful Persian assistant."},
            {"role": "user", "content": user_message},
        ],
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            await update.message.reply_text(answer)
        else:
            await update.message.reply_text(f"❌ خطا از OpenRouter ({response.status_code})")
    except Exception as e:
        await update.message.reply_text("⚠️ خطایی رخ داد: " + str(e))

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("🤖 Bot started successfully...")
    app.run_polling()

if __name__ == "__main__":
    main()
