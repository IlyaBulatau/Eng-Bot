from engbot.services.cache.states import CacheBotGroup

from telegram.ext import ExtBot
from telegram import Update, Chat
from telegram.constants import ChatMemberStatus as CS


class ChatController:
    """
    Tracking that user is member group
    """

    def __init__(self, update: Update, bot: ExtBot):
        self.update: Update = update
        self.bot: ExtBot = bot
        self.user_id: str = str(self.update.effective_user.id)

    async def control(self) -> list[tuple[str]]:
        """
        if user is not member group
        return list of (title, link) there groups
        """
        # getting all groups of the bot from cache
        cache = CacheBotGroup(self.update)
        groups: list[str] | list = cache.get_groups()

        result = []
        for group_id in groups:
            event = await self.bot.get_chat_member(
                chat_id=group_id, user_id=self.user_id
            )
            if event.status not in (CS.ADMINISTRATOR, CS.MEMBER, CS.OWNER):
                chat: Chat = await self.bot.get_chat(chat_id=group_id)
                result.append((chat.title, chat.invite_link))

        return result
