from engbot.models.users import User
from engbot.database.main_database.repositories.base import CreateBase, DetailBase
from engbot.database.mongo.repositories.users import (
    get_user_by_argument,
    create_user,
)


class DetailUser(DetailBase):
    """
    Class for getting information about user from database
    """

    def __call__(self, *args, **kwargs) -> User:
        user: User = get_user_by_argument(
            collection=self.connection, telegram_id=self.telegram_id, **kwargs
        )
        return user


class CreateUser(CreateBase):
    """
    Class for creating new user in database

    Receiving kwargs it must be containe data for creating 'User' object
    :Look 'UserField' class
    """

    def __init__(self, user_model: User) -> None:
        super().__init__()
        self.user_model = user_model
        self.__call__()

    def __call__(self, *args, **kwargs) -> None:
        create_user(collection=self.connection, user_model=self.user_model)


class ListUser:
    ...


class UpdateUser:
    ...
