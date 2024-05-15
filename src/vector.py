from decimal import Decimal
import numpy as np
from sheetcake import Cell


def is_scalar(value) -> bool:
    """
    Return True if the value is a scalar, False otherwise.
    """
    # return isinstance(value, (Cell, int, float, Decimal))
    if isinstance(value, (Cell, int, float, Decimal, np.floating, np.int, np.float, np.complex, )):
        return True
    if isinstance(value, np.ndarray):
        return False
    if str(type(value)).startswith("<class 'numpy."):
        return True
    return False


def is_vector(value) -> bool:
    """
    Return True if the value is a vector, False otherwise.
    """
    # return isinstance(value, (Array, np.ndarray, list, tuple))
    return hasattr(value, "__iter__")
