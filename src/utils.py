from decimal import Decimal


def is_number(obj):
    if isinstance(obj, (int, float, Decimal)):
        return True
    else:
        return False


def get_value(obj, default=None):
    if hasattr(obj, 'value'):
        return obj.value
    elif is_number(obj):
        return obj
    else:
        return default
