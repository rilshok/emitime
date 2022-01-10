import datetime as dt
from typing import Dict

from plum import add_conversion_method

from emitime.date import _string_to_ymd

from numbers import Number

from collections import namedtuple

SplitSeconds = namedtuple('SplitSeconds', ['d', 'h', 'm', 's', 'ms', 'us'], defaults=[0]*6)

def split_seconds(value: Number) -> SplitSeconds:
    if value < 0.:
        msg = 'the number of seconds must be greater than zero'
        raise ValueError(msg)
    msus = int(value * 1_000_000) % 1_000_000
    return SplitSeconds(
        d = int(value // 86_400),
        h = int(value % 86_400 // 3_600),
        m = int(value % 3_600 // 60),
        s = int(value % 60),
        ms = msus // 1_000,
        us = msus % 1_000,
    )

def microseconds(
    *, h: int = 0, m: int = 0, s: int = 0, ms: int = 0, us: int = 0
) -> int:
    return (3_600 * h + 60 * m + s) * 1_000_000 + ms * 1_000 + us


def str_to_date(value: str) -> dt.date:
    raise NotImplementedError



def date_to_str(value: dt.date) -> str:
    y = value.year
    m = value.month
    d = value.day
    return f"{y}-{m:02}-{d:02}"


def time_to_timedelta(value: dt.time) -> dt.timedelta:
    h = value.hour
    m = value.minute
    s = value.second
    us = value.microsecond
    total = (3_600 * h + 60 * m + s) * 1_000_000 + us
    return dt.timedelta(microseconds=total)


def timedelta_to_str(value: dt.timedelta) -> str:
    sec = value.total_seconds()
    sign = "-" if sec < 0 else "+"
    s = split_seconds(abs(sec))
    time = f"{s.h:02}:{s.m:02}"
    if s.d != 0:
        time = f"{s.d}^{time}"
    tail = ""
    if s.us != 0:
        tail = f"'{s.us:03}"
    if s.ms != 0 or tail:
        tail = f".{s.ms:03}{tail}"
    if s.s != 0 or tail:
        tail = f":{s.s:02}{tail}"
    return f"{sign}{time}{tail}"

def time_to_str(value: dt.time) -> str:
    return timedelta_to_str(time_to_timedelta(value))

def datetime_to_str(value: dt.datetime) -> str:
    date = date_to_str(value.date())
    time = time_to_str(value.time())
    if not time:
        return date
    return f"{date}^{time}"

def str_to_timedelta(value: str) -> dt.timedelta:
    try:
        sign = 1.0
        d = h = m = s = ms = us = 0
        if value.startswith("-"):
            sign = -1.0
            value = value[1:]
        if "^" in value or "d" in value:
            if "^" in value:
                split = value.split("^")
            else:
                split = value.split("d")
            value = split[-1]
            d = int(split[0])
        if value:
            if "." in value:
                split = value.split(".")
                value = split[0]
                msus = split[-1]
                if "'" in msus:
                    ms, us = [*map(int, msus.split("'"))]
                else:
                    ms = int(msus)
            split = value.split(":")
            h = int(split[0])
            m = int(split[1])
            if len(split) == 3:
                s = int(split[2])
        assert (
            0 <= h < 24
            and 0 <= m < 60
            and 0 <= s < 60
            and 0 <= ms < 1e3
            and 0 <= us < 1e3
        )
    except Exception:
        need_format = (
            "time part does not match the format [-|+][d^]hh:mm[:ss[.ms['us]]]"
        )
        raise ValueError(need_format)
    total = 86_400 * 1_000_000 * d + microseconds(h=h, m=m, s=s, ms=ms, us=us)
    return sign * dt.timedelta(microseconds=total)

def timedelta_to_time(value:dt.timedelta) -> dt.time:
    total =

    raise NotImplementedError

def str_to_time(value: str) -> dt.time:
    try:
        assert "^" not in value
        assert "d" not in value
        assert "-" not in value
        assert "+" not in value
        timedelta = str_to_timedelta(value)
    except Exception:
        need_format = (
            "value does not match the format hh:mm[:ss[.ms['us]]]"
        )
        raise ValueError(need_format)
    return timedelta_to_time(timedelta)

def date_to_datetime(value: dt.date) -> dt.datetime:
    if isinstance(value, dt.datetime):
        return value
    return dt.datetime(value.year, value.month, value.day)



def str_to_datetime(value: str) -> dt.datetime:
    """yyyy-mm-dd[^hh:mm[:ss[.ms['us]]]]"""
    try:
        if "^" in value or "d" in value:
            if "^" in value:
                split = value.split("^")
            else:
                split = value.split("d")
            assert len(split) == 2
            date = str_to_date(split[0])
            time = str_to_time(split[1])
        else:
            date =  str_to_date(value)
            time = dt.timedelta()

    except Exception:
        need_format = (
            "value does not match the format yyyy-mm-dd[^hh:mm[:ss[.ms['us]]]]"
        )
        raise ValueError(need_format)

    return date_to_datetime(date) + time_to_timedelta(time)



def add_conversion_methods():
    from emitime.base import Interval, Moment

    add_conversion_method(type_from=str, type_to=dt.datetime, f=str_to_datetime)
    add_conversion_method(type_from=dt.datetime, type_to=str, f=datetime_to_str)
    add_conversion_method(type_from=str, type_to=dt.timedelta, f=str_to_timedelta)
    add_conversion_method(type_from=dt.timedelta, type_to=str, f=timedelta_to_str)
    add_conversion_method(
        type_from=Interval, type_to=dt.timedelta, f=lambda x: x.timedelta
    )
    add_conversion_method(type_from=Moment, type_to=dt.datetime, f=lambda x: x.datetime)
    add_conversion_method(type_from=dt.date, type_to=dt.datetime, f=date_to_datetime)
    add_conversion_method(type_from=dt.time, type_to=dt.timedelta, f=time_to_timedelta)
