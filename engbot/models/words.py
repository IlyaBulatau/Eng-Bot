from pydantic import BaseModel, validator

from datetime import datetime


class Word(BaseModel):
    """
    Representing word model

    Changing to capital words
    """

    eng: str
    translate: str


    @validator("eng")
    def eng_to_capitalize(cls, eng: str):
        return eng.capitalize()
    
    
    @validator("translate")
    def eng_to_capitalize(cls, translate: str):
        return translate.capitalize()
    

class DateCreated(BaseModel):
    """
    Object date created words
    """

    created_on: datetime
    words: Word
