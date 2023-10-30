from engbot.handlers.commands.assemble import assemble_commands

from telegram.ext import Application

def setup_handlers(application: Application):
    assemble_commands(application)