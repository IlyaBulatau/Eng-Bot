from pymongo.collection import Collection
from engbot.models.users import User, UserField


MONGO_ID_FIELD = "_id"


def get_user_by_argument(collection: Collection, **kwargs) -> User:
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

    find: dict = collection.find_one(kwargs)

    # remove _id key from dict
    find.pop(MONGO_ID_FIELD)
    user = User(**find)

    return user


def get_user_by_telegram_id(collection: Collection, telegram_id: str | int) -> User:
    """
    Return dict with user data
    """
    user: User = get_user_by_argument(collection, telegram_id=telegram_id)
    return user


def get_all_user(limit: int = None):
    ...


def create_user(collection: Collection, user_model: User) -> None:
    """
    Create new user in Mongodb database
    """
    model: dict = user_model.model_dump()
    telegram_id: str | int = model.get(UserField.TELEGRAM_ID.value)

    if is_do_exists_user(collection, telegram_id=telegram_id):
        return
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

    user = collection.find_one({UserField.TELEGRAM_ID.value: str(telegram_id)})
    if user:
        return True
    return False
