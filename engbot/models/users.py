from pydantic import BaseModel, validator
from engbot.models.words import DateCreated


class User(BaseModel):
    """
    Representing user model
    """

    telegram_id: str | int
    username: str
    language_code: str
    words: DateCreated | None = None

    @validator("telegram_id")
    def telegram_id_validate(cls, telegram_id: int | str) -> str:
        if isinstance(telegram_id, int):
            return telegram_id
        elif isinstance(telegram_id, str) and telegram_id.isdigit():
            return telegram_id
        else:
            raise Exception(
                "Telegram id must be is integer or is a string contain only integer"
            )
