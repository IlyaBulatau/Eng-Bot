from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes

from engbot.services.cache.states import CacheBotGroup


async def track_my_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Tracks update that contains data
    about added of leave the bot from groups

    If bot stating is admin the group
    this  will write in cache
    
    If bot kicked from group or not be is not admin
    this also will writing in cache
    """
    event: ChatMemberUpdated = update.my_chat_member
    status: str = event.new_chat_member.status
    is_admin: bool = True if status in (ChatMember.ADMINISTRATOR, ChatMember.OWNER) else None
    
    group_id = event.chat.id

    cache = CacheBotGroup(update)
    if is_admin:
        cache.set_group(group_id)
    else:
        cache.remove_group(group_id) 


async def track_chats_memer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Trcking adding and lick or leaving user from group where thw bot is an admin
    """
    event = update.chat_member
    