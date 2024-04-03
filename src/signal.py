class Signal:

    def __init__(self) -> None:
        self._slots = []

    def connect(self, slot):
        self._slots.append(slot)

    def remove_slot(self, slot):
        self._slots.remove(slot)

    def emit(self, *args, **kwargs):
        for slot in self._slots:
            slot(*args, **kwargs)

    def disconnect(self, slot):
        if self.is_connected(slot):
            self._slots.pop(self._slots.index(slot))

    def is_connected(self, slot):
        return slot in self._slots
