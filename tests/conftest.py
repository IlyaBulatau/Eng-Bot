from engbot.database.main_database.db import Database
from engbot.models.users import UserField
from engbot.models.words import WordField
from engbot.services.cache.storage import redis_cli

from pymongo.collection import Collection

import pytest


@pytest.fixture(scope="session")
def database() -> Collection:
    """
    Return database connect
    And
    drop the database after tests
    """

    db = Database()
    conn: Collection = db.get_connection()
    yield conn
    db.drop_database()


@pytest.fixture(scope="session")
def cache_obj():
    yield redis_cli


@pytest.fixture(scope="session")
def test_data(database) -> dict:
    """
    Create data for tests
    """

    data: dict = {"test": "OK"}
    yield data


@pytest.fixture(scope="session")
def test_user_data(database) -> dict:
    """
    Create user data for tests
    """
    data = {
        UserField.TELEGRAM_ID.value: "123",
        UserField.USERNAME.value: "@bob",
        UserField.LANGUAGE_CODE.value: "en",
    }
    yield data


@pytest.fixture(scope="session")
def test_word_data(database) -> dict:
    """
    Create word for test
    """
    data = {WordField.ENG_WORD.value: "hi", WordField.TRANSlATE.value: "привет"}
    yield data
