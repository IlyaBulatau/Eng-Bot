from pymongo.collection import Collection
from engbot.models.users import User


def get_user_by_argument(collection: Collection, **kwargs) -> dict:
    """
    Receive arguments, check they, find user by arguments
    Return dict with user data
    """
    model_fields = set(field for field in User.model_fields.keys())
    argumetns = set(arg for arg in kwargs.keys())
    difference = argumetns - model_fields

    if difference != set():
        # if kwargs containse not accepted fields
        raise Exception(
            f"Next arguments {' '.join(difference)} is not valid, accept field: {' '.join(model_fields)}"
        )

    user = collection.find_one(kwargs)

    return user


def get_user_by_telegram_id(collection: Collection, telegram_id) -> dict:
    """
    Return dict with user data
    """
    user: dict = get_user_by_argument(collection, telegram_id=telegram_id)
    return user


def get_all_user(limit: int = None):
    ...


def create_user(collection: Collection, user_model: User) -> None:
    """
    Create new user in Mongodb database
    """
    model: dict = user_model.model_dump()
    telegram_id: str | int = model.get("telegram_id")

    if is_do_exists_user(collection, telegram_id=telegram_id):
        raise Exception(
            f" User with '{telegram_id}' ID is exists in collection '{collection.name}'"
        )
    try:
        collection.insert_one(model)
    except Exception as e:
        ...


def update_user_by_argument():
    ...


def is_do_exists_user(collection: Collection, telegram_id: str | int):
    """
    Check is do exists user with telegram id in Mondo database
    if user is exists - return True
    else - return False
    """

    user = collection.find_one({"telegram_id": str(telegram_id)})
    if user:
        return True
    return False
