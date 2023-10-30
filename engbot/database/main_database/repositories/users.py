from typing import Any
from engbot.models.users import User
from engbot.database.main_database.db import Database
from engbot.database.mongo.repositories.users import (
    get_user_by_argument,
    create_user,
)


class DetailUser:
    """
    Class for getting information about user from database
    """

    def __init__(self, telegram_id: str | int | None = None, **kwargs) -> User:
        self.telegram_id = telegram_id

    def __call__(self, *args, **kwargs) -> User:
        connection = Database().collection
        user: dict = get_user_by_argument(
            collection=connection, telegram_id=self.telegram_id, **kwargs
        )
        # remove _id key from dict
        user.pop("_id")

        self.user_data: dict = user

        return user


class CreateUser:
    """
    Class for creating new user in database
    """

    def __init__(self, user_model: User) -> None:
        self.user_model: User = user_model
        self.__call__()

    def __call__(self, *args, **kwargs) -> None:
        connection = Database().get_connection()
        create_user(collection=connection, user_model=self.user_model)


class ListUser:
    ...


class UpdateUser:
    ...
