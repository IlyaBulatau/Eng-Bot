from engbot.services.cache.storage import redis_cli

import pytest


@pytest.fixture(scope="module")
def cache_obj():
    yield redis_cli


@pytest.fixture(scope="module")
def test_cache_data(cache_obj) -> dict:
    """
    Data for test cache sustem
    """
    data = {"testKey": "testValue"}
    yield data
    cache_obj.delete(next(iter(data.keys())))


class TestConnection:
    """
    Test connection to cache sustem
    """

    def test_insert_data(self, test_cache_data: dict):
        """
        Test insert process
        """
        first_key: str = next(iter(test_cache_data))
        value: str = test_cache_data.get(first_key)

        redis_cli.set(name=first_key, value=value)

    def test_get_data(self, test_cache_data: dict):
        """
        Test getting process
        """

        first_key: str = next(iter(test_cache_data))

        assert redis_cli.get(first_key) == test_cache_data.get(first_key)
