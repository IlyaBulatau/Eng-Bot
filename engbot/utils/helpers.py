from datetime import date


def convert_date_to_string(date: date) -> str:
    """
    Convert date object to string object
    """
    _format = "%-d.%m.%Y"
    result: str = date.strftime(_format)
    
    return result
