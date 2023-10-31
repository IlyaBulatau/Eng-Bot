from engbot.handlers.commands.assemble import assemble_commands
from engbot.handlers.message.create_new_word.handlers import HANDLER_CREATE_NEW_WORD

from telegram.ext import Application


def setup_handlers(application: Application):
    application.add_handler(HANDLER_CREATE_NEW_WORD)
    assemble_commands(application)
