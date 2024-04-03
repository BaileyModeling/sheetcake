from sheetcake2 import BeginningBalance, EndingBalance, Cell
import pytest


def test_ending_balance_append():
    ebal = EndingBalance.zeros(3)
    ebal.append(Cell(9))
    assert ebal.total == 9
