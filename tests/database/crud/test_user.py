from pymongo.collection import Collection

from engbot.models.users import User
from engbot.database.main_database.repositories.users import (
    CreateUser,
    DetailUser,
    ListUser,
    UpdateUser,
)


class TestCreate:
    def test_create_user_positive(self, database: Collection, test_user_data: dict):
        user = User(
            telegram_id=test_user_data.get("telegram_id"),
            username=test_user_data.get("username"),
            language_code=test_user_data.get("language_code"),
        )

        user = CreateUser(user_model=user)

    def test_create_user_negative(self, database: Collection, test_user_data: dict):
        ...


class TestDetail:
    def test_get_one_user(self, database: Collection, test_user_data: dict):
        detail = DetailUser(telegram_id=test_user_data.get("telegram_id"))
        user = detail()

        assert type(user) == dict

        assert user.get("telegram_id") == test_user_data.get("telegram_id")
        assert user.get("username") == test_user_data.get("username")
        assert user.get("language_code") == test_user_data.get("language_code")
