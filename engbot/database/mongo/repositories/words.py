from pymongo.collection import Collection

from datetime import date

from engbot.utils.helpers import (
    convert_date_to_string,
    reform_from_string_to_string_of_date,
)
from engbot.models.words import WordList, Word, WordListField, WordField
from engbot.models.users import UserField
from engbot.database.mongo.repositories.users import get_user_by_argument
from engbot.database.mongo.mongodb import MONGO_ID_FIELD


def create_word_of_user(
    collection: Collection, telegram_id: str | int, word: Word
) -> None:
    """
    Create word in mongoDB with datetime key
    if the data not exists, created and insert this data
    """
    date_today = convert_date_to_string(date.today())
    created_on = {WordListField.CREATED_ON.value: {date_today: []}}
    new_word: dict[str, str] = word.model_dump()

    # if not date today in database
    collection.update_one(
        upsert=False,
        filter={
            UserField.TELEGRAM_ID.value: telegram_id,
            f"{UserField.WORDS.value}.{WordListField.CREATED_ON.value}.{date_today}": {
                "$exists": 0
            },
        },
        update={"$addToSet": {UserField.WORDS.value: created_on}},
    )

    # set the word in collection
    collection.update_one(
        upsert=False,
        filter={
            UserField.TELEGRAM_ID.value: telegram_id,
            f"{UserField.WORDS.value}.{WordListField.CREATED_ON.value}.{date_today}": {
                "$exists": 1
            },
        },
        update={
            "$addToSet": {
                f"{UserField.WORDS.value}.$.{WordListField.CREATED_ON.value}.{date_today}": new_word
            }
        },
    )


def get_all_words_of_user(
    collection: Collection, telegram_id: str | int
) -> list[WordList]:
    user_dict: dict = get_user_by_argument(
        collection=collection, telegram_id=str(telegram_id)
    )
    list_words_in_date: list[
        dict[str, dict[str, list[dict[str, str]]]]
    ] = user_dict.get(UserField.WORDS.value)

    if not user_dict.get(UserField.WORDS.value):
        return None

    words: list[WordList] = [
        WordList(
            created_on=reform_from_string_to_string_of_date(date),
            words=[
                Word(  # create words objects
                    eng_word=translate_dict.get(WordField.ENG_WORD.value),
                    translate=translate_dict.get(WordField.TRANSlATE.value),
                )
                for translate_dict in dict_word  # getting every set of words by 'this' date
            ],
        )
        for dates in list_words_in_date[
            ::-1
        ]  # get WordListField.CREATED_ON.value in reverse list
        for dict_date_in_word in dates.values()  # getting dict with date - key and set of wod - value
        for date, dict_word in dict_date_in_word.items()  # this key valye
    ]

    return words


def count_words_of_day_in_array(
    collection: Collection, telegram_id: str | int
) -> int | None:
    """
    Getting count words of current day of user from mongodb

    Process:
    In first - getting data by telegram ID and date today,
    then keeping only field 'words',
    furth created dict with key of 'words' nad value of list of list of words,
    and finally remove inner list and getting size of list
    """
    created_on_key: str = convert_date_to_string(date.today())

    pipline = [
        {  # get data by telegram ID
            "$match": {UserField.TELEGRAM_ID.value: str(telegram_id)},
        },
        {  # get data by date today
            "$match": {
                f"{UserField.WORDS.value}.{WordListField.CREATED_ON.value}.{created_on_key}": {
                    "$exists": 1
                },
            }
        },  # get only field of words
        {"$project": {UserField.WORDS.value: 1, MONGO_ID_FIELD: 0}},
        {  # create dict with key 'words' and value list of words
            "$group": {
                MONGO_ID_FIELD: 0,
                UserField.WORDS.value: {
                    "$first": f"${UserField.WORDS.value}.{WordListField.CREATED_ON.value}.{created_on_key}"
                },
            }
        },
        {  # get first element from list of words
            "$project": {
                MONGO_ID_FIELD: 0,
                f"{UserField.WORDS.value}": {"$first": f"${UserField.WORDS.value}"},
            }
        },
        {  # get size of list
            "$project": {
                MONGO_ID_FIELD: 0,
                f"{UserField.WORDS.value}": {"$size": f"${UserField.WORDS.value}"},
            }
        },
    ]

    data_from_mongo = collection.aggregate(pipline)
    # get result
    list_of_result: list = [dicts for dicts in data_from_mongo]
    result: dict | None = list_of_result[0] if list_of_result else None

    return int(result.get(UserField.WORDS.value, None)) if result else None