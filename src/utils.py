from decimal import Decimal
import numpy as np


def is_number(value) -> bool:
    """
    Return True if the value is a number, False otherwise.
    """
    if isinstance(value, (int, float, Decimal, np.floating, np.int, np.float, np.complex, )):
        return True
    if str(type(value)).startswith("<class 'numpy."):
        return True
    return False


def is_iterable(value) -> bool:
    """
    Return True if the value is an iterable, False otherwise.
    """
    try:
        iter(value)
        return True
    except TypeError:
        return False


def get_value(obj, default=None):
    if hasattr(obj, 'value'):
        return obj.value
    elif is_number(obj):
        return obj
    else:
        return default
