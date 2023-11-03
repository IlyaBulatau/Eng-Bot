from pymongo.collection import Collection

from engbot.models.users import User
from engbot.models.users import UserField
from engbot.database.main_database.repositories.users import (
    CreateUser,
    DetailUser,
)


class TestCreate:
    def test_create_user_positive(self, database: Collection, test_user_data: dict):
        user = User(
            telegram_id=test_user_data.get(UserField.TELEGRAM_ID.value),
            username=test_user_data.get(UserField.USERNAME.value),
            language_code=test_user_data.get(UserField.LANGUAGE_CODE.value),
        )

        user = CreateUser(user_model=user)

    def test_create_user_negative(self, database: Collection, test_user_data: dict):
        ...


class TestDetail:
    def test_get_one_user(self, database: Collection, test_user_data: dict):
        detail = DetailUser(telegram_id=test_user_data.get(UserField.TELEGRAM_ID.value))
        user = detail()

        assert type(user) == User

        assert user.telegram_id == test_user_data.get(UserField.TELEGRAM_ID.value)
        assert user.username == test_user_data.get(UserField.USERNAME.value)
        assert user.language_code == test_user_data.get(UserField.LANGUAGE_CODE.value)
