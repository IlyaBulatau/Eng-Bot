from engbot.config import Config
from engbot.database.base import BaseDatabase

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database as DB


class MongoDB(BaseDatabase):
    def __init__(self):
        super().__init__()
        self.__DATABASE_NAME = Config.MONGO_DB_NAME
        self.__COLLECTION_NAME = Config.MONGO_COLLECTION_NAME
        self.__collection: Collection = self._connect_to_collection()

    def _connect_to_collection(self) -> Collection:
        client = MongoClient(self.url)
        database: DB = client[self.__DATABASE_NAME]
        collection: Collection = database[self.__COLLECTION_NAME]

        return collection
    

    def create_database(self, database_name:str=None) -> None:
        """
        Create mongodb database
        """
        if database_name:
            self.__DATABASE_NAME: DB = database_name


    def drop_database(self, database_name:str=None) -> None:
        """
        Delete mongodb database
        """
        name: str = database_name if database_name else self.__DATABASE_NAME
        self.__collection.database.client.drop_database(name)


    def get_connection(self) -> Collection:
        """
        Return connection to mongodb collection
        """
        return self.collection

    @property
    def collection(self):
        return self.__collection
