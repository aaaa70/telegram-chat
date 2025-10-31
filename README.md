# Telegram Bot using google/gemma-7b-it via OpenRouter

## Setup (Render or any server)

1. Upload this project to Render (or your server).
2. In Render dashboard, set the following **Environment Variables**:
   - `TELEGRAM_TOKEN` — your Telegram bot token (from BotFather)
   - `OPENROUTER_API_KEY` — your OpenRouter API key

3. Start the service (Render will use the `Procfile` to run the bot).

## Notes
- The bot replies with **text only**.
- The code expects the OpenRouter chat completions endpoint at `https://openrouter.ai/api/v1/chat/completions`.
- For security, **do not** put tokens directly inside `main.py`. Use environment variables.
