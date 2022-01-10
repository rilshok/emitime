import datetime as dt

from plum import add_conversion_method

from emitime.date import _string_to_ymd


def str_to_datetime(value: str) -> dt.datetime:
    # FIXME: yyyy-mm-dd^hh:mm[:ss[.ms['μs]]]
    y, m, d = _string_to_ymd(value)
    return dt.datetime(year=y, month=m, day=d)


def datetime_to_str(value: dt.datetime) -> str:
    year = value.year
    month = value.month
    day = value.day
    string = "{}-{:02}-{:02}".format(int(year), int(month), int(day))
    return string


def timedelta_to_str(value: dt.timedelta) -> str:
    sec = value.total_seconds()
    sign = "-" if sec < 0 else "+"
    sec = abs(sec)
    d = int(sec // 86_400)
    h = int(sec % 86_400 // 3_600)
    m = int(sec % 3_600 // 60)
    s = int(sec % 60)
    msμs = int(sec * 1_000_000) % 1000000
    ms = msμs // 1_000
    μs = msμs % 1_000
    time = f"{h:02}:{m:02}"
    if d != 0:
        time = f"{d}^{time}"
    tail = ""
    if μs != 0:
        tail = f"'{μs:03}"
    if ms != 0 or tail:
        tail = f".{ms:03}{tail}"
    if s != 0 or tail:
        tail = f":{s:02}{tail}"
    return f"{sign}{time}{tail}"


def str_to_timedelta(value: str) -> dt.timedelta:
    try:
        sign = 1.0
        d = h = m = s = ms = μs = 0
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
                msμs = split[-1]
                if "'" in msμs:
                    ms, μs = [*map(int, msμs.split("'"))]
                else:
                    ms = int(msμs)
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
            and 0 <= μs < 1e3
        )
    except Exception:
        need_format = (
            "time part does not match the format [-|+][d^]hh:mm[:ss[.ms['μs]]]"
        )
        raise AssertionError(need_format)
    total = (86_400 * d + 3_600 * h + 60 * m + s) * 1_000_000 + ms * 1_000 + μs
    return dt.timedelta(microseconds=sign * total)


def date_to_datetime(value: dt.date) -> dt.datetime:
    if isinstance(value, dt.datetime):
        return value
    return dt.datetime(value.year, value.month, value.day)


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
