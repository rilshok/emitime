__all__ = [
    'DateTime',
]

from typing import Tuple
from datetime import datetime as py_datetime

def _string_to_dt(string: str, format: str):
    from emitime import Date, Time
    # return None, None
    raise NotImplementedError

def _string_to_dt_adaptive(string):
    # return None, None
    raise NotImplementedError

class DateTime:
    def __init__(self, *args, year=None, month=None, day=None, hour=None, minute=None, second=None, millisecond=None) -> None:
        from emitime import Date, Time
        from emitime import time as t
        date, time = None, None
        there_is_datekw = year is not None or month is not None or day is not None
        there_is_timekw = hour is not None or minute is not None or second is not None or millisecond is not None

        if there_is_datekw or there_is_timekw and len(args)==0:
            assert year is not None
            assert month is not None
            assert day is not None
            date = Date(year=year, month=month, day=day)
            time_dict = dict()
            if minute is not None:
                time_dict['minutes'] = minute
            if hour is not None:
                time_dict['hours'] = hour
            if second is not None:
                time_dict['seconds'] = second
            if millisecond is None:
                millisecond = 0
            time = t.Time(t.Time(**time_dict) + t.Atomic(millisecond))
        elif len(args) == 2 and not there_is_datekw and not there_is_timekw:
            if isinstance(args[0], Date) and isinstance(args[1], Time):
                date = args[0]
                time = args[1]
            elif isinstance(args[0], Time) and isinstance(args[1], Date):
                date = args[1]
                time = args[1]
            elif isinstance(args[0], str) and isinstance(args[1], str):
                if '%' in args[1]:
                    date, time = _string_to_dt(args[0], args[1])
                else:
                    date = Date(args[0])
                    time = Time(args[1])
            else:
                date = Date(args[0])
                time = Time(args[1])
        elif len(args) == 1 and not there_is_datekw and not there_is_timekw:
            value = args[0]
            if isinstance(value, str):
                date, time = _string_to_dt_adaptive(value)
            elif isinstance(value, py_datetime):
                self.py_datetime=value
                return
            elif isinstance(value, Date):
                date = value
                time = None
            else:
                raise NotImplementedError
        if date is None:
            raise NotImplementedError
        if time is None:
            time = t.Atomic(0)
        time = t.Time(time)
        self.py_datetime = py_datetime(
            year=int(date.year),
            month=int(date.month),
            day=int(date.day),
        ) + time.pytimedelta

    @property
    def py_datetime(self) -> py_datetime:
        return self._datetime

    @py_datetime.setter
    def py_datetime(self, value) -> None:
        assert isinstance(value, py_datetime)
        self._datetime = value

    @property
    def date(self):
        from emitime.date import Date
        return Date(self.py_datetime.date())

    @property
    def time(self):
        from emitime.time import Time
        return Time(self.py_datetime.time())

    # TODO: str(self).long
    def __str__(self) -> str:
        return '{} {}'.format(str(self.date), str(self.time))

    def __repr__(self) -> str:
        return str(self)

    # TODO: math ops
