from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from engbot.models.words import WordList, WordField
from engbot.utils.callback_datas import (
    LEFT_BUTTON,
    RIGHT_BUTTON,
    ENGLISH_LAGUAGE,
    RUSSIAN_LANGUAGE,
)


def keyboard_of_words(
    words_list: list[WordList],
    limit: int = 10,
    offset: int = 0,
    language_type: str = ENGLISH_LAGUAGE,
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

    type_of_word = (
        WordField.ENG_WORD.value
        if language_type == ENGLISH_LAGUAGE
        else WordField.TRANSlATE.value
    )

    markup: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=word_object.model_dump().get(type_of_word).capitalize(),
                callback_data=words_list[offset].created_on,
            )
        ]
        for word_object in words_list[offset].words
    ][:limit]

    arrows_bar = create_low_arrows_bar_to_keyboards(
        left_arrows=not (
            (offset == 0) or (offset == 0 and offset == count_date_of_words)
        ),
        right_arraow=not (
            (offset == count_date_of_words)
            or (offset == 0 and offset == count_date_of_words)
        ),
        language_type=language_type,
    )

    markup.extend(arrows_bar)

    return InlineKeyboardMarkup(markup)


def create_low_arrows_bar_to_keyboards(
    left_arrows=True, right_arraow=True, language_type=RUSSIAN_LANGUAGE
) -> list[InlineKeyboardButton]:
    markup = []
    middle_text = "🇬🇧" if language_type == RUSSIAN_LANGUAGE else "🇷🇺"

    left_buttom = InlineKeyboardButton(text="<<", callback_data=LEFT_BUTTON)
    right_buttom = InlineKeyboardButton(text=">>", callback_data=RIGHT_BUTTON)
    midle_buttom = InlineKeyboardButton(text=middle_text, callback_data=language_type)

    if left_arrows:
        markup.append(left_buttom)
    markup.append(midle_buttom)
    if right_arraow:
        markup.append(right_buttom)

    return [markup]
