from datetime import date
from pydantic import BaseModel
from enum import Enum


def convert_date_to_string(date: date) -> str:
    """
    Convert date object to string object
    """
    _format = "%-d%m%Y"
    result: str = date.strftime(_format)

    return "d" + result


def intersection_model_and_enum(obj_model: BaseModel, obj_enum: Enum):
        """
        Enum class must match with model class
        """

        self_fields = set(obj_model.model_fields.keys())
        enum_fields = set(elem.value for elem in tuple(obj_enum))
        
        if len(self_fields.intersection(enum_fields)) != len(enum_fields):
            raise Exception(f"Fileds in model and enum class must match\n\nModel: {obj_model.__name__}, Enum: {obj_enum.__name__}")
