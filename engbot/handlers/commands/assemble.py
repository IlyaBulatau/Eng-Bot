from engbot.handlers.commands import commands
from engbot.utils.set_command import CommandEnum

from telegram.ext import CommandHandler, Application


def assemble_commands(application: Application):
    application.add_handler(
        CommandHandler(command=CommandEnum.START.value, callback=commands.command_start)
    )
    application.add_handler(
        CommandHandler(
            command=CommandEnum.CANCEL.value, callback=commands.command_cancel
        )
    )
    application.add_handler(
        CommandHandler(command=CommandEnum.WORDS.value, callback=commands.command_words)
    )
    application.add_handler(
        CommandHandler(command=CommandEnum.INFO.value, callback=commands.command_info)
    )
