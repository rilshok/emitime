# emiTime

The __emiTime__ library is designed to simplify the work with objects describing calendar time points and intervals between them.
All algorithms presented in the library are based on two entities `Moment` and `Inerval`.
Each of them can be fired from anything that looks like a calendar time point or a time interval.

## Installation

```
pip install emitime
```

Or from GitHub

```
git clone https://github.com/rilshok/emitime.git
cd emitime
pip install -e .
```

## Usage

A `Moment` object can be created by a `str`, datetime module objects such as `date` and `datetime`, or another `Moment`.
In turn, `Interval` can also be derived from a `str`, `datetime.time` or another `Interval`.

```python
import datetime as dt

from emitime import Moment

d1 = Moment("1970-01-01")
d2 = Moment(dt.datetime(1970, 1, 1))
d3 = Moment(dt.date(1970, 1, 1))
d4 = Moment(d3)

print(f"{d1=}, {d2=}, {d3=}, {d4=}")
print(f"{d1 == d2 == d3 == d4 = }")
```
```
d1=1970-01-01, d2=1970-01-01, d3=1970-01-01, d4=1970-01-01
d1 == d2 == d3 == d4 = True
```

```python
import datetime as dt

from emitime import Interval

t1 = Interval("2d")
t2 = Interval("12:00")
t3 = Interval(dt.timedelta(hours=5))
t4 = Interval(t3)

print(f"{t1=}, {t2=}, {t3=}, {t4=}")
print(f"{t1 > t2 > t3 >= t4 = }")
```
```
t1=+2^00:00, t2=+12:00, t3=+05:00, t4=+05:00
t1 > t2 > t3 >= t4 = True
```

`Moment` and `Interval` can participate in natural mathematical operations and be compared with each other.
Also, whenever possible, depending on the context, __emiTime__ promotes the type of one of the operands of the operation to `Moment` or `Interval`

```python
import datetime as dt

from emitime import Interval, Moment

m1 = Moment("1970-01-01") + "2d"
m2 = dt.timedelta(hours=5) + Moment("01.01.1970")
m3 = "1970-01-01" + Interval("12:00")

i1 = Moment("2020-01-01") - "2019-01-01"
i2 = "12:00" - Interval("1d")
i3 = dt.date(2021, 1, 1) - Moment("2020-01-01")

print(f"{m1=}, {m2=}, {m3=}")
print(f"{i1=}, {i2=}, {i3=}")
print(f"{m1 > m2=}")
print(f"{m2 < m3 <= m1 =}")
print(f"{m3+i2 == m1 - i3+i1 - i3+i1 = }")
```
```
m1=1970-01-03, m2=1970-01-01d05:00, m3=1970-01-01d12:00
i1=+365^00:00, i2=-12:00, i3=+366^00:00
m1 > m2=True
m2 < m3 <= m1 =True
m3+i2 == m1 - i3+i1 - i3+i1 = True
```

`Moment` is based on the standard `datetime.datetime` and `Interval` is based on `datetime.timedelta`. Which can be accessed as follows.

```python
from emitime import Interval, Moment

m = Moment("1970-01-01")
i = Interval("02:10")
mdt = m.datetime
itd = i.timedelta

print(f"{mdt = }")
print(f"{itd = }")
```
```
mdt = datetime.datetime(1970, 1, 1, 0, 0)
itd = datetime.timedelta(seconds=7800)
```


---
Emit and enjoy.
