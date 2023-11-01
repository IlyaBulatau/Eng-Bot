from dotmap import DotMap

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
    
    def __call__(self, *args, **kwargs) -> DotMap:

        user: dict = get_user_by_argument(
            collection=self.connection, telegram_id=self.telegram_id, **kwargs
        )
        # remove _id key from dict
        user.pop("_id")

        user_obj = DotMap(user)

        self.user_data: dict = user_obj

        return user_obj



class CreateUser(CreateBase):
    """
    Class for creating new user in database
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
