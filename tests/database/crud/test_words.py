from datetime import date, datetime


from pymongo.collection import Collection

from engbot.utils.helpers import DATE_FORMAT
from engbot.models.users import UserField
from engbot.database.main_database.repositories.words import CreateWord, ListWord
from engbot.models.words import Word, WordList, WordField, WordListField


class TestCreate:
    def test_create_word_for_user(
        self, database: Collection, test_user_data: dict, test_word_data: dict
    ):
        telegram_id = test_user_data.get(UserField.TELEGRAM_ID.value)

        CreateWord(user_telegram_id=telegram_id, **test_word_data)

    def test_create_word_for_user_negative(
        self, database: Collection, test_user_data: dict
    ):
        ...


class TestListShow:
    def test_get_all_word_of_user(
        self, database: Collection, test_user_data: dict, test_word_data: dict
    ):
        telegram_id = test_user_data.get(UserField.TELEGRAM_ID.value)
        get_words = ListWord(telegram_id=telegram_id)
        words: list[WordList] = get_words()

        word: Word = words[0].words[0]
        word_to_dict: dict = word.model_dump()

        assert type(words[0]) == WordList
        assert type(word) == Word

        assert "".join(
            words[0].model_dump().get(WordListField.CREATED_ON.value).split("-")
        ) == datetime.strftime(date.today(), DATE_FORMAT)
        assert word_to_dict.get(WordField.ENG_WORD.value) == test_word_data.get(
            WordField.ENG_WORD.value
        )
        assert word_to_dict.get(WordField.TRANSlATE.value) == test_word_data.get(
            WordField.TRANSlATE.value
        )
