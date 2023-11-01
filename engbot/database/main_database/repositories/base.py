from dotmap import DotMap
from pymongo.collection import Collection

from abc import ABC, abstractmethod

from engbot.database.main_database.db import Database


class BaseCRUD(ABC):
    """
    Base model for CRUD operations

    Containe connection to database
    """

    @abstractmethod
    def __init__(self):
        self.connection: Collection = Database().get_connection()


class DetailBase(BaseCRUD):
    """
    Base class for getting information

    Receive user telegram_id
    """

    def __init__(self, telegram_id: str | int | None = None, **kwargs) -> None:
        super().__init__()
        self.telegram_id = telegram_id

    @abstractmethod
    def __call__(self, *args, **kwargs) -> DotMap:
        ...


class CreateBase(BaseCRUD):
    """
    Base class for creating
    """

    @abstractmethod
    def __call__(self, *args, **kwargs) -> None:
        ...
