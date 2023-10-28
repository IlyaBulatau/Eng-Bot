from config import Config
from database.base import Database

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database as DB


class MongoDB(Database):
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

    @property
    def collection(self):
        return self.__collection
