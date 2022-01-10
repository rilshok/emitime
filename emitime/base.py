import datetime as dt
from numbers import Number

from plum import convert, dispatch

from emitime.conversion import add_conversion_methods
from plum.type import PromisedType, Union


IntervalType = PromisedType()
MomentType = PromisedType()

LikeInterval = Union[str, dt.timedelta, IntervalType]
LikeMoment = Union[str, dt.date, dt.datetime, MomentType]


class Interval:
    def __init__(self, value) -> None:
        self.timedelta = value

    @property
    def timedelta(self) -> dt.timedelta:
        return self._value

    @timedelta.setter
    def timedelta(self, value) -> None:
        self._value = convert(value, dt.timedelta)

    @dispatch
    def __add__(self, other: LikeInterval) -> "Interval":
        """interval + interval -> interval"""
        return Interval(self.timedelta + convert(other, dt.timedelta))

    @dispatch
    def __add__(self, other: LikeMoment) -> "Moment":
        """interval + moment -> moment"""
        return Moment(convert(other, dt.datetime) + self.timedelta)

    @dispatch
    def __sub__(self, other: LikeInterval) -> "Interval":
        """interval - interval -> interval"""
        return Interval(self.timedelta - convert(other, dt.timedelta))

    @dispatch
    def __mul__(self, other: Number) -> "Interval":
        """interval * Number -> interval"""
        return Interval(self.timedelta * other)

    @dispatch
    def __truediv__(self, other: LikeInterval) -> float:
        """interval / interval -> float"""
        return self.timedelta / convert(other, dt.timedelta)

    @dispatch
    def __truediv__(self, other: Number) -> "Interval":
        """interval / Number -> interval"""
        return Interval(self.timedelta / other)

    @dispatch
    def __floordiv__(self, other: LikeInterval) -> int:
        """interval // interval -> int"""
        return self.timedelta // convert(other, dt.timedelta)

    @dispatch
    def __mod__(self, other: LikeInterval) -> "Interval":
        """interval % interval -> interval"""
        return Interval(self.timedelta % convert(other, dt.timedelta))

    def __str__(self) -> str:
        return convert(self.timedelta, str)

    def __repr__(self) -> str:
        return str(self)


class Moment:
    def __init__(self, value) -> None:
        self.datetime = value

    @property
    def datetime(self) -> dt.datetime:
        return self._value

    @datetime.setter
    def datetime(self, value: LikeMoment) -> None:
        self._value = convert(value, dt.datetime)

    @dispatch
    def __sub__(self, other: LikeMoment) -> Interval:
        """moment - moment -> interval"""
        return Interval(self.datetime - convert(other, dt.datetime))

    @dispatch
    def __sub__(self, other: LikeInterval) -> "Moment":
        """moment - interval -> moment"""
        return Moment(self.datetime - convert(other, dt.timedelta))

    @dispatch
    def __add__(self, other: LikeInterval) -> "Moment":
        """moment + interval -> moment"""
        return Moment(self.datetime + convert(other, dt.timedelta))

    def __str__(self) -> str:
        return convert(self.datetime, str)

    def __repr__(self) -> str:
        return str(self)


IntervalType.deliver(Interval)
MomentType.deliver(Moment)

add_conversion_methods()
