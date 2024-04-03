import datetime as dt


def accounting(amount: float) -> str:
    """  1,234,567.89 fixed width"""
    if amount is None or amount == "":
        return ""
    elif isinstance(amount, str):
        return amount
    return "{:>15,.2f}".format(amount)


def currency2(amount: float) -> str:
    """$1,234,567.89"""
    if amount is None or amount == "":
        return ""
    elif isinstance(amount, str):
        return amount
    return "$" + "{:,.2f}".format(amount)


def comma(amount: float) -> str:
    """1,234,567"""
    if amount is None or amount == "":
        return ""
    elif isinstance(amount, str):
        return amount
    return "{:,.0f}".format(amount)


def comma2(amount: float) -> str:
    """1,234,567.89"""
    if amount is None or amount == "":
        return ""
    elif isinstance(amount, str):
        return amount
    return "{:,.2f}".format(amount)


def percent(amount: float) -> str:
    """12.34%"""
    if amount is None or amount == "":
        return ""
    elif isinstance(amount, str):
        return amount
    return "{:,.2f}%".format(amount * 100)


def percentage(*args, **kwargs):
    """Alias for percent()"""
    return percent(*args, **kwargs)


def date(on_date: dt.date) -> str:
    """12/31/2023"""
    if on_date is None:
        return ""
    return on_date.strftime("%m/%d/%Y")


def mmddyyyy(date: dt.date) -> str:
    """12/31/2023"""
    if date is None:
        return ""
    return date.strftime("%m/%d/%Y")


def mmddyy(date: dt.date) -> str:
    """12/31/23"""
    if date is None:
        return ""
    return date.strftime("%m/%d/%y")


def yyyymmdd(date: dt.date) -> str:
    """2023-12-31"""
    if date is None:
        return ""
    return date.strftime("%F")
