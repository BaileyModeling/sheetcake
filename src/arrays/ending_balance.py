from .base_array import BaseArray
from .array import Array


class EndingBalance(Array):

    def __init__(self, duration=None, name='Ending Balance', array=None, fmt=None):
        super(Array, self).__init__(duration, name, array, fmt)

    @property
    def total(self):
        return self._array[-1].value
