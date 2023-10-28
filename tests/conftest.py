from engbot.config import Config
from engbot.database.mongo.mongodb import MongoDB
from pymongo.collection import Collection

import pytest


@pytest.fixture(scope="session")
def database() -> Collection:
    """
    Return mongodb collection
    And
    drop the database after tests 
    """
    
    db: Collection = MongoDB().collection
    yield db
    db.database.client.drop_database(Config.MONGO_DB_NAME)


@pytest.fixture(scope="session")
def test_data(database) -> dict:
    """
    Create data for tests
    """

    data = {
        "test": "OK"
    }
    yield data
