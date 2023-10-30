from engbot.database.main_database.db import Database
from pymongo.collection import Collection

import pytest


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def test_data(database) -> dict:
    """
    Create data for tests
    """

    data: dict = {"test": "OK"}
    yield data


@pytest.fixture(scope="module")
def test_user_data(database) -> dict:
    """
    Create user data for tests
    """
    data = {"telegram_id": "123", "username": "@bob", "language_code": "en"}
    yield data
