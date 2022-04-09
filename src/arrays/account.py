from sheetcake import Cell
from sheetcake.src import errors
from sheetcake.src.arrays.beginning_balance import BeginningBalance
from sheetcake.src.arrays.ending_balance import EndingBalance


class Account:

    def __init__(self, *args, name='Unnamed Account', fmt=None, duration=None) -> None:
        self.name = name
        self.fmt = fmt
        self.args = list(args)
        if len(args):
            duration = len(args[0])
        if duration is None:
            raise errors.ImproperConfig("Must set either args or duration.")
        self.duration = duration

        self.bbal = BeginningBalance(self.duration)
        self.ebal = EndingBalance(self.duration)

        # for i, cell in enumerate(self.bbal):
        #     self.ebal[i].add(cell)
        bbal_plus_args = [self.bbal] + self.args
        for array in bbal_plus_args:
            if not len(array) == duration:
                raise ValueError(f"Cannot add arrays of different length: {len(array)}, {duration}")
            for i, cell in enumerate(array):
                self.ebal[i].add(cell)

        self.bbal.connect_ending_balance(self.ebal)

    @property
    def arrays(self):
        return self.args

    def add(self, *args):
        self.args += list(args)
        for array in args:
            if not len(array) == self.duration:
                raise ValueError(f"Cannot add arrays of different length: {len(array)}, {self.duration}")
            for i, cell in enumerate(array):
                self.ebal[i].add(cell)
