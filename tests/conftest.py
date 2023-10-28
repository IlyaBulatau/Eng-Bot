from engbot.config import Config
from engbot.database.mongo.mongodb import MongoDB
from pymongo.collection import Collection

import pytest


@pytest.fixture(scope="session")
def database() -> Collection:
    
    db: Collection = MongoDB().collection
    yield db
    db.database.client.drop_database(Config.MONGO_DB_NAME)


@pytest.fixture(scope="session")
def test_data(database) -> dict:
    data = {
        "test": "OK"
    }
    yield data
