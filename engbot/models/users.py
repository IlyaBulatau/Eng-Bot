from pydantic import BaseModel


class User(BaseModel):
    telegram_id: int
    username: str
    language_code: str

