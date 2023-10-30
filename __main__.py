from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram import Update

import logging

from engbot.database.main_database.db import Database
from engbot.config import Config



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(user.id)
    

if __name__ == "__main__":
    application = ApplicationBuilder().token(token=Config.BOT_TOKEN).build()

    application.add_handler(handler=MessageHandler(filters=filters.TEXT, callback=handler))

    application.run_polling()
