from telegram import Update

from engbot.services.cache.storage import BaseStorage


class State(BaseStorage):
    def __init__(self, update: Update):
        super().__init__()

        if not isinstance(update, Update):
            raise Exception("update object must be Update instance")
        self.update: Update = update
        self.user_id: str = str(self.update.effective_user.id)

    def set_data(self, **kwargs) -> None:
        """
        Save data in storage
        """

        self.storage.hmset(self.user_id, kwargs)

    def get_data(self) -> dict | None:
        data = self.storage.hgetall(self.user_id)

        return data if data else None

    def clear_data(self) -> None:
        self.storage.delete(self.user_id)


class CahceCurrentUserPage(BaseStorage):
    CACHE_PREFIX = "cache_current_page"
    CACHE_SEP = ":"

    def __init__(self, user_telegram_id: int | str):
        super().__init__()
        self.telegrm_id: str = str(user_telegram_id)
        self.__cache_key: str = self.CACHE_PREFIX + self.CACHE_SEP + self.telegrm_id
        self.__start_page: int = 0
        self.ttl_sec: int = 2419200  # 1 mounth

    @property
    def cache_key(self):
        return self.__cache_key

    @property
    def start_page(self):
        return self.__start_page

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
        if result == 0:
            return False
        return True

    def update_page(self, amount=0):
        """
        Update key on amount value
        If key not exists - creating the key
        """
        if amount < 0:
            self.storage.decr(self.__cache_key, amount)
        else:
            self.storage.incr(self.__cache_key, amount)
