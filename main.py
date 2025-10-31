import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# خواندن توکن‌ها از Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if TELEGRAM_TOKEN is None or OPENROUTER_API_KEY is None:
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
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            # Try to parse response safely
            jr = response.json()
            # Fallback if structure is slightly different
            answer = None
            if isinstance(jr, dict):
                choices = jr.get("choices") or jr.get("outputs")
                if choices and isinstance(choices, list) and len(choices) > 0:
                    first = choices[0]
                    # Common schema: choices[0].message.content
                    if isinstance(first, dict):
                        if "message" in first and isinstance(first["message"], dict):
                            answer = first["message"].get("content")
                        elif "text" in first:
                            answer = first.get("text")
                        elif "output" in first:
                            answer = first.get("output")
            if not answer:
                answer = str(jr)
            await update.message.reply_text(answer)
        else:
            await update.message.reply_text(f"❌ خطا در دریافت پاسخ از OpenRouter (status={response.status_code})")
    except Exception as e:
        await update.message.reply_text("⚠️ خطایی رخ داد: " + str(e))

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
