from functools import wraps
from typing import Coroutine

from telegram import Update
from telegram.ext import ExtBot

from engbot.services.controllers.chat_controllers import ChatController


def controller(coro: Coroutine):
    @wraps(coro)
    async def _inner(*args, **kwargs):
        """
        Controller for groups of the bot and tracking users
        """
        update: Update = args[0]
        bot: ExtBot = update.get_bot()

        controller_obj = ChatController(update, bot=bot)
        result = await controller_obj.control()

        if result:
            # if there is groups that the user is not member
            await bot.send_message(
                chat_id=update.effective_chat.id, text="Вы не можете юзать бота"
            )
            # answer to callback data
            if update.callback_query:
                await update.callback_query.answer()
            # delete the message
            await update.message.delete()

            return

        result = await coro(*args, **kwargs)
        return result

    return _inner
