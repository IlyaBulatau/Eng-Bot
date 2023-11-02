from engbot.database.main_database.repositories.base import CreateBase, DetailBase
from engbot.models.words import Word, WordList
from engbot.database.mongo.repositories.words import (
    create_word_of_user,
    get_all_words_of_user,
)


class DetailWord(DetailBase):
    ...


class ListWord(DetailBase):
    """
    Class for showing all user words
    """

    def __call__(self, *args, **kwargs) -> list[WordList]:
        list_words_by_dates: list[WordList] = get_all_words_of_user(
            collection=self.connection,
            telegram_id=self.telegram_id,
        )

        return list_words_by_dates


class CreateWord(CreateBase):
    """
    Class for creating new word of user

    Receiving kwargs it must be containe data for creating 'Word' object
    :Look 'WordField' class
    """

    def __init__(self, user_telegram_id: str | int, **kwargs) -> None:
        super().__init__()
        self.user_telegram_id: str | int = user_telegram_id
        self.__call__(**kwargs)

    def __call__(self, *args, **kwargs) -> None:
        create_word_of_user(
            collection=self.connection,
            telegram_id=self.user_telegram_id,
            word=Word(**kwargs),
        )
