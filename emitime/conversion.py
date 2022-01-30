__all__ = (
    "str_to_date",
    "date_to_str",
    "time_to_timedelta",
    "timedelta_to_str",
    "datetime_to_str",
    "str_to_timedelta",
    "timedelta_to_time",
    "str_to_time",
    "date_to_datetime",
    "str_to_datetime"
)

import datetime as dt
from collections import namedtuple
from typing import Union

from plum import add_conversion_method

Number = Union[int, float]

SplitSeconds = namedtuple(
    "SplitSeconds",
    ["d", "h", "m", "s", "ms", "us"],
    defaults=(0, 0, 0, 0, 0, 0),
)


def split_seconds(value: Number) -> SplitSeconds:
    if value < 0:
        msg = "the number of seconds must be greater than zero"
        raise ValueError(msg)
    msus = int(value * 1_000_000) % 1_000_000
    return SplitSeconds(
        d=int(value // 86_400),
        h=int(value % 86_400 // 3_600),
        m=int(value % 3_600 // 60),
        s=int(value % 60),
        ms=msus // 1_000,
        us=msus % 1_000,
    )


def microseconds(value: SplitSeconds) -> int:
    return (
        (86_400 * value.d + 3_600 * value.h + 60 * value.m + value.s) * 1_000_000
        + value.ms * 1_000
        + value.us
    )


def str_to_date(value: str) -> dt.date:
    if "-" in value:  # eng format
        ymd = value.split("-")
    elif "." in value:  # ru format
        ymd = value.split(".")[::-1]
    elif "/" in value:  # eng format
        ymd = value.split("/")
    else:
        raise NotImplementedError
    assert all([*map(str.isnumeric, ymd)])
    assert len(ymd) == 3
    year, month, day = ymd
    if len(year) == 2:
        # short year
        assert dt.date.today().year < 2035
        if int(year) <= 35:
            year = "20" + year
        else:
            year = "19" + year
    return dt.date(year=int(year), month=int(month), day=int(day))


def date_to_str(value: dt.date) -> str:
    y = value.year
    m = value.month
    d = value.day
    return f"{y}-{m:02}-{d:02}"


def time_to_timedelta(value: dt.time) -> dt.timedelta:
    secs = SplitSeconds(
        d=0, h=value.hour, m=value.minute, s=value.second, ms=0, us=value.microsecond
    )
    return dt.timedelta(microseconds=microseconds(secs))


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
    t = value.time()
    if t == dt.time():
        return date
    time = time_to_str(t)
    return f"{date}d{time}".replace("+", "")


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
        need_format = "Value does't match the format: [-|+][d^]hh:mm[:ss[.ms['us]]]"
        raise ValueError(need_format)
    secs = SplitSeconds(d=d, h=h, m=m, s=s, ms=ms, us=us)
    return sign * dt.timedelta(microseconds=microseconds(secs))


def timedelta_to_time(value: dt.timedelta) -> dt.time:
    total = value.total_seconds()
    if total < 0:
        msg = f"Negative '{value=!r}' can't be converted to time"
        raise ValueError(msg)
    secs = split_seconds(total)
    if secs.d != 0:
        msg = f"'{value=!r}' can't be converted to time as it contains days"
        raise ValueError(msg)

    return dt.time(
        hour=secs.h, minute=secs.m, second=secs.s, microsecond=secs.ms * 1_000 + secs.us
    )


def str_to_time(value: str) -> dt.time:
    try:
        assert "^" not in value
        assert "d" not in value
        assert "-" not in value
        assert "+" not in value
        timedelta = str_to_timedelta(value)
    except Exception:
        need_format = "'value' does not match the format: hh:mm[:ss[.ms['us]]]"
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
            date = str_to_date(value)
            time = dt.time()

    except Exception:
        need_format = (
            "'value' does't match the format: yyyy-mm-dd[^hh:mm[:ss[.ms['us]]]]"
        )
        raise ValueError(need_format)

    return date_to_datetime(date) + time_to_timedelta(time)


def is_time_str(value: str) -> bool:
    try:
        str_to_timedelta(value)
    except Exception:
        return False
    return True


def is_moment_str(value: str) -> bool:
    if len(value) < 8:
        return False
    try:
        str_to_datetime(value)
    except Exception:
        return False
    return True


def add_conversion_methods():
    from emitime.base import Interval, Moment

    add_conversion_method(type_from=str, type_to=dt.timedelta, f=str_to_timedelta)
    add_conversion_method(type_from=dt.time, type_to=dt.timedelta, f=time_to_timedelta)
    add_conversion_method(
        type_from=Interval, type_to=dt.timedelta, f=lambda x: x.timedelta
    )

    add_conversion_method(type_from=str, type_to=dt.datetime, f=str_to_datetime)
    add_conversion_method(type_from=dt.date, type_to=dt.datetime, f=date_to_datetime)
    add_conversion_method(type_from=Moment, type_to=dt.datetime, f=lambda x: x.datetime)

    add_conversion_method(type_from=dt.datetime, type_to=str, f=datetime_to_str)
    add_conversion_method(type_from=dt.timedelta, type_to=str, f=timedelta_to_str)
