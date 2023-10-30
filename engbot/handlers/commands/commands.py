from telegram.ext import ContextTypes, CommandHandler
from telegram import Update

from random import choice

from engbot.handlers.commands.utils import TEXT_FOR_START_COMMAND
from engbot.database.main_database.repositories.users import CreateUser
from engbot.models.users import User


async def command_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    CreateUser(user_model=User(
        telegram_id=user.id,
        username=user.username,
        language_code=user.language_code
    ))

    answer = choice(TEXT_FOR_START_COMMAND)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer,
        )


async def command_new_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Mock for create new word",
        )


async def command_words_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Mock for list of words",
        )
