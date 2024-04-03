from sheetcake import fmt
from datetime import date


def test_accounting():
    assert fmt.accounting(1234567.89) == "   1,234,567.89"


def test_currency2():
    assert fmt.currency2(1234567.89) == "$1,234,567.89"


def test_comma():
    assert fmt.comma(1234567.89) == "1,234,568"


def test_comma2():
    assert fmt.comma2(1234567.89) == "1,234,567.89"


def test_percent():
    assert fmt.percent(0.123456789) == "12.35%"


def test_percentage():
    assert fmt.percentage(0.123456789) == "12.35%"


def test_accounting_string_input():
    assert fmt.accounting("1234567.89") == "1234567.89"


def test_currency2_string_input():
    assert fmt.currency2("1234567.89") == "1234567.89"


def test_comma_string_input():
    assert fmt.comma("1234567.89") == "1234567.89"


def test_comma2_string_input():
    assert fmt.comma2("1234567.89") == "1234567.89"


def test_percent_string_input():
    assert fmt.percent("0.123456789") == "0.123456789"


def test_accounting_string_none():
    assert fmt.accounting(None) == ""


def test_currency2_string_none():
    assert fmt.currency2(None) == ""


def test_comma_string_none():
    assert fmt.comma(None) == ""


def test_comma2_string_none():
    assert fmt.comma2(None) == ""


def test_percent_string_none():
    assert fmt.percent(None) == ""


def test_date():
    assert fmt.date(date(2020, 12, 31)) == "12/31/2020"


def test_date_none():
    assert fmt.date(None) == ""


def test_mmddyy():
    assert fmt.mmddyy(date(2020, 12, 31)) == "12/31/20"


def test_mmddyy_none():
    assert fmt.mmddyy(None) == ""


def test_yyyymmdd():
    assert fmt.yyyymmdd(date(2020, 12, 31)) == "2020-12-31"


def test_yyyymmdd_none():
    assert fmt.yyyymmdd(None) == ""
