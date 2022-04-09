from .base_array import BaseArray
from .array import Array


class BeginningBalance(Array):

    def __init__(self, duration=None, name='Beginning Balance', array=None, fmt=None):
        if array is None:
            array = [0] * duration
        super(Array, self).__init__(duration, name, array, fmt)
        self.ebal = None

    @property
    def total(self):
        return self._array[0].value

    def connect_ending_balance(self, ebal_array):
        self.ebal = ebal_array
        if not len(ebal_array) == self.duration:
            raise ValueError(f"Cannot add arrays of different length: {len(ebal_array)}, {self.duration}")
        for i, cell in enumerate(ebal_array):
            if i < self.duration - 1:
                self[i+1].equal(cell)
        # self.ebal.changed.connect(self.update)
        # self.ebal.changed_value.connect(self.update_value)
