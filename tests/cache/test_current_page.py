import pytest
from redis import Redis

from engbot.services.cache.states import CahceCurrentUserPage


@pytest.fixture(scope="module")
def test_data_cache(cache_obj: Redis):
    """
    Data for test tracking of current page
    """

    data = {"telegram_id": "123456"}
    yield data


@pytest.fixture(scope="module")
def tracker(test_data_cache: dict):
    tr = CahceCurrentUserPage(test_data_cache.get(next(iter(test_data_cache.keys()))))
    yield tr
    print(tr.cache_key)
    tr.storage.delete(tr.cache_key)


class TestCacheCurrentPage:
    def test_is_exists_page_before_set(self, tracker: CahceCurrentUserPage):
        bool_res = tracker.is_exists_page()
        print(tracker.cache_key)
        assert bool_res == False

    def test_set_page(self, tracker: CahceCurrentUserPage):
        tracker.update_page()

        assert tracker.get_current_page() == 0

    def test_update_page(self, tracker: CahceCurrentUserPage):
        tracker.update_page(amount=1)

        assert tracker.get_current_page() == 1

    def test_is_exists_page_after_set(self, tracker: CahceCurrentUserPage):
        bool_res = tracker.is_exists_page()

        assert bool_res == True
