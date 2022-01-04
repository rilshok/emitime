from emitime.date import *
import datetime as dt

def test_create_date_by_pydate():
    pyd = dt.date(year=2014, month=3, day=16)
    d = Date(pyd)
    assert d.year == pyd.year
    assert d.month == pyd.month
    assert d.day == pyd.day
