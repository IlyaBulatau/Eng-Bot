from pydantic import BaseModel, validator

from datetime import date
from enum import Enum

from engbot.utils.helpers import intersection_model_and_enum


class Word(BaseModel):
    """
    Representing word model

    Changing to capital words
    """

    eng_word: str
    translate: str

    @validator("eng_word", "translate")
    def validate_all_fields(cls, kwargs):
        intersection_model_and_enum(Word, WordField)
        return kwargs


class WordList(BaseModel):
    """
    Object date created words
    """

    created_on: date = date.today()
    words: list[Word]

    @validator("created_on", "words")
    def validate_all_fields(cls, kwargs):
        intersection_model_and_enum(WordList, WordListField)
        return kwargs


class WordField(Enum):
    ENG_WORD: str = "eng_word"
    TRANSlATE: str = "translate"


class WordListField(Enum):
    CREATED_ON: str = "created_on"
    WORDS: str = "words"
