from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from telegram import Update

from engbot.database.main_database.repositories.words import CreateWord
from engbot.services.cache.states import State
from engbot.models.words import WordField
from engbot.utils.set_command import CommandEnum
from engbot.services.controllers.limiters import WordLimiter


async def command_new_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starting of saving new word
    Asking write new word

    Tracking limiting quantity words in day
    """
    answer = context.bot.send_message

    limiter = WordLimiter()
    if not limiter.is_acceptable(telegram_id=update.effective_user.id):
        await answer(
            chat_id=update.effective_chat.id,
            text="📈 Извините, на сегодня вы записали максимальное количество слов.",
        )
        return
    await answer(
        chat_id=update.effective_chat.id,
        text="""
🚀 Введие слово или выражение на английском\nкоторое хотите сохранить и для которого далее напишите перевод.\n\n
🇬🇧 Слово/выражение должно содержать только английские буквы и знаки пробела.
        """,
    )

    return WordField.ENG_WORD.value


async def receive_eng_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receiving new word and save them
    Asking write translating the word
    """

    word = update.effective_message.text
    state = State(update)
    state.set_data(eng_word=word)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
👍 Отлично!\n\n🇷🇺 Теперь введите перевод на русском для слова - {word.capitalize()}.\n\n\
❗ Перевод должен содержать только русские буквы и знаки пробела.
""",
    )

    return WordField.TRANSlATE.value


async def incorrectly_eng_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
⚠️ Ввод не корректный, попробуйте еще раз.\n\n
🔴 Для завершения процесса /cancel
""",
    )

    state = State(update)
    user_data = state.get_data()

    if not user_data:
        return WordField.ENG_WORD.value
    return WordField.TRANSlATE.value


async def receive_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receiving translate the word
    Saving the word and the translate in database
    """

    translate = update.effective_message.text
    state = State(update)
    state.set_data(translate=translate)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ Прекрасно! Можете взглянуть на свой словарь /words",
    )

    CreateWord(str(update.effective_user.id), **state.get_data())
    state.clear_data()
    return ConversationHandler.END


async def command_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = State(update)
    state.clear_data()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"❌ Процесс прерван.",
    )

    return ConversationHandler.END


HANDLER_CREATE_NEW_WORD = ConversationHandler(
    entry_points=[
        CommandHandler(command=CommandEnum.NEW.value, callback=command_new_word)
    ],
    states={
        WordField.ENG_WORD.value: [
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
        WordField.TRANSlATE.value: [
            MessageHandler(
                filters=filters.TEXT
                & ~filters.COMMAND
                & filters.Regex(r"^[ёЁА-Яа-я\s]+$"),
                callback=receive_translate,
            ),
            MessageHandler(
                filters=filters.ALL & ~filters.COMMAND, callback=incorrectly_eng_word
            ),
        ],
    },
    fallbacks=[
        CommandHandler(command=CommandEnum.CANCEL.value, callback=command_cancel)
    ],
)
