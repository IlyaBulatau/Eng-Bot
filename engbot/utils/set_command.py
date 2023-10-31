from telegram import BotCommand
from telegram.ext import Application, ExtBot

from enum import Enum


class CommandEnum(Enum):

    start: str = "start"
    cancel: str = "cancel"
    new: str = "new"


async def set_command_ui(application: Application) -> None:
    """
    Set up UI menu to bot
    """

    bot: ExtBot = application.bot

    commands = [
                BotCommand(command=CommandEnum.start.value, description="Начало"),
                BotCommand(command=CommandEnum.cancel.value, description="Сброс"),
                BotCommand(command=CommandEnum.new.value, description="Новое слово"),
               ]

    await bot.set_my_commands(commands=commands)