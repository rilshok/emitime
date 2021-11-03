__all__ = [
    'Date',
]

from typing import Any, Tuple, Union

from emitime import datetime as dt
from emitime import time as t
from datetime import date as py_date


AnyDelta = Union[int, float, str, t.Atomic, t.Days, t.Hours, t.Minutes, t.Seconds, 'Year', 'Day', 'Month']
AnyDate = Union[str, py_date, 'Date']

class Year(int):
    def __new__(cls, value) -> int:
        if isinstance(value, str):
            if value.isnumeric():
                value = int(value)
            else:
                raise NotImplementedError
        # NOTE: In 1752 Great Britain and the British Empire adopted the Gregorian calendar
        assert 1753 <= value < 10000
        obj = int.__new__(cls, value)
        return obj

    def __repr__(self) -> str:
        return '{} year'.format(int(self))

class MonthString(str):
    def __new__(cls, intvalue):
        assert 1 <= intvalue <= 12
        name, long = [
            ('jan','January'), ('feb','February'),
            ('mar','March'), ('apr','April'),
            ('may','May'), ('jun','June'),
            ('jul','July'), ('aug','August'),
            ('sep','September'), ('oct','October'),
            ('nov','November'), ('dec','December'),
        ][intvalue-1]
        obj = str.__new__(cls, name)
        obj.long = long
        return obj

class Month(int):
    def __new__(cls, value) -> int:
        if isinstance(value, str):
            value = value.lower()
            if value.isnumeric():
                value = int(value)
            elif len(value) == 3:
                value = [
                    'jan', 'feb', 'mar', 'apr',
                    'may', 'jun', 'jul', 'aug',
                    'sep', 'oct', 'nov', 'dec',
                ].index(value) + 1
            else:
                value = [
                    'january', 'february', 'march',
                    'april', 'may', 'june',
                    'july', 'august', 'september',
                    'october', 'november', 'december'
                ].index(value) + 1
        if not isinstance(value, int):
            raise NotImplementedError
        assert 1 <= value <= 12
        obj = int.__new__(cls, value)
        return obj

    def __str__(self) -> str:
        return MonthString(int(self))

    def __repr__(self) -> str:
        return str(self).long

class Day(int):
    def __new__(cls, value):
        if isinstance(value, str):
            if value.isnumeric():
                value = int(value)
            else:
                raise NotImplementedError
        if not isinstance(value, int):
            raise NotImplementedError
        assert 1 <= value <= 31
        obj = int.__new__(cls, value)
        return obj

    def __repr__(self) -> str:
        return '{} day'.format(int(self))

def _string_to_ymd(string) -> Tuple[Year, Month, Day]:
    assert isinstance(string, str)
    if '-' in string: # eng format
        ymd = string.split('-')
    elif '.' in string: # ru format
        ymd = string.split('.')[::-1]
    elif '/' in string: # eng format
        ymd = string.split('/')
    else:
        raise NotImplementedError
    assert all([*map(str.isnumeric, ymd)])
    assert len(ymd) == 3
    year, month, day = ymd
    if len(year) == 2:
        # short year
        assert py_date.today().year < 2035
        if int(year)<=35:
            year = '20' + year
        else:
            year = '19' + year
    return Year(year), Month(month), Day(day)

class DateString(str):
    def __new__(cls, value):
        assert isinstance(value, Date)
        year = value.year
        month = value.month
        day = value.day
        main = '{}-{:02}-{:02}'.format(int(year), int(month), int(day))
        obj = str.__new__(cls, main)
        obj.ru = '{:02}.{:02}.{}'.format(int(day), int(month), int(year))
        obj.eng_long = '{} {} {}'.format(int(day), str(month), int(year))
        return obj

class Date:
    def __init__(self, *args, year=None, month=None, day=None) -> None:
        kw_empty = year is None or month is None or day is None
        if len(args) == 1 and kw_empty:
            value = args[0]
            if isinstance(value, str):
                year, month, day = _string_to_ymd(value)
            elif isinstance(value, Date):
                self._date = value._date
                return
            elif isinstance(value, py_date):
                self._date = value
                return
        elif len(args) == 3 and kw_empty:
            year = Year(args[0])
            month = Month(args[1])
            day = Day(args[2])
        kw_empty = year is None or month is None or day is None
        if kw_empty:
            raise NotImplementedError
        if not isinstance(year, Year):
            year = Year(year)
        if not isinstance(month, Month):
            month = Month(month)
        if not isinstance(day, Day):
            day = Day(day)
        self._date = py_date(
            year = int(year),
            month = int(month),
            day = int(day)
        )

    def __str__(self) -> DateString:
        return DateString(self)

    def __repr__(self):
        return str(str(self))

    @property
    def py_date(self) -> py_date:
        return self._date

    @py_date.setter
    def py_date(self, value) -> None:
        self._date = value

    @property
    def year(self) -> Year:
        return Year(self.py_date.year)

    @year.setter
    def year(self, value: Any) -> None:
        self.py_date = py_date(
            year = int(Year(value)),
            month = int(self.month),
            day = int(self.day)
        )

    @property
    def month(self) -> Month:
        return Month(self.py_date.month)

    @month.setter
    def month(self, value: Any) -> None:
        self.py_date = py_date(
            year = int(self.year),
            month = int(Month(value)),
            day = int(self.day),
        )

    @property
    def day(self) -> Day:
        return Day(self.py_date.day)

    @day.setter
    def day(self, value: Any) -> None:
        self.py_date = py_date(
            year = int(self.year),
            month = int(self.month),
            day = int(Day(value)),
        )

    def __lt__(self, other: AnyDate) -> bool: # <
        raise NotImplementedError

    def __le__(self, other: AnyDate) -> bool: # <=
        raise NotImplementedError

    def __gt__(self, other: AnyDate) -> bool: # >
        raise NotImplementedError

    def __ge__(self, other: AnyDate) -> bool: # >=
        raise NotImplementedError

    def __eq__(self, other: AnyDate) -> bool: # ==
        raise NotImplementedError

    def __ne__(self, other: AnyDate) -> bool:
        raise NotImplementedError

    def __add__(self, other: AnyDelta) -> Union['Date', dt.DateTime]:
        raise NotImplementedError

    @t.uptype
    def __sub__(self, other: AnyDate) -> AnyDelta:
        raise NotImplementedError
