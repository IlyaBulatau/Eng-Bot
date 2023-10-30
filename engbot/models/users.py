from pydantic import BaseModel, validator


class User(BaseModel):
    """
    Represeting user model
    """
    telegram_id: str
    username: str
    language_code: str


    @validator("telegram_id")
    def telegram_id_validate(cls, telegram_id: int | str) -> str:
        
        if isinstance(telegram_id, int):
            return telegram_id
        elif isinstance(telegram_id, str) and telegram_id.isdigit():
            return telegram_id
        else:
            raise Exception("Telegram id must be is integer or is a string contain only integer") 