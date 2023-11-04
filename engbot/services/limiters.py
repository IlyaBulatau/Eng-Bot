from engbot.database.main_database.db import Database
from engbot.database.mongo.repositories.words import count_words_of_day_in_array


class WordLimiter:
    """
    Object for tracking limiting quantity words in day

    User don't can create more than QUANTITY_IN_DAY words in day
    """

    QUANTITY_IN_DAY = 10

    def __init__(self):
        self.__connection_to_db = Database().get_connection()

    def is_acceptable(self, telegram_id: str | int):
        """
        Cheking the word count
        """
        quantity: int = count_words_of_day_in_array(
            collection=self.__connection_to_db, telegram_id=telegram_id
        )
        if quantity and quantity >= self.QUANTITY_IN_DAY:
            return False
        return True
