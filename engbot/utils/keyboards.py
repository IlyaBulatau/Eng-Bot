from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from engbot.models.words import Word, WordList, WordField


def keyboard_of_words(
    words_list: list[WordList], limit: int = 10, offset: int = 0
) -> InlineKeyboardMarkup:
    """
    Create keyboard for show words
    """
    
    markup: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=word_object.model_dump().get(WordField.ENG_WORD.value),
            callback_data=words_list[offset].created_on
        )]
        for word_object in words_list[offset].words
    ][:limit]
    
    return InlineKeyboardMarkup(markup)

