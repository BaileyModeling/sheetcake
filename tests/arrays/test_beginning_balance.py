from sheetcake2 import BeginningBalance, EndingBalance
import pytest


def test_beginning_balance_unequal_len_raises_error():
    bbal = BeginningBalance.zeros(3)
    ebal = EndingBalance.zeros(4)
    with pytest.raises(Exception):
        bbal.connect_ending_balance(ebal)


def test_beginning_balance_append():
    bbal = BeginningBalance.zeros(3)
    bbal.append(1)
    assert len(bbal) == 4
