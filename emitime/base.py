__all__ = (
    "Moment",
    "Interval",
)

import datetime as dt
import time
from typing import Any, Union as tUnion

from plum import convert, dispatch
from plum.type import PromisedType, Union

from emitime.conversion import (
    Number,
    add_conversion_methods,
    is_moment_str,
    is_time_str,
)

IntervalType = PromisedType()
MomentType = PromisedType()

# TODO: add float support
LikeInterval = Union[str, dt.timedelta, dt.time, IntervalType]
LikeMoment = Union[str, dt.date, dt.datetime, MomentType]


def upI(value: LikeInterval) -> dt.timedelta:
    return convert(value, dt.timedelta)


def upM(value: LikeMoment) -> dt.datetime:
    return convert(value, dt.datetime)


def is_interval(value: Any) -> bool:
    if isinstance(value, (dt.timedelta, dt.time, Interval)):
        return True
    if isinstance(value, str):
        if is_time_str(value):
            return True
    return False


def is_moment(value: Any) -> bool:
    if isinstance(value, (dt.date, dt.datetime, Moment)):
        return True
    if isinstance(value, str):
        if is_moment_str(value):
            return True
    return False


class Interval:
    def __init__(self, *args, **kwargs) -> None:
        if kwargs:
            raise NotImplementedError
        if len(args) != 1:
            raise NotImplementedError
        self.timedelta = args[0]

    @property
    def timedelta(self) -> dt.timedelta:
        return self._value

    @timedelta.setter
    @dispatch
    def timedelta(self, value: LikeInterval) -> None:
        self._value = upI(value)

    def __add__(
        self, other: Union["Interval", "Moment"]
    ) -> Union["Interval", "Moment"]:
        """this + (interval|moment) -> (interval|moment)"""
        if is_interval(other):
            return Interval(self.timedelta + upI(other))
        if is_moment(other):
            return Moment(upM(other) + self.timedelta)
        raise NotImplementedError

    def __radd__(
        self, other: Union["Interval", "Moment"]
    ) -> Union["Interval", "Moment"]:
        """(interval|moment) + this -> (interval|moment)"""
        return self + other

    @dispatch
    def __sub__(self, other: LikeInterval) -> "Interval":
        """this - interval -> interval"""
        return Interval(self.timedelta - upI(other))

    def __rsub__(
        self, other: tUnion["LikeInterval", "LikeMoment"]
    ) -> tUnion["Interval", "Moment"]:
        """(interval|moment) - this -> (interval|moment)"""
        if is_interval(other):
            return Interval(upI(other) - self.timedelta)
        elif is_moment(other):
            return Moment(upM(other) - self.timedelta)
        raise NotImplementedError

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

    def __float__(self) -> float:
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.timedelta)

class Moment:
    def __init__(self, *args, **kwargs) -> None:
        if kwargs:
            raise NotImplementedError
        if len(args) != 1:
            raise NotImplementedError
        self.datetime = args[0]

    @property
    def datetime(self) -> dt.datetime:
        return self._value

    @datetime.setter
    @dispatch
    def datetime(self, value: LikeMoment) -> None:
        self._value = upM(value)

    @property
    def date(self) -> dt.date:
        return self.datetime.date()

    @date.setter
    @dispatch
    def date(self, value: dt.date) -> None:
        if isinstance(value, dt.datetime):
            raise NotImplementedError
        raise NotImplementedError

    @date.setter
    @dispatch
    def date(self, value: str) -> None:
        raise NotImplementedError

    @property
    def time(self) -> dt.time:
        return self.datetime.time()

    @time.setter
    @dispatch
    def time(self, value: dt.time) -> None:
        raise NotImplementedError

    @time.setter
    @dispatch
    def time(self, value: str) -> None:
        raise NotImplementedError

    def __sub__(
        self, other: tUnion["LikeInterval", "LikeMoment"]
    ) -> tUnion["Interval", "Moment"]:
        """this - (interval|moment) -> (moment|interval)"""
        if is_interval(other):
            return Moment(self.datetime - upI(other))
        if is_moment(other):
            return Interval(self.datetime - upM(other))
        raise NotImplementedError

    @dispatch
    def __rsub__(self, other: LikeMoment) -> Interval:
        """moment - this -> interval"""
        return Moment(other) - self

    @dispatch
    def __add__(self, other: LikeInterval) -> "Moment":
        """this + interval -> moment"""
        return Moment(self.datetime + upI(other))

    def __radd__(self, other: LikeInterval) -> "Moment":
        """interval + this -> moment"""
        return self + other

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

    def __float__(self) -> float:
        # FIXME: microseconds are not converted
        return time.mktime(self.datetime.timetuple())

    def __hash__(self) -> int:
        return hash(self.datetime)

IntervalType.deliver(Interval)
MomentType.deliver(Moment)

add_conversion_methods()
