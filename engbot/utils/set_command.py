from telegram import BotCommand
from telegram.ext import Application, ExtBot

from enum import Enum


class CommandEnum(Enum):
    START: str = "start"
    CANCEL: str = "cancel"
    NEW: str = "new"
    WORDS: str = "words"


async def set_command_ui(application: Application) -> None:
    """
    Set up UI menu to bot
    """

    bot: ExtBot = application.bot

    commands = [
        BotCommand(command=CommandEnum.START.value, description="Начало"),
        BotCommand(command=CommandEnum.CANCEL.value, description="Сброс"),
        BotCommand(command=CommandEnum.NEW.value, description="Новое слово"),
        BotCommand(command=CommandEnum.WORDS.value, description="Мои слова"),
    ]

    await bot.set_my_commands(commands=commands)
