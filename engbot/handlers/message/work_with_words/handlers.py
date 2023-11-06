from telegram.ext import ContextTypes
from telegram import Update, CallbackQuery

from engbot.services.cache.states import CahceCurrentUserPage
from engbot.handlers.utils import TEXT_FOR_WORDS_SHOW
from engbot.utils.keyboards import keyboard_of_words
from engbot.database.main_database.repositories.words import ListWord
from engbot.models.words import WordList
from engbot.services.decorators.controller import controller
from engbot.utils.callback_datas import (
    LEFT_BUTTON,
    RIGHT_BUTTON,
    ENGLISH_LAGUAGE,
    RUSSIAN_LANGUAGE,
)


@controller
async def callback_arrows(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Reacts on touch arrows buttom

    If user touch left button - decrease current page if it touch right increment
    """
    # callback datas
    callback: CallbackQuery = update.callback_query
    callback_data = callback.data
    user_telegram_id: int = callback.from_user.id

    # get words
    get_words = ListWord(user_telegram_id)
    words: list[WordList] = get_words()

    # update current page in cache
    cache = CahceCurrentUserPage(user_telegram_id=user_telegram_id)

    if callback_data == LEFT_BUTTON:
        cache.update_page(amount=1, decrease=False)
    elif callback_data == RIGHT_BUTTON:
        cache.update_page(amount=1)

    current_page: int = cache.get_current_page()

    # build answer
    date_created_words: str = words[current_page].created_on
    markup = keyboard_of_words(words_list=words, offset=current_page)

    await callback.edit_message_text(
        text=TEXT_FOR_WORDS_SHOW.format(date=date_created_words), reply_markup=markup
    )


@controller
async def callback_language_buttom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # callback datas
    callback: CallbackQuery = update.callback_query
    callback_data = callback.data
    user_telegram_id: int = callback.from_user.id

    update_language = (
        ENGLISH_LAGUAGE if callback_data == RUSSIAN_LANGUAGE else RUSSIAN_LANGUAGE
    )

    # get words
    get_words = ListWord(user_telegram_id)
    words: list[WordList] = get_words()

    # update current page in cache
    cache = CahceCurrentUserPage(user_telegram_id=user_telegram_id)
    current_page = cache.get_current_page()

    date_created_words: str = words[current_page].created_on
    markup = keyboard_of_words(
        words_list=words, offset=current_page, language_type=update_language
    )

    await callback.edit_message_text(
        text=TEXT_FOR_WORDS_SHOW.format(date=date_created_words), reply_markup=markup
    )


async def empty_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handled callbacks that is empty
    """
    await update.callback_query.answer()


@controller
async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handled callbacks that is empty
    """
    ...
