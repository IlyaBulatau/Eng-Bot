from telegram.ext import ApplicationBuilder
from telegram import Update

import logging

from engbot.handlers.setup_handlers import setup_handlers
from engbot.config import Config
from engbot.utils.set_command import set_command_ui


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(token=Config.BOT_TOKEN)
    builder = application.concurrent_updates(False).post_init(set_command_ui).build()

    setup_handlers(builder)

    builder.run_polling(allowed_updates=Update.ALL_TYPES)
