from telegram.ext import ContextTypes
from telegram import Update

from random import choice

from engbot.utils.keyboards import keyboard_of_words
from engbot.handlers.commands.utils import TEXT_FOR_START_COMMAND
from engbot.database.main_database.repositories.users import CreateUser
from engbot.database.main_database.repositories.words import ListWord
from engbot.models.users import User
from engbot.models.words import WordList


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


async def command_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_telegram_id = update.effective_user.id

    get_words = ListWord(telegram_id=user_telegram_id)
    words: list[WordList] = get_words()

    date_created_words: str = words[0].created_on

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Дата добавления: {date_created_words}",
        reply_markup=keyboard_of_words(words_list=words),
    )


async def command_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Рабочих процессов нету"
    )
