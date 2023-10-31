from redis import Redis
from telegram.ext import ContextTypes
from telegram import Update

from engbot.services.cache.storage import redis_cli


SEC_TTL = 86400


class State:
    def __init__(self, update: Update):
        self.storage: Redis = redis_cli

        if not isinstance(update, Update):
            raise Exception("update object must be Update instance")
        self.update: Update = update
        self.user_id: str = str(self.update.effective_user.id)
        self.ttl = SEC_TTL

    def set_data(self, **kwargs) -> None:
        """
        Save data in storage
        """

        self.storage.set(self.user_id, kwargs, self.ttl)

    def get_data(self) -> dict | None:
        data = self.storage.get(self.user_id)

        return data if data else None

    def clear_data(self):
        self.storage.delete(self.user_id)
