import datetime as dt
from numbers import Number
from typing import Any, Union

from plum import convert, dispatch

from emitime.conversion import add_conversion_methods
from emitime.date import DateString

add_conversion_methods()

LikeInterval = Union[str, dt.timedelta, "Interval"]

class Interval:
    def __init__(self, value: Any) -> None:
        self.timedelta = value

    @property
    def timedelta(self) -> dt.timedelta:
        return self._value

    @timedelta.setter
    def timedelta(self, value) -> None:
        self._value = convert(value, dt.timedelta)

    @dispatch
    def __add__(self, other: "Interval") -> "Interval":
        """interval + interval -> interval"""
        return Interval(self.timedelta + other.timedelta)

    @dispatch
    def __sub__(self, other: "Interval") -> "Interval":
        """interval - interval -> interval"""
        return Interval(self.timedelta - other.timedelta)

    @dispatch
    def __mul__(self, other: Number) -> "Interval":
        """interval * Number -> interval"""
        return Interval(self.timedelta * other)

    @dispatch
    def __truediv__(self, other: "Interval") -> float:
        """interval / interval -> float"""
        return self.timedelta / other.timedelta

    @dispatch
    def __truediv__(self, other: Number) -> "Interval":
        """interval / Number -> interval"""
        return Interval(self.timedelta / other)

    @dispatch
    def __floordiv__(self, other: "Interval") -> int:
        """interval // interval -> int"""
        return self.timedelta // other.timedelta

    @dispatch
    def __mod__(self, other: "Interval") -> "Interval":
        """interval % interval -> interval"""
        return Interval(self.timedelta % other.timedelta)

    def __str__(self) -> str:
        return convert(self.timedelta, str)

    def __repr__(self) -> str:
        return str(self)

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
        return Interval(self.datetime - other.datetime)

    @dispatch
    def __sub__(self, other: Interval) -> "Moment":
        return Moment(self.datetime - other.timedelta)

    @dispatch
    def __add__(self, other: Interval) -> "Moment":
        """moment + interval -> moment"""
        return Moment(self.datetime + other.timedelta)

    def __add__(self, other):
        return self + convert(other, Interval)

    @dispatch
    def __radd__(self, other: Interval) -> "Moment":
        """interval + datetime -> moment"""
        return self + other

    def __str__(self) -> str:
        return convert(self.datetime, str)

    def __repr__(self) -> str:
        return str(self)
