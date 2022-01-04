from emitime.date import *
import datetime as dt


def test_create_date_by_pydate():
    pyd = dt.date(year=2014, month=3, day=16)
    d = Date(pyd)
    assert d.year == pyd.year
    assert d.month == pyd.month
    assert d.day == pyd.day
    assert d.pydate == pyd
    assert d == pyd

def test_date_to_str():
    assert str(Date(year=1992, month=1, day=2)) == '1992-01-02'
    assert str(Date(year=1993, month=12, day=12)) == '1993-12-12'

def test_date_comparison():
    d1 = Date(year=1992, month=1, day=2)
    d2 = Date(year=1993, month=12, day=12)
    d3 = Date(year=1993, month=12, day=12)
    assert d1 < d2 <= d3
    assert d3 >= d2 > d1
    assert d3 >= d1
    assert d1 != d2
    assert d2 == d3
    assert d1 < d2.pydate
    assert d2.pydate > d1
