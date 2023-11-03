from datetime import date
from pydantic import BaseModel
from enum import Enum

from engbot.utils.callback_datas import RIGHT_BUTTOM, LEFT_BUTTOM


DATE_FORMAT = "%d%m%Y"


def convert_date_to_string(date: date) -> str:
    """
    Convert date object to string object

    Returning date in formatt d02112023 corresponds 02-11-2023

    Some databases don't allow put date or string that start with numbers
    Thus this function returning date that in this format
    """
    result: str = date.strftime(DATE_FORMAT)

    return "d" + result


def reform_from_string_to_string_of_date(string_of_date: str) -> str:
    """
    Reform from d02112023 to 02-11-2023
    """
    sod = string_of_date[1:]  # remove first letter 'd'
    result = sod[:2] + "-" + sod[2:4] + "-" + sod[4:]  # addition result
    return result


def intersection_model_and_enum(obj_model: BaseModel, obj_enum: Enum):
    """
    Enum class must match with model class
    """

    self_fields = set(obj_model.model_fields.keys())
    enum_fields = set(elem.value for elem in tuple(obj_enum))

    if len(self_fields.intersection(enum_fields)) != len(enum_fields):
        raise Exception(
            f"Fileds in model and enum class must match\n\nModel: {obj_model.__name__}, Enum: {obj_enum.__name__}"
        )


def accept_callback_arrows(callback_data: str):
    """
    Checking what the callback data for arrows menu is equal to
    """
    return True if callback_data == RIGHT_BUTTOM or LEFT_BUTTOM else False
