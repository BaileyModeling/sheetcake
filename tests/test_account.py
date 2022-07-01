from sheetcake import Account, Array, zeros
# from sheetcake import Cell
import pytest


@pytest.fixture
def array_a():
    return Array(array=(1, 2, 3), name='a')


@pytest.fixture
def array_b():
    return Array(array=(10, 20, 30), name='b')


@pytest.fixture
def acco():
    array_a = Array(array=(1, 2, 3), name='a')
    array_b = Array(array=(10, 20, 30), name='b')
    return Account(array_a, array_b)


def test_empty_account():
    acco = Account(duration=3)
    assert acco.bbal[0].value == 0
    assert acco.bbal[1].value == 0
    assert acco.bbal[2].value == 0
    assert acco.ebal[0].value == 0
    assert acco.ebal[1].value == 0
    assert acco.ebal[2].value == 0


def test_account_beginning_balance(acco):
    assert acco.bbal[0].value == 0
    assert acco.bbal[1].value == acco.ebal[0].value
    assert acco.bbal[2].value == acco.ebal[1].value


def test_account_ending_balance(acco):
    assert acco.ebal[0].value == 11
    assert acco.ebal[1].value == 33
    assert acco.ebal[2].value == 66


def test_account_ending_balance_updates(array_a, array_b):
    acco = Account(array_a, array_b)
    array_a[0].value = 100
    array_a[1].value = 200
    array_a[2].value = 300
    assert acco.ebal[0].value == 110
    assert acco.ebal[1].value == 330
    assert acco.ebal[2].value == 660


def test_account_add_array(acco):
    array_c = Array(array=(100, 200, 300), name='c')
    acco.add(array_c)
    assert acco.ebal[0].value == 111
    assert acco.ebal[1].value == 333
    assert acco.ebal[2].value == 666


def test_set_initial_balance(acco):
    acco.bbal.set_value(0, 100)
    assert acco.bbal[0].value == 100
    assert acco.ebal[0].value == 111
    assert acco.ebal[1].value == 133
    assert acco.ebal[2].value == 166


def test_if_bbal_is_set_it_will_not_update(array_a, array_b):
    acco = Account(array_a, array_b)
    acco.bbal.set_value(1, 200)
    # acco.bbal[1].value = 200
    array_a[0].value = 100
    assert acco.bbal[1].value == 200

    assert acco.ebal[0].value == 110
    assert acco.ebal[1].value == 222
    assert acco.ebal[2].value == 255


def test_account_no_duration_raises_error():
    with pytest.raises(Exception) as e_info:
        acco = Account()


def test_account_init_diff_length_raises_error():
    array_a = Array(array=(1, 2, 3), name='a')
    array_b = Array(array=(10, 20), name='b')
    with pytest.raises(Exception) as e_info:
        acco = Account(array_a, array_b)


def test_account_add_diff_length_raises_error(acco):
    array_c = Array(array=(10, 20), name='c')
    with pytest.raises(Exception) as e_info:
        acco.add(array_c)


def test_account_arrays(acco: Account):
    assert len(acco.arrays) == 2
