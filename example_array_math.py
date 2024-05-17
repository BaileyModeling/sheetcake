from sheetcake import Array, Cell, BeginningBalance, EndingBalance
from sheetcake import fmt
from datetime import date


if __name__ == '__main__':
    from sheetcake import DateArray, dates
    # a = Array.from_values(values=(-100, 0, 100), name='a')
    # b = Cell(10, "b")
    # array = a - b - b
    # array.print_formulas(deep=True)
    # print("="*80)
    # array.print_value_audit(deep=True)
    # print("="*80)
    # array.print()
    DURATION = 3
    date_array = DateArray("2023-11-01", DURATION)
    exit_date = date(2023,12,15)

    bbal = BeginningBalance.zeros(DURATION, fmt=fmt.accounting)
    adv = Array.from_values(values=(1154930.3, 1859155.05, 1859155.05), name='Advances', fmt=fmt.accounting)
    int_rt = Cell(0.074, "Interest Rate", fmt=fmt.percent)
    bank_days = Cell(360, "Bank Days")
    # monthly_rt = int_rt / 12
    daily_rt = int_rt / bank_days
    date_array.days
    days_prorated = Array.from_values(values=date_array.prorated_days(exit_date), name="Prorated Days in Month")

    monthly_rt = Array.blank(DURATION, name="Monthly Rate")
    monthly_rt.equal_item(daily_rt).mult_item(days_prorated)

    interest = Array.zeros(DURATION, name="Interest", fmt=fmt.accounting)
    interest.equal_item(bbal).mult_item(monthly_rt)

    ebal = EndingBalance.sum([bbal, adv, interest], name='Ending Balance', fmt=fmt.accounting)
    bbal.connect_ending_balance(ebal)

    print("="*80)
    bbal.print_formulas(deep=False)
    print("="*80)
    bbal.print_value_audit(deep=False)
    print("="*80)

    print("="*80)
    interest.print_formulas(deep=False)
    print("="*80)
    interest.print_value_audit(deep=False)
    print("="*80)

    print("="*80)
    ebal.print_formulas(deep=False)
    print("="*80)
    ebal.print_value_audit(deep=False)
    print("="*80)

    print("="*80)
    bbal.print()
    interest.print()
    ebal.print()
