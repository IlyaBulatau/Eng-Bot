from engbot.config import Config
from engbot.tasks.scheduler import scheduler
from engbot.tasks import constants as con

import asyncio
from random import choice

from telegram import Bot


async def _notice_about_learn(user_telegram_id: str | int):
    """
    Sends notice to user about learn
    """
    bot = Bot(Config.BOT_TOKEN)

    await bot.send_message(
        chat_id=str(user_telegram_id),
        text=choice(con.TEXT_FOR_NOTICE),
    )


@scheduler.task(expire=con.EXPIRE_TIME_TO_NOTICE_LEARN)
def notice_user_about_learn(user_telegram_id: str | int):
    """
    Implementation send message
    """
    asyncio.run(_notice_about_learn(user_telegram_id))
