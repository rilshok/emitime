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
