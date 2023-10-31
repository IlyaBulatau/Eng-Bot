from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from telegram import Update

from enum import Enum


class StateEnum(Enum):
    eng_word: str = "ENG WORD"
    translate: str = "TRANSLATE"


async def command_new_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starting of saving new word
    Asking write new word
    """

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
Введие слово или выражение на английском которое хотите сохранить и для которого далее напишите перевод\n\n
Слово/выражение должно содержать только английские буквы и знаки пробела
        """,
    )

    return StateEnum.eng_word.value


async def receive_eng_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receiving new word and save them
    Asking write translating the word
    """

    word = update.effective_message.text
    context.user_data.update(word=word)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
Отлично!\n\nТеперь введите перевод на русском для слова {word}\n\n\
Перевод должен содержать только русские буквы и знаки пробела
""",
    )

    return StateEnum.translate.value


async def incorrectly_eng_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = update.effective_message.text

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
Ввод не корректный, попробуйте еще раз\n\n
Для завершения процесса /cancel
""",
    )

    user_data = context.user_data

    if user_data == {}:
        return StateEnum.eng_word.value
    return StateEnum.translate.value


async def receive_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receiving translate the word
    Saving the word and the translate in database
    """

    translate = update.effective_message.text
    context.user_data.update(translate=translate)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Прекрасно! Можете взглянуть на свой словарь /words",
    )

    context.user_data.clear()
    return ConversationHandler.END


async def command_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Процесс прерван",
    )

    return ConversationHandler.END


HANDLER_CREATE_NEW_WORD = ConversationHandler(
    entry_points=[CommandHandler(command="new", callback=command_new_word)],
    states={
        StateEnum.eng_word.value: [
            MessageHandler(
                filters=filters.TEXT
                & ~filters.COMMAND
                & filters.Regex(r"^[a-zA-z\s]+$"),
                callback=receive_eng_word,
            ),
            MessageHandler(
                filters=filters.ALL & ~filters.COMMAND, callback=incorrectly_eng_word
            ),
        ],
        StateEnum.translate.value: [
            MessageHandler(
                filters=filters.TEXT
                & ~filters.COMMAND
                & filters.Regex(r"^[А-Яа-я\s]+$"),
                callback=receive_translate,
            ),
            MessageHandler(
                filters=filters.ALL & ~filters.COMMAND, callback=incorrectly_eng_word
            ),
        ],
    },
    fallbacks=[CommandHandler(command="cancel", callback=command_cancel)],
)
