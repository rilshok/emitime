# emiTime
Emit Time from any time!

# Installation

```
pip install emitime
```

# Usage example

```python
import emitime as et
from random import random

start = et.Hours(12) - et.Seconds(700)
end = et.Time("14:20")
step = et.Minutes(20)
for v in et.timerange(start, end, step):
    v += 2 * et.Minutes(random() * 3 - 1.5)
    passed = et.Time(v - start)
    passed = et.Time(passed.hours_in + passed.minutes_in)
    print(v, passed, sep='; ')

print(v.pytimedelta, type(v.pytimedelta))
```

```
11:47:44.110; 00:00
12:10:40.024; 00:22
12:27:07.720; 00:38
12:50:58.082; 01:02
13:09:30.274; 01:21
13:29:11.062; 01:40
13:45:28.850; 01:57
14:05:29.692; 02:17
14:05:29.692000 <class 'datetime.timedelta'>
```

---
Emit and enjoy.
