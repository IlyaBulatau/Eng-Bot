from telegram import Update
from telegram.ext import ExtBot
from telegram.error import BadRequest

from engbot.services.cache.storage import BaseStorage


class State(BaseStorage):
    """
    Stores and clears current user data, e.g. conversation with bot
    """

    CACHE_PREFIX = "state_create_word"

    def __init__(self, update: Update):
        super().__init__()

        if not isinstance(update, Update):
            raise Exception("update object must be Update instance")
        self.update: Update = update
        self.user_telegram_id: str = str(self.update.effective_user.id)
        self.__cache_key: str = (
            self.CACHE_PREFIX + self.CACHE_SEP + self.user_telegram_id
        )

    @property
    def cache_key(self):
        return self.__cache_key

    def set_data(self, **kwargs) -> None:
        """
        Save data in storage
        """

        self.storage.hmset(self.__cache_key, kwargs)

    def get_data(self) -> dict | None:
        data = self.storage.hgetall(self.__cache_key)

        return data if data else None

    def clear_data(self) -> None:
        self.storage.delete(self.__cache_key)


class CahceCurrentUserPage(BaseStorage):
    """
    Tracking current page of user
    """

    CACHE_PREFIX = "cache_current_page"

    def __init__(self, user_telegram_id: int | str):
        super().__init__()
        self.user_telegram_id = str(user_telegram_id)
        self.__cache_key: str = (
            self.CACHE_PREFIX + self.CACHE_SEP + self.user_telegram_id
        )
        self.__start_page: int = 0
        self.ttl_sec: int = 2419200  # 1 mounth

    @property
    def cache_key(self):
        return self.__cache_key

    @property
    def start_page(self):
        return self.__start_page

    def set_current_page(self):
        """
        Set current page of user in cache
        """
        self.storage.set(name=self.__cache_key, value=self.__start_page)

    def get_current_page(self):
        """
        Get current page of user from cache
        """
        page = self.storage.get(name=self.__cache_key)
        return int(page)

    def is_exists_page(self):
        """
        Check on exists page in cache for the user
        """
        result: int = self.storage.exists(self.__cache_key)
        if int(result) == 0:
            return False
        return True

    def update_page(self, amount=0, decrease=True):
        """
        Update key on amount value
        If key not exists - creating the key
        """
        if not decrease:
            self.storage.decr(self.__cache_key, int(amount))
        else:
            self.storage.incr(self.__cache_key, int(amount))


class CacheBotGroup(BaseStorage):
    """
    Keeps track of which groups the bot is in
    """

    CACHE_PREFIX = "list_bot_groups"

    def __init__(self, update: Update):
        super().__init__()
        self.update: Update = update
        self.user_telegram_id: str = str(self.update.effective_user.id)
        self.__cache_key: str = self.CACHE_PREFIX

    @property
    def cache_key(self):
        return self.__cache_key

    def get_groups(self) -> list[str] | None:
        """
        Getting all groups of bot
        where his is admin
        """
        groups: list[str] = list(self.storage.smembers(self.cache_key))
        return groups

    def set_group(self, telegram_group_id) -> None:
        """
        Added new group for bot to set in cache
        """
        self.storage.sadd(self.cache_key, str(telegram_group_id))

    def remove_group(self, telegram_group_id) -> None:
        """
        Removed group for bot in cache
        if the group is exists in cache set
        """
        groups: list[str] | None = self.get_groups()

        if groups:
            if str(telegram_group_id) in groups:
                new_list_of_groups: list[str] = groups.remove(str(telegram_group_id))
                self.storage.delete(self.cache_key)
                if new_list_of_groups:
                    self.set_group(str(telegram_group_id))


class CacheLastWordKeyboard(BaseStorage):
    """
    Caching last id of keyboard of words

    If user will usage not current keyboard of words
    the cache which responsibility for current page not correct work

    Thus this cache object will remove last keyboard of words
    when new keyboard will creating and will write ID this keyboard in cache
    """

    CACHE_PREFIX = "last_kb_id"

    def __init__(self, update: Update, bot: ExtBot):
        super().__init__()
        self.bot: ExtBot = bot
        self.user_telegram_id: str = str(update.effective_user.id)
        self.__cache_key: str = (
            self.CACHE_PREFIX + self.CACHE_SEP + self.user_telegram_id
        )

    @property
    def cache_key(self):
        return self.__cache_key

    def save(self, kb_id: str | int) -> None:
        """
        Set kb ID in cache
        """
        self.storage.set(name=self.cache_key, value=str(kb_id))

    async def delete(self) -> None:
        """
        Getting last keybord ID
        And if it exists - delete the keyboard
        """
        kb_id: str | None = self.storage.get(name=self.cache_key)
        if kb_id:
            try:
                await self.bot.delete_message(
                    chat_id=self.user_telegram_id, message_id=str(kb_id)
                )
            except BadRequest as e:
                # add logging
                ...
