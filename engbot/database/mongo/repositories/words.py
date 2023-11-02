from pymongo.collection import Collection

from datetime import date

from engbot.utils.helpers import convert_date_to_string
from engbot.models.words import WordList, Word, WordListField
from engbot.models.users import UserField
from engbot.database.mongo.repositories.users import get_user_by_telegram_id


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
        upsert=True,
        filter={UserField.TELEGRAM_ID.value: telegram_id},
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
    
    list_words_by_dates: list[WordList] = get_user_by_telegram_id(
        collection=collection, telegram_id=telegram_id
    )
    
    return list_words_by_dates
