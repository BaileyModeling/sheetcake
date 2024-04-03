from sheetcake2 import Array, Cell, BeginningBalance, EndingBalance
from sheetcake2 import fmt, DateArray, dates
# from rem import DateArray
# from rem.src import dates
from datetime import date


def test_array_interest_calculation():
    DURATION = 3
    date_array = DateArray("2023-11-01", DURATION)
    exit_date = date(2023,12,15)

    bbal = BeginningBalance.zeros(DURATION, fmt=fmt.accounting)
    adv = Array.from_values(values=(1154930.3, 1859155.05, 1859155.05), name='Advances', fmt=fmt.accounting)
    int_rt = Cell(0.074, "Interest Rate", fmt=fmt.percent)
    bank_days = Cell(360, "Bank Days")
    # monthly_rt = int_rt / 12
    daily_rt = int_rt / bank_days
    # date_array.days
    days_prorated = Array.from_values(values=date_array.prorated_days(exit_date), name="Prorated Days in Month")

    monthly_rt = Array.blank(DURATION, name="Monthly Rate")
    monthly_rt.equal(daily_rt).mult(days_prorated)

    interest = Array.zeros(DURATION, name="Interest", fmt=fmt.accounting)
    interest.equal(bbal).mult(monthly_rt)

    ebal = EndingBalance.sum([bbal, adv, interest], name='Ending Balance', fmt=fmt.accounting)
    bbal.connect_ending_balance(ebal)
    assert abs(bbal[2].value - 3_017_408.98) < 0.01
    assert abs(interest[1].value - 3_323.63) < 0.01
    assert abs(ebal[2].value - 4_876_564.03) < 0.01
