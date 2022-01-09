import datetime as dt
from numbers import Number
from typing import Any

from plum import convert, dispatch

from emitime.conversion import add_conversion_methods

add_conversion_methods()


class Interval:
    def __init__(self, value: Any) -> None:
        self.timedelta = value

    def timedelta(self) -> dt.timedelta:
        return self._value

    @timedelta.setter
    def timedelta(self, value) -> None:
        self._value = convert(value, dt.timedelta)

    @dispatch
    def __add__(self, other: "Interval") -> "Interval":
        """interval + interval -> interval"""
        pass

    @dispatch
    def __sub__(self, other: "Interval") -> "Interval":
        """interval - interval -> interval"""
        pass

    @dispatch
    def __mul__(self, other: Number) -> "Interval":
        """interval * Number -> interval"""
        raise NotImplementedError

    @dispatch
    def __truediv__(self, other: "Interval") -> float:
        """interval / interval -> float"""
        pass

    @dispatch
    def __truediv__(self, other: Number) -> "Interval":
        """interval / Number -> interval"""
        pass

    @dispatch
    def __floordiv__(self, other: "Interval") -> int:
        """interval // interval -> int"""
        pass

    @dispatch
    def __mod__(self, other: "Interval") -> "Interval":
        """interval % interval -> interval"""
        pass


class Moment:
    def __init__(self, value: Any) -> None:
        self.datetime = value

    @property
    def datetime(self) -> dt.datetime:
        return self._value

    @datetime.setter
    def datetime(self, value) -> None:
        self._value = convert(value, dt.datetime)

    @dispatch
    def __sub__(self, other: "Moment") -> Interval:
        raise NotImplementedError

    @dispatch
    def __sub__(self, other: Interval) -> "Moment":
        raise NotImplementedError

    @dispatch
    def __add__(self, other: Interval) -> "Moment":
        """datetime + time"""
        pass

    @dispatch
    def __radd__(self, other: Interval) -> "Moment":
        """interval + datetime -> moment"""
        return self + other
