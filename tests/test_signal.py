from sheetcake2.src.signal import Signal
import pytest


class Example:
    updated = False

    def update(self):
        self.updated = True


@pytest.fixture
def obj():
    return Example()


@pytest.fixture
def signal():
    return Signal()


def test_signal_init(signal):
    assert not signal._slots


def test_signal_connect(signal: Signal, obj: Example):
    signal.connect(obj.update)
    assert signal.is_connected(obj.update)


def test_signal_remove_slot(signal: Signal, obj: Example):
    signal.connect(obj.update)
    assert signal.is_connected(obj.update)
    signal.remove_slot(obj.update)
    assert not signal._slots


def test_signal_disconnect(signal: Signal, obj: Example):
    signal.connect(obj.update)
    assert signal.is_connected(obj.update)
    signal.disconnect(obj.update)
    assert not signal._slots


def test_signal_emit(signal: Signal, obj: Example):
    signal.connect(obj.update)
    assert not obj.updated
    signal.emit()
    assert obj.updated
