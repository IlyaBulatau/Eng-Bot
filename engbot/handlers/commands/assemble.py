from engbot.handlers.commands import commands

from telegram.ext import CommandHandler, Application


def assemble_commands(application: Application):
    application.add_handler(
        CommandHandler(command="start", callback=commands.command_start_handler)
        )
    application.add_handler(
        CommandHandler(command="new_word", callback=commands.command_new_word)
        )
    application.add_handler(
        CommandHandler(command="words", callback=commands.command_words_handler)
        )

