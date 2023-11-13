from engbot.config import Config
from engbot.tasks.scheduler import scheduler
from engbot.tasks import constants as con
from engbot.models.words import WordList, WordListField, WordField
from engbot.database.main_database.repositories.users import ListUser
from engbot.database.main_database.repositories.words import ListWord
from engbot.tasks.constants import TEXT_FOR_ASKING, TIME_ASKING_TRANSLATE

from random import choice
import asyncio
from random import choice
from typing import Callable

from celery.schedules import crontab
from telegram import Bot


@scheduler.task(expire=con.EXPIRE_TIME_TO_NOTICE_LEARN)
def notice_user_about_learn(user_telegram_id: str | int):
    """
    Task implementation
    """
    asyncio.run(_notice_about_learn(user_telegram_id))


@scheduler.task(expire=con.EXPIRE_TIME_TO_ASKING_TRANSLATE)
def asking_translate():
    """
    Task implementation
    """
    get_users: Callable = ListUser()
    list_of_user_id: list[str] = get_users()

    for user_id in list_of_user_id:
        try:
            asyncio.run(_asking_translate(user_id))
        except:
            # add logging
            ...


async def _notice_about_learn(user_telegram_id: str | int):
    """
    Sends notice to user about learn
    """
    bot = Bot(Config.BOT_TOKEN)

    await bot.send_message(
        chat_id=str(user_telegram_id),
        text=choice(con.TEXT_FOR_NOTICE),
    )


async def _asking_translate(user_telegram_id: str | int):
    bot = Bot(Config.BOT_TOKEN)

    get_words = ListWord(user_telegram_id)
    
    if not get_words:
        # if user doesn't have words
        await bot.send_message(
            chat_id=str(user_telegram_id),
            text="👋 Хей, вы еще не записали ни одного слова.\n\n📚 Let's go study! /words"
        )
        return
      
    words_on_date: WordList = choice(get_words())
    list_of_dict: list[dict] = words_on_date.model_dump().get(WordListField.WORDS.value)
    word: dict = choice(list_of_dict)

    await bot.send_message(
        chat_id=str(user_telegram_id),
        text=TEXT_FOR_ASKING.format(
            eng_word=word.get(WordField.ENG_WORD.value.capitalize())
        ),
        parse_mode="Markdown",
    )  # TODO - make the answer contain spoiler text - || transalte ||


scheduler.conf.beat_schedule = {
    "setup-task-on-once-day": {
        "task": "engbot.tasks.tasks.asking_translate",
        "schedule": crontab(
            hour=TIME_ASKING_TRANSLATE.get("hour", 17),
            minute=TIME_ASKING_TRANSLATE.get("minute", 30),
        ),
    }
}
