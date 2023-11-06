from engbot.handlers.commands.assemble import assemble_commands
from engbot.handlers.message.create_new_word.handlers import HANDLER_CREATE_NEW_WORD
from engbot.handlers.message.work_with_words import handlers
from engbot.handlers.chats.handlers import track_chats_memer, track_my_member
from engbot.utils.helpers import accept_callback_arrows, accept_callback_language_type

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ChatMemberHandler,
    MessageHandler,
    filters,
)


def setup_handlers(application: Application):
    application.add_handler(
        ChatMemberHandler(
            callback=track_my_member, chat_member_types=ChatMemberHandler.MY_CHAT_MEMBER
        )
    )
    application.add_handler(
        ChatMemberHandler(
            callback=track_chats_memer, chat_member_types=ChatMemberHandler.CHAT_MEMBER
        )
    )
    application.add_handler(HANDLER_CREATE_NEW_WORD)
    assemble_commands(application)
    application.add_handler(
        CallbackQueryHandler(
            callback=handlers.callback_arrows, pattern=accept_callback_arrows
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            callback=handlers.callback_language_buttom,
            pattern=accept_callback_language_type,
        )
    )
    application.add_handler(CallbackQueryHandler(callback=handlers.empty_callback))
    application.add_handler(
        MessageHandler(filters=filters.ALL, callback=handlers.echo_message)
    )
