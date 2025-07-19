
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from handlers.video_handler import handle_video_link, get_lang

logging.basicConfig(level=logging.INFO)
TOKEN = "7848915171:AAHg6LbnFge0whnHbqh_dJk8FfMnedhPFkE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    msg = {
        "ar": "👋 أهلاً بك في SaveMate!\nأرسل رابط فيديو من تيك توك، إنستغرام، تويتر أو فيسبوك لتحميله.",
        "en": "👋 Welcome to SaveMate!\nSend me a TikTok, Instagram, Twitter, or Facebook video link to download."
    }
    await update.message.reply_text(msg.get(lang, msg["en"]))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_video_link))
    app.run_polling()
