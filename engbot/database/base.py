from engbot.config import Config


class BaseDatabase:
    """
    Base class for database classes
    """

    def __init__(self):
        self.__url = Config.DATABASE_URL

    @property
    def url(self):
        return self.__url
