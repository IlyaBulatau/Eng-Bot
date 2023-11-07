from engbot.services.cache.states import CacheBotGroup

from telegram.ext import ExtBot
from telegram import Update, Chat
from telegram.constants import ChatMemberStatus as CS, ChatType as CT


class ChatController:
    """
    Tracking that user is member group
    """

    def __init__(self, update: Update, bot: ExtBot):
        self.update: Update = update
        self.bot: ExtBot = bot
        self.user_id: str = str(self.update.effective_user.id)

    async def member_control(self) -> list[tuple[str]] | list:
        """
        if user is not member group
        return list of (title, link) there groups
        """
        # getting all groups of the bot from cache
        cache = CacheBotGroup(self.update)
        groups: list[str] | list = cache.get_groups()
        result: list[tuple[str]] | list = await self._member_control(groups=groups)

        return result

    async def _member_control(self, groups: list[str]):
        result = []
        for group_id in groups:
            event = await self.bot.get_chat_member(
                chat_id=group_id, user_id=self.user_id
            )
            if event.status not in (CS.ADMINISTRATOR, CS.MEMBER, CS.OWNER):
                chat: Chat = await self.bot.get_chat(chat_id=group_id)
                result.append((chat.title, chat.invite_link))

        return result

    def type_chat_control(self) -> bool:
        """
        Return True if the chat is a private or sender
        Else Flase
        """
        type_chat = self.update.effective_chat.type
        if type_chat not in (CT.SENDER, CT.PRIVATE):
            return False
        return True
