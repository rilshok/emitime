import datetime as dt

from plum import convert, dispatch

from emitime.conversion import Number, add_conversion_methods
from plum.type import PromisedType, Union

IntervalType = PromisedType()
MomentType = PromisedType()

LikeInterval = Union[str, dt.timedelta, dt.time, IntervalType]
LikeMoment = Union[str, dt.date, dt.datetime, MomentType]


def upI(value: LikeInterval) -> dt.timedelta:
    return convert(value, dt.timedelta)

def upM(value: LikeMoment) -> dt.datetime:
    return convert(value, dt.datetime)

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
        """this + interval -> interval"""
        return Interval(self.timedelta + upI(other))

    @dispatch
    def __add__(self, other: LikeMoment) -> "Moment":
        """this + moment -> moment"""
        return Moment(upM(other) + self.timedelta)

    @dispatch
    def __radd__(self, other: LikeMoment) -> "Moment":
        """moment + this -> moment"""
        return Moment(other) + self

    @dispatch
    def __sub__(self, other: LikeInterval) -> "Interval":
        """this - interval -> interval"""
        return Interval(self.timedelta - upI(other))

    @dispatch
    def __mul__(self, other: Number) -> "Interval":
        """this * Number -> interval"""
        return Interval(self.timedelta * other)

    @dispatch
    def __rmul__(self, other: Number) -> "Interval":
        """Number * this -> interval"""
        return self * other

    @dispatch
    def __truediv__(self, other: LikeInterval) -> float:
        """this / interval -> float"""
        return self.timedelta / upI(other)

    @dispatch
    def __truediv__(self, other: Number) -> "Interval":
        """this / Number -> interval"""
        return Interval(self.timedelta / other)

    @dispatch
    def __floordiv__(self, other: LikeInterval) -> int:
        """this // interval -> int"""
        return self.timedelta // upI(other)

    @dispatch
    def __mod__(self, other: LikeInterval) -> "Interval":
        """this % interval -> interval"""
        return Interval(self.timedelta % upI(other))

    @dispatch
    def __lt__(self, other: LikeInterval) -> bool:
        """this < interval -> bool"""
        return self.timedelta < upI(other)

    @dispatch
    def __le__(self, other: LikeInterval) -> bool:
        """this <= interval -> bool"""
        return self.timedelta <= upI(other)

    @dispatch
    def __eq__(self, other: LikeInterval) -> bool:
        """this == interval -> bool"""
        return self.timedelta == upI(other)

    @dispatch
    def __ne__(self, other: LikeInterval) -> bool:
        """this != interval -> bool"""
        return self.timedelta != upI(other)

    @dispatch
    def __gt__(self, other: LikeInterval) -> bool:
        """this > interval -> bool"""
        return self.timedelta > upI(other)

    @dispatch
    def __ge__(self, other: LikeInterval) -> bool:
        """this >= interval -> bool"""
        return self.timedelta >= upI(other)

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
        """this - moment -> interval"""
        return Interval(self.datetime - upM(other))

    @dispatch
    def __sub__(self, other: LikeInterval) -> "Moment":
        """this - interval -> moment"""
        return Moment(self.datetime - upI(other))

    @dispatch
    def __rsub__(self, other: LikeMoment) -> Interval:
        """moment - this -> interval"""
        return Moment(other) - self

    @dispatch
    def __add__(self, other: LikeInterval) -> "Moment":
        """this + interval -> moment"""
        return Moment(self.datetime + upI(other))

    @dispatch
    def __lt__(self, other: LikeMoment) -> bool:
        """this < moment -> bool"""
        return self.datetime < upM(other)

    @dispatch
    def __le__(self, other: LikeMoment) -> bool:
        """this <= moment -> bool"""
        return self.datetime <= upM(other)

    @dispatch
    def __eq__(self, other: LikeMoment) -> bool:
        """this == moment -> bool"""
        return self.datetime == upM(other)

    @dispatch
    def __ne__(self, other: LikeMoment) -> bool:
        """this != moment -> bool"""
        return self.datetime != upM(other)

    @dispatch
    def __gt__(self, other: LikeMoment) -> bool:
        """this > moment -> bool"""
        return self.datetime > upM(other)

    @dispatch
    def __ge__(self, other: LikeMoment) -> bool:
        """this >= moment -> bool"""
        return self.datetime >= upM(other)

    def __str__(self) -> str:
        return convert(self.datetime, str)

    def __repr__(self) -> str:
        return str(self)


IntervalType.deliver(Interval)
MomentType.deliver(Moment)

add_conversion_methods()
