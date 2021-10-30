__all__ = [
    'Atomic',
    'Time',
    'Seconds',
    'Minutes',
    'Hours',
    'Days',
    'timerange',
]

from datetime import timedelta as py_timedelta

from typing import Tuple, Union

AnyTime = Union[float, str, 'Atomic', 'Days', 'Hours', 'Minutes', 'Seconds']

def _num_to_str(num):
    if round(num) == num:
        return str(round(num))
    return str(num)

def _string_to_atomic(string :str) -> 'Atomic':
    """[D-]HH:MM[:SS][.MS]"""
    need_format = 'time part does not match the format [D-]HH:MM[:SS][.MS]'
    d = h = m = s = a = 0
    if 'd' in string:
        t = string.split('d')
    else:
        t = string.split('-')
    assert len(t) <= 2
    if len(t) == 2:
        d = int(t[0])
        string = t[1]
    t = string.split('.')
    assert len(t) <= 2
    if len(t) == 2:
        a = int(t[1])
        string = t[0]
    t = string.split(":")
    if 2 <= len(t) <= 3:
        h = int(t[0])
        m = int(t[1])
        if len(t) == 3:
            s = int(t[2])
        elif a!=0:
            raise AssertionError(need_format)
    if not (0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60 and a < 1000):
        raise AssertionError(need_format)
    return Atomic(Days(d) + Hours(h) + Minutes(m) + Seconds(s) + Atomic(a))

class TimeString(str):
    def __new__(cls, value, long):
        obj = str.__new__(cls, value)
        obj.long = long
        return obj

def _atomic_to_string(atomic :'Atomic') -> TimeString:
    t = Time(atomic)
    d = int(t.days_in.days)
    h = int(t.hours_in.hours)
    m = int(t.minutes_in.minutes)
    s = int(t.seconds_in.seconds)
    a = int(t.atomic_in.atomic)
    string = '{:02}:{:02}'.format(h, m)
    long = string
    if s != 0:
        string += ':{:02}'.format(s)
    long+=':{:02}'.format(s)
    if a != 0:
        if s == 0:
            string += ':{:02}'.format(s)
        string += '.{:03}'.format(a)
    long += '.{:03}'.format(a)
    if d != 0:
        string = '{}-{}'.format(d, string)
    long = '{}-{}'.format(d, long)
    return TimeString(value=string, long=long)

def uptype(func):
    def cast(*args, **kwargs):
        T = lambda x: x
        t = None
        types = {type(a) for a in args}.difference({int, float})
        if len(types) == 1:
            t = types.pop()
            if issubclass(t, Atomic):
                T = t
        if len(types) == 2 and all([issubclass(t, Atomic) for t in types]):
            T = Time
        result = func(*args, **kwargs)
        if isinstance(result, Atomic):
            result = T(result)
        if isinstance(result, Time) and t is None:
            if result == result.seconds_in:
                return Seconds(result)
            if result == result.minutes_in:
                return Minutes(result)
            if result == result.hours_in:
                return Hours(result)
            if result == result.days_in:
                return Days(result)
        return result
    return cast

class Atomic:
    def __init__(self, value: AnyTime) -> None:
        if isinstance(value, str):
            value = _string_to_atomic(value)
        if isinstance(value, Atomic):
            value = value.atomic
        if isinstance(value, py_timedelta):
            value = value.total_seconds() * 1000.
        if not isinstance(value, (float, int)):
            raise NotImplementedError
        self._value = int(value)

    @property
    def atomic(self) -> int:
        return int(self._value)

    def __str__(self) -> TimeString:
        return TimeString(
            value='{} ms'.format(self.atomic),
            long='{} millisecond'.format(self.atomic),
        )

    def __repr__(self) -> str:
        return str(self)

    @atomic.setter
    def atomic(self, other: AnyTime) -> None:
        self._value = Atomic(other).atomic

    def __int__(self) -> int:
        return self.atomic

    def __float__(self) -> float:
        return float(self.atomic)

    def copy(self) -> 'Atomic':
        return Atomic(self.atomic)

    @property
    def milliseconds(self) -> float:
        return self.atomic

    @milliseconds.setter
    def milliseconds(self, value):
        self.atomic = Atomic(value).atomic

    @property
    def seconds(self) -> float:
        return self.atomic / 1000.

    @seconds.setter
    def seconds(self, value):
        self.atomic = Seconds(value).atomic

    @property
    def centiseconds(self)-> float:
        return self.atomic / 100.

    @centiseconds.setter
    def centiseconds(self, value)-> float:
        if isinstance(value, (int, float)):
            value = Atomic(value * 100.)
        self.atomic = Atomic(value).atomic

    @property
    def minutes(self) -> float:
        return float(self.seconds) / 60.

    @minutes.setter
    def minutes(self, value):
        self.atomic = Minutes(value).atomic

    @property
    def hours(self) -> float:
        return float(self.minutes) / 60.

    @hours.setter
    def hours(self, value):
        self.atomic = Hours(value).atomic

    @property
    def days(self) -> float:
        return float(self.hours) / 24.

    @days.setter
    def days(self, value):
        self.atomic = Days(value).atomic

    def __lt__(self, other: AnyTime) -> bool:
        return self.atomic < Atomic(other).atomic

    def __le__(self, other: AnyTime) -> bool:
        return self.atomic <= Atomic(other).atomic

    def __eq__(self, other: AnyTime) -> bool:
        return self.atomic == Atomic(other).atomic

    def __ne__(self, other: AnyTime) -> bool:
        return self.atomic != Atomic(other).atomic

    def __gt__(self, other: AnyTime) -> bool:
        return self.atomic > Atomic(other).atomic

    def __ge__(self, other: AnyTime) -> bool:
        return self.atomic >= Atomic(other).atomic

    @uptype
    def __add__(self, other: AnyTime) -> 'Atomic':
        return Atomic(self.atomic + Atomic(other).atomic)

    @uptype
    def __sub__(self, other: AnyTime) -> 'Atomic':
        return Atomic(self.atomic - Atomic(other).atomic)

    @uptype
    def __mul__(self, other: Union[int, float]) -> 'Atomic':
        if isinstance(other, (int, float)):
            return Atomic(self.atomic * other)
        raise NotImplementedError

    @uptype
    def __truediv__(self, other: AnyTime) -> 'Atomic':
        if isinstance(other, (int, float)):
            return Atomic(self.atomic / other)
        # if other is subAtomic return float
        raise NotImplementedError

    @uptype
    def __floordiv__(self, other: AnyTime) -> 'Atomic':
        if isinstance(other, int):
            return Atomic(self.atomic // other)
        # if other is subAtomic return float
        raise NotImplementedError

    @uptype
    def __mod__(self, other: AnyTime) -> 'Atomic':
        if isinstance(other, (int, float)):
            return Atomic(self.atomic % other)
        raise NotImplementedError

    def __divmod__(self, other: AnyTime) -> Tuple['Atomic', 'Atomic']:
        return (self // other, self % other)

    @uptype
    def __radd__(self, other: AnyTime) -> 'Atomic':
        return self + other

    @uptype
    def __rsub__(self, other: AnyTime) -> 'Atomic':
        return self * -1. + other

    @uptype
    def __rmul__(self, other: AnyTime) -> 'Atomic':
        return self * other

    def __rtruediv__(self, other: AnyTime) -> float:
        # FIXME: implement this, use other as same atomic
        raise NotImplementedError

    def __rfloordiv__(self, other: AnyTime) -> float:
        # FIXME: implement this, use other as same atomic
        raise NotImplementedError

    def __rmod__(self, other: AnyTime) -> float:
        raise NotImplementedError

    # def __rdivmod__(self, other):

    @uptype
    def __iadd__(self, other: AnyTime) -> 'Atomic':
        return self + other

    @uptype
    def __isub__(self, other: AnyTime) -> 'Atomic':
        return self - other

    @uptype
    def __imul__(self, other: Union[int, float]) -> 'Atomic':
        return self * other

    @uptype
    def __itruediv__(self, other: AnyTime) -> 'Atomic':
        return self / other

    @uptype
    def __ifloordiv__(self, other: AnyTime) -> 'Atomic':
        return self // other

    @uptype
    def __imod__(self, other: AnyTime) -> 'Atomic':
        return self % other

    def __bool__(self):
        return bool(self.atomic)

    def __hash__(self):
        return self.atomic

    def __bytes__(self):
        return bytes(self.atomic)

    @property
    def pytimedelta(self) -> py_timedelta:
        t = Time(self)
        return py_timedelta(
            days=t.days_in.days,
            # weeks=...,
            hours=t.hours_in.hours,
            minutes=t.minutes_in.minutes,
            seconds=t.seconds_in.seconds,
            # microseconds=...,
            milliseconds=t.atomic_in.atomic,
        )

    @pytimedelta.setter
    def pytimedelta(self, other) -> None:
        self.atomic = Atomic(other).atomic

def asatomic(*anytime: AnyTime, **anytimekw) -> Atomic:
    atomic = Atomic(0.)
    if len(anytime) == 1:
        atomic += Atomic(anytime[0])
    elif len(anytime) == 2:
        # m, s
        assert 'hours' not in anytimekw
        assert 'minutes' not in anytimekw
        is_ms = isinstance(anytime[0], Hours) and isinstance(anytime[0], Minutes)
        is_ms_f = all([isinstance(at, (float, int)) for at in anytime])
        if is_ms:
            atomic += anytime[0].atomic
            atomic += anytime[1].atomic
        elif is_ms_f:
            atomic += Hours(anytime[0])
            atomic += Minutes(anytime[1])
        else:
            raise NotImplementedError
    elif len(anytime) == 3:
        # h, m, s
        assert 'hours' not in anytimekw
        assert 'minutes' not in anytimekw
        assert 'seconds' not in anytimekw
        is_hms = isinstance(anytime[0], Hours) and isinstance(anytime[1], Minutes) and isinstance(anytime[2], Seconds)
        is_hms_f = all([isinstance(at, (float, int)) for at in anytime])
        if is_hms:
            atomic += anytime[0].atomic
            atomic += anytime[1].atomic
            atomic += anytime[2].atomic
        elif is_hms_f:
            atomic += Hours(anytime[0])
            atomic += Minutes(anytime[1])
            atomic += Seconds(anytime[2])
        else:
            raise NotImplementedError
    elif len(anytime) == 4:
        # d, h, m, s
        assert 'days' not in anytimekw
        assert 'hours' not in anytimekw
        assert 'minutes' not in anytimekw
        assert 'seconds' not in anytimekw
        is_dhms = isinstance(anytime[0], Hours) and isinstance(anytime[1], Hours) and isinstance(anytime[2], Minutes) and isinstance(anytime[3], Seconds)
        is_dhms_f = all([isinstance(at, (float, int)) for at in anytime])
        if is_dhms:
            atomic += anytime[0].atomic
            atomic += anytime[1].atomic
            atomic += anytime[2].atomic
            atomic += anytime[3].atomic
        elif is_dhms_f:
            atomic += Hours(anytime[0])
            atomic += Hours(anytime[1])
            atomic += Minutes(anytime[2])
            atomic += Seconds(anytime[3])
        else:
            raise NotImplementedError
    atomic_map = dict(
        days=Days,
        hours=Hours,
        minutes=Minutes,
        seconds=Seconds,
        milliseconds=Atomic,
    )
    for key, value in anytimekw.items():
        if key not in atomic_map:
            raise NotImplementedError
        atomic += atomic_map[key](value).atomic
    return atomic

# FIXME: *_in should return float
class Time(Atomic):
    def __init__(self, *anytime: AnyTime, **anytimekw) -> None:
        if len(anytime) == 1 and isinstance(anytime[0], (int, float)):
            raise NotImplementedError
        elif len(anytime) == 1 and isinstance(anytime[0], Atomic):
            atomic = anytime[0].atomic
        else:
            atomic = asatomic(*anytime, **anytimekw)
        super().__init__(atomic)

    def copy(self):
        return Time(self.atomic)

    @property
    def atomic_in(self) -> Atomic:
        return Atomic(self.atomic % 1000)

    @property
    def seconds_in(self) -> 'Seconds':
        return Seconds(int(self.seconds) % 60)

    @property
    def minutes_in(self) -> 'Minutes':
        return Minutes(int(self.minutes) % 60)

    @property
    def hours_in(self) -> 'Hours':
        return Hours(int(self.hours) % 24)

    @property
    def days_in(self) -> 'Days':
        return Days(int(self.days))

    def __float__(self) -> float:
        raise NotImplementedError

    def __str__(self) -> TimeString:
        return _atomic_to_string(self)

    @uptype
    def __add__(self, other: AnyTime) -> Atomic:
        if isinstance(other, (int, float)):
            raise NotImplementedError
        return super().__add__(other)

    @uptype
    def __sub__(self, other: AnyTime) -> Atomic:
        if isinstance(other, (int, float)):
            raise NotImplementedError
        return super().__sub__(other)

class Seconds(Atomic):
    def __init__(self, amount):
        if isinstance(amount, (int, float)):
            amount = Atomic(amount * 1000).atomic
        super().__init__(amount)

    def __float__(self) -> float:
        return self.seconds

    def __str__(self) -> TimeString:
        return TimeString(
            value='{} s'.format(_num_to_str(float(self))),
            long='{} seconds'.format(_num_to_str(float(self)))
        )

    @uptype
    def __add__(self, other: AnyTime) -> 'Atomic':
        if isinstance(other, (int, float)):
            other = Seconds(other)
        return super().__add__(other)

    @uptype
    def __sub__(self, other: AnyTime) -> 'Atomic':
        if isinstance(other, (int, float)):
            other = Seconds(other)
        return super().__sub__(other)

class Minutes(Atomic):
    def __init__(self, amount):
        if isinstance(amount, (int, float)):
            amount = Seconds(amount * 60).atomic
        super().__init__(amount)

    def __float__(self) -> float:
        return self.minutes

    def __str__(self) -> TimeString:
        return TimeString(
            value='{} min'.format(_num_to_str(float(self))),
            long='{} minutes'.format(_num_to_str(float(self)))
        )

    @uptype
    def __add__(self, other: AnyTime) -> 'Atomic':
        if isinstance(other, (int, float)):
            other = Minutes(other)
        return super().__add__(other)

    @uptype
    def __sub__(self, other: AnyTime) -> 'Atomic':
        if isinstance(other, (int, float)):
            other = Minutes(other)
        return super().__sub__(other)

class Hours(Atomic):
    def __init__(self, amount):
        if isinstance(amount, (int, float)):
            amount = Minutes(amount * 60).atomic
        super().__init__(amount)

    def __float__(self) -> float:
        return self.hours

    def __str__(self) -> TimeString:
        return TimeString(
            value='{} h'.format(_num_to_str(float(self))),
            long='{} hours'.format(_num_to_str(float(self))),
        )

    @uptype
    def __add__(self, other: AnyTime) -> Atomic:
        if isinstance(other, (int, float)):
            other = Hours(other)
        return super().__add__(other)

    @uptype
    def __sub__(self, other: AnyTime) -> Atomic:
        if isinstance(other, (int, float)):
            other = Hours(other)
        return super().__sub__(other)

class Days(Atomic):
    def __init__(self, amount):
        if isinstance(amount, (int, float)):
            amount = Hours(amount * 24).atomic
        super().__init__(amount)

    def __float__(self) -> float:
        return self.days

    def __str__(self) -> TimeString:
        return TimeString(
            value='{} d'.format(_num_to_str(float(self))),
            long='{} days'.format(_num_to_str(float(self))),
        )

    @uptype
    def __add__(self, other: AnyTime) -> Atomic:
        if isinstance(other, (int, float)):
            other = Days(other)
        return super().__add__(other)

    @uptype
    def __sub__(self, other: AnyTime) -> Atomic:
        if isinstance(other, (int, float)):
            other = Days(other)
        return super().__sub__(other)

# class Weeks(Atomic):
#     def __init__(self, amount):
#         raise NotImplementedError

def timerange(*args):
    start = end = step = 0
    if len(args) == 1:
        end = args[0]
        step = Seconds(1)
    elif len(args) == 2:
        start, end = args
        step = Seconds(1)
    elif len(args) == 3:
        start, end, step = args
    else:
        msg = 'The function gets maximum three arguments'
        raise AssertionError(msg)
    start = Atomic(start).atomic
    end = Atomic(end).atomic
    step = Atomic(step).atomic
    for v in range(start, end, step):
        yield Time(Atomic(v))
