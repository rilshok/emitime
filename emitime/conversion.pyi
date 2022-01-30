import datetime as dt
from typing import Any, NamedTuple, Union

Number = Union[int, float]

class SplitSeconds(NamedTuple):
    d: Any
    h: Any
    m: Any
    s: Any
    ms: Any
    us: Any

def split_seconds(value: Number) -> SplitSeconds: ...
def microseconds(value: SplitSeconds) -> int: ...
def str_to_date(value: str) -> dt.date: ...
def date_to_str(value: dt.date) -> str: ...
def time_to_timedelta(value: dt.time) -> dt.timedelta: ...
def timedelta_to_str(value: dt.timedelta) -> str: ...
def time_to_str(value: dt.time) -> str: ...
def datetime_to_str(value: dt.datetime) -> str: ...
def str_to_timedelta(value: str) -> dt.timedelta: ...
def timedelta_to_time(value: dt.timedelta) -> dt.time: ...
def str_to_time(value: str) -> dt.time: ...
def date_to_datetime(value: dt.date) -> dt.datetime: ...
def str_to_datetime(value: str) -> dt.datetime: ...
def is_time_str(value: str) -> bool: ...
def is_moment_str(value: str) -> bool: ...
def add_conversion_methods(): ...
