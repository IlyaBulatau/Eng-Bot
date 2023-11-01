from pydantic import BaseModel, validator
from engbot.models.words import DateCreated

from enum import Enum


class User(BaseModel):
    """
    Representing user model
    """

    telegram_id: str | int
    username: str
    language_code: str
    words: DateCreated | None = None

    @validator("telegram_id", "username", "language_code")
    def validate_all_fields(cls, kwargs):
        """
        Enum class in this module must match with this class
        """
        self_fields = set(User.model_fields.keys())
        enum_fields = set(elem.value for elem in tuple(UserField))
        
        if len(self_fields.intersection(enum_fields)) != len(enum_fields):
            raise Exception("Fileds in model and enum class must match")
        return kwargs
        

    @validator("telegram_id")
    def telegram_id_validate(cls, telegram_id: int | str) -> str:
        if isinstance(telegram_id, int):
            return str(telegram_id)
        elif isinstance(telegram_id, str) and telegram_id.isdigit():
            return telegram_id
        else:
            raise Exception(
                "Telegram id must be is integer or is a string contain only integer"
            )


class UserField(Enum):
    TELEGRAM_ID: str = "telegram_id"
    USERNAME: str = "username"
    LANGUAGE_CODE: str = "language_code"
    WORDS: str =  "words"
