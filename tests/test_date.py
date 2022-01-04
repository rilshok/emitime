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

def test_create_date_by_string():
    d = Date('2014-03-16')
    assert d.year == 2014
    assert d.month == 3
    assert d.day == 16

def test_date_to_str():
    d1 = Date(year=1992, month=1, day=2)
    d2 = Date(year=1993, month=12, day=12)
    assert str(d1) == '1992-01-02'
    assert str(d2) == '1993-12-12'
    assert str(d1.year) == '1992 year'
    assert str(d1.month) == 'jan'
    assert str(d1.month).long == 'January'
    assert str(d1.day) == '2 day'
    assert str(d1).ru == '02.01.1992'
    assert str(d1).eng_long == '2 jan 1992'

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

def test_date_arithmetic():
    pyd1 = dt.date(year=1992, month=1, day=2)
    pyd2 = dt.date(year=1993, month=12, day=12)
    # Date(pyd2) - Date(pyd1) ==== pyd2-pyd1
