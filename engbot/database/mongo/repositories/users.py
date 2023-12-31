from pymongo.collection import Collection
from engbot.models.users import User, UserField
from engbot.database.mongo.mongodb import MONGO_ID_FIELD


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

    user: dict = collection.find_one(kwargs)

    # remove _id key from dict
    user.pop(MONGO_ID_FIELD)

    return user


def get_user_by_telegram_id(collection: Collection, telegram_id: str | int) -> User:
    """
    Return dict with user data
    """
    user_dict: dict = get_user_by_argument(collection, telegram_id=str(telegram_id))
    user_dict.pop(UserField.WORDS.value)
    user = User(**user_dict)

    return user


def get_all_user(collection: Collection) -> list[str]:
    """
    Return list of user telegram ID
    """
    pipline = [
        {
            "$match": {UserField.TELEGRAM_ID.value: {"$exists": 1}}
        },
        {
            "$project": {UserField.TELEGRAM_ID.value: 1, MONGO_ID_FIELD: 0}
        }
    ]
    dict.keys
    data_fom_mongo = collection.aggregate(pipline)
    result: list[str] = [dicts.get(UserField.TELEGRAM_ID.value) for dicts in data_fom_mongo]
    return result


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
