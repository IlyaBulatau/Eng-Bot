from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram import Update

import logging

from engbot.config import Config



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(token=Config.BOT_TOKEN).build()
    
    application.run_polling()
