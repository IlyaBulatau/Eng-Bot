from redis import Redis

from abc import ABC, abstractmethod

from engbot.config import Config


redis_cli = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)


class BaseStorage(ABC):
    CACHE_PREFIX = ""
    CACHE_SEP = ":"

    def __init__(self):
        self.storage: Redis = redis_cli
        self.__cache_key: str = self.CACHE_PREFIX + self.CACHE_SEP

    @property
    @abstractmethod
    def cache_key(self) -> str:
        return self.__cache_key
