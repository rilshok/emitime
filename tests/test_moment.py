import datetime as dt

from emitime import Moment
from pytest import mark


def test_moment_by_pydate() -> None:
    d = dt.date(year=2014, month=3, day=16)
    m = Moment(d)
    assert m.datetime.year == d.year
    assert m.datetime.month == d.month
    assert m.datetime.day == d.day
    assert m == d


@mark.parametrize(
    "value",
    [
        "2014-03-16",
        "2014/03/16",
        "16.03.2014",
    ],
)
def test_moment_by_string(value: str) -> None:
    m = Moment(value)
    assert m.datetime.year == 2014
    assert m.datetime.month == 3
    assert m.datetime.day == 16


@mark.parametrize(
    "date,target",
    [
        (dt.datetime(1992, 1, 2), "1992-01-02"),
    ],
)
def test_moment_to_string(date: dt.datetime, target: str) -> None:
    assert Moment(date) == target


def test_moment_comparison():
    m1 = Moment(dt.date(year=1992, month=1, day=2))
    m2 = Moment(dt.date(year=1993, month=12, day=12))
    m3 = Moment(dt.date(year=1993, month=12, day=12))
    assert m1 < m2 <= m3
    assert m3 >= m2 > m1
    assert m3 >= m1
    assert m1 != m2
    assert m2 == m3
    assert m1 < m2.datetime
    assert m2.datetime > m1


def test_moment_arithmetic():
    d1 = dt.date(year=1992, month=1, day=2)
    d2 = dt.date(year=1993, month=12, day=12)
    assert Moment(d2) - Moment(d1) == d2 - d1
    assert Moment(d2) - d1 == d2 - d1
    assert d2 - Moment(d1) == d2 - d1
