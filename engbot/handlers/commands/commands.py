from telegram.ext import ContextTypes
from telegram import Update

from random import choice

from engbot.utils.keyboards import keyboard_of_words
from engbot.handlers.utils import (
    TEXT_FOR_START_COMMAND,
    TEXT_FOR_WORDS_SHOW,
    TEXT_INFO_COMMAND,
)
from engbot.database.main_database.repositories.users import CreateUser
from engbot.database.main_database.repositories.words import ListWord
from engbot.models.users import User
from engbot.models.words import WordList
from engbot.services.cache.states import CahceCurrentUserPage, CacheLastWordKeyboard
from engbot.services.decorators.controller import controller


@controller
async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Reacts on 'start' command

    Creating new user if it not exists
    """
    user = update.effective_user
    CreateUser(
        user_model=User(
            telegram_id=user.id,
            username=user.username if user.username else user.first_name,
            language_code=user.language_code,
        )
    )

    answer = choice(TEXT_FOR_START_COMMAND)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer,
    )


@controller
async def command_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Reacts on 'words' command

    Sends message with text about date of created on words
    and keyboards of words to user

    Shows first list of words from end of list page

    Sets current page of user on zero
    """
    user_telegram_id = update.effective_user.id

    # set current page zero
    cache = CahceCurrentUserPage(user_telegram_id=user_telegram_id)
    cache.set_current_page()

    # delete prev keyboard of words
    cache_kb = CacheLastWordKeyboard(update=update, bot=context.bot)
    await cache_kb.delete()

    get_words = ListWord(telegram_id=user_telegram_id)
    words: list[WordList] = get_words()

    if not words:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🇬🇧 У вас нету записанных слов.\n\n💡 Вы можете сохранить новое слово использую команду /new",
        )
        return

    date_created_words: str = words[0].created_on
    markup = keyboard_of_words(words_list=words)

    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=TEXT_FOR_WORDS_SHOW.format(date=date_created_words),
        reply_markup=markup,
    )
    # save the kb of words in cache
    cache_kb.save(message.id)


@controller
async def command_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...


@controller
async def command_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_user.id, text=TEXT_INFO_COMMAND, parse_mode="Markdown"
    )


@controller
async def command_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends message about that not exists at the time work processes
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="⚙️ Рабочих процессов нету."
    )
