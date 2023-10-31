from engbot.handlers.commands import commands

from telegram.ext import CommandHandler, Application


def assemble_commands(application: Application):
    application.add_handler(
        CommandHandler(command="start", callback=commands.command_start)
        )
    application.add_handler(
        CommandHandler(command="words", callback=commands.command_words)
        )
    application.add_handler(
        CommandHandler(command="cancel", callback=commands.command_cancel)
    )

