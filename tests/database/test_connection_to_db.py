from pymongo.collection import Collection
from pymongo.results import InsertOneResult


class TestConnect:
    def test_insert_one_data(self, database: Collection, test_data: dict):
        """
        Test insert one value in database
        """

        result = database.insert_one(test_data)

        assert type(result) == InsertOneResult

    def test_find_one_data(self, database: Collection, test_data: dict):
        """
        Test find one value on database
        """
        result: dict = database.find_one(test_data)

        key = [key for key in result.keys()][0]
        value = [value for value in result.values()][0]

        assert result.get(key, None) == value
