from engbot.config import Config
from abc import abstractmethod, ABC


class BaseDatabase(ABC):
    """
    Base class for database classes
    """

    def __init__(self):
        self.__url = Config.DATABASE_URL

    @property
    def url(self):
        return self.__url

    @abstractmethod
    def create_database(self):
        ...


    @abstractmethod
    def drop_database(self):
        ...


    @abstractmethod
    def get_connection(self):
        ...    
