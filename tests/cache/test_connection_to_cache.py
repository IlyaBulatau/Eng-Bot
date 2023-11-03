from redis import Redis

import pytest


@pytest.fixture(scope="module")
def test_cache_data(cache_obj: Redis) -> dict:
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

    def test_insert_data(self, test_cache_data: dict, cache_obj: Redis):
        """
        Test insert process
        """
        first_key: str = next(iter(test_cache_data))
        value: str = test_cache_data.get(first_key)

        cache_obj.set(name=first_key, value=value)

    def test_get_data(self, test_cache_data: dict, cache_obj: Redis):
        """
        Test getting process
        """

        first_key: str = next(iter(test_cache_data))

        assert cache_obj.get(first_key) == test_cache_data.get(first_key)
