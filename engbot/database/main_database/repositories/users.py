from engbot.models.users import User
from engbot.database.main_database.repositories.base import CreateBase, DetailBase
from engbot.database.mongo.repositories.users import (
    get_user_by_telegram_id,
    create_user,
    get_all_user,
)


class DetailUser(DetailBase):
    """
    Class for getting information about user from database
    """

    def __call__(self, *args, **kwargs) -> User:
        user: User = get_user_by_telegram_id(
            collection=self.connection, telegram_id=str(self.telegram_id)
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


class ListUser(DetailBase):
    """
    Class for getting all users from DB
    Return list of user telegram ID
    """

    def __call__(self, offset: int = 0, limit: str = 1000, *args, **kwargs) -> list[str]:
        list_of_user_id: list[str] = get_all_user(self.connection)

        return list_of_user_id[offset:limit]
    


class UpdateUser:
    ...
