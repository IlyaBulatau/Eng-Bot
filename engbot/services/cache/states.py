from telegram import Update

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

    def get_groups(self) -> list[str] | list:
        """
        Getting all groups of bot
        where his is admin
        """
        str_of_groups_list = self.storage.get(self.cache_key)
        if not str_of_groups_list:
            return []

        list_of_group: list = self._groups_to_list(str_of_groups_list)

        if not list_of_group:
            return []

        return list_of_group

    def set_group(self, telegram_group_id) -> None:
        """
        Added new group for bot
        """
        groups: list[str] | list = self.get_groups()

        if str(telegram_group_id) in groups:
            return

        groups.append(str(telegram_group_id))

        save_obj: str = self._groups_to_str(groups)
        self.storage.set(self.__cache_key, save_obj)

    def remove_group(self, telegram_group_id) -> None:
        """
        Removed group for bot
        """
        groups: list[str] | list = self.get_groups()

        if not str(telegram_group_id) in groups:
            return

        groups.remove(str(telegram_group_id))

        save_obj: str = self._groups_to_str(groups)
        self.storage.set(self.__cache_key, save_obj)

    def _groups_to_str(self, list_of_str: list[str]) -> str:
        """
        Receive list of str
        Return string
        Example: [1, 2, 3] => '[1, 2, 3]'
        """
        return str(list_of_str)

    def _groups_to_list(self, string: str) -> list[str] | list:
        """
        Getting a string as a list of strings
        Return list of strings
        Example: '[1, 2, 3]' => [1, 2, 3]
        """
        new_string: str = string[1:-1]  # remove []
        if new_string.strip() == "":
            return []
        list_of_str: list[str] = new_string.split(", ")
        result: list[str] = [item[1:-1] for item in list_of_str]  # remove quotes

        return result
