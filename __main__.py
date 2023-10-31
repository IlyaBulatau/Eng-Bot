from telegram.ext import ApplicationBuilder

import logging

from engbot.handlers.setup_handlers import setup_handlers
from engbot.config import Config


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(token=Config.BOT_TOKEN).concurrent_updates(False).build()

    setup_handlers(application)

    application.run_polling()
