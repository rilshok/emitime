__all__ = ("momentrange",)

from .base import Interval, Moment
import typing as tp

def momentrange(start, stop, step) -> tp.Iterable[Moment]:
    start = Moment(start)
    stop = Moment(stop)
    step = Interval(step)
    assert stop != start
    side = True
    if step > "00:00:00.001":
        assert start < stop
    elif step < "-00:00:00.001":
        side = False
        assert stop < start
    else:
        raise ValueError(step)
    while start < stop if side else start > stop:
        yield start
        start = start + step
