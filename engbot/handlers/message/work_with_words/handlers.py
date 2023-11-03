from telegram.ext import ContextTypes
from telegram import Update, CallbackQuery

from engbot.services.cache.states import CahceCurrentUserPage
from engbot.utils.keyboards import keyboard_of_words
from engbot.database.main_database.repositories.words import ListWord
from engbot.models.words import WordList
from engbot.utils.callback_datas import LEFT_BUTTON, RIGHT_BUTTON


async def callback_arrows(update: Update, context: ContextTypes):
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
        text=f"Дата добавления: {date_created_words}", reply_markup=markup
    )
