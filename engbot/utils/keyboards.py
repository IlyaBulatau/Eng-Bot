from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from engbot.models.words import WordList, WordField
from engbot.utils.callback_datas import (
    LEFT_BUTTOM,
    RIGHT_BUTTOM,
    ENGLISH_LAGUAGE,
    RUSSIAN_LANGUAGE,
)


def keyboard_of_words(
    words_list: list[WordList], limit: int = 10, offset: int = 0
) -> InlineKeyboardMarkup:
    """
    Create keyboard for show words

    Arguments:
    :words_list - list of WordList object that containe
                  all words of user from database
    :limit -      How many words shows in keyboard
    :offset -     which date with words will showing, starting from the end array
    """
    count_date_of_words = len(words_list) - 1

    markup: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=word_object.model_dump().get(WordField.ENG_WORD.value),
                callback_data=words_list[offset].created_on,
            )
        ]
        for word_object in words_list[offset].words
    ][:limit]

    arrows_bar = create_low_arrows_bar_to_keyboards()
    if offset == count_date_of_words:
        arrows_bar = create_low_arrows_bar_to_keyboards(right_arraow=False)
    if offset == 0:
        arrows_bar = create_low_arrows_bar_to_keyboards(left_arrows=False)

    markup.extend(arrows_bar)

    return InlineKeyboardMarkup(markup)


def create_low_arrows_bar_to_keyboards(
    left_arrows=True, right_arraow=True, language_turn=RUSSIAN_LANGUAGE
) -> list[InlineKeyboardButton]:
    markup = []
    middle_text = "🇬🇧" if language_turn == ENGLISH_LAGUAGE else "🇷🇺"

    left_buttom = InlineKeyboardButton(text="<<", callback_data=LEFT_BUTTOM)
    right_buttom = InlineKeyboardButton(text=">>", callback_data=RIGHT_BUTTOM)
    midle_buttom = InlineKeyboardButton(text=middle_text, callback_data=language_turn)

    if left_arrows:
        markup.append(left_buttom)
    markup.append(midle_buttom)
    if right_arraow:
        markup.append(right_buttom)

    return [markup]
