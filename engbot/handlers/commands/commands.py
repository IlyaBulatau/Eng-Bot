from telegram.ext import ContextTypes, CommandHandler
from telegram import Update

from random import choice

from engbot.handlers.commands.utils import TEXT_FOR_START_COMMAND
from engbot.database.main_database.repositories.users import CreateUser
from engbot.models.users import User


async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    CreateUser(
        user_model=User(
            telegram_id=user.id,
            username=user.username,
            language_code=user.language_code,
        )
    )

    answer = choice(TEXT_FOR_START_COMMAND)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer,
    )


async def command_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Рабочих процессов нету"
    )


async def command_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Mock for list of words",
    )
