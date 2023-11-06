from engbot.handlers.commands.assemble import assemble_commands
from engbot.handlers.message.create_new_word.handlers import HANDLER_CREATE_NEW_WORD
from engbot.handlers.message.work_with_words import handlers
from engbot.utils.helpers import accept_callback_arrows, accept_callback_language_type

from telegram.ext import Application, CallbackQueryHandler


def setup_handlers(application: Application):
    application.add_handler(HANDLER_CREATE_NEW_WORD)
    assemble_commands(application)
    application.add_handler(
        CallbackQueryHandler(
            callback=handlers.callback_arrows, pattern=accept_callback_arrows
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            callback=handlers.callback_language_buttom,
            pattern=accept_callback_language_type,
        )
    )
    application.add_handler(CallbackQueryHandler(callback=handlers.empty_callback))
