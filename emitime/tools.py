__all__ = ("momentrange",)

from .base import Interval, Moment
import typing as tp


def momentrange(start, stop, step) -> tp.Iterable[Moment]:
    start = Moment(start).datetime
    stop = Moment(stop).datetime
    step = Interval(step).timedelta
    # return start, stop, step
    assert stop != start
    side = True
    if step.total_seconds() > 0.001:
        assert start < stop
    elif step.total_seconds() < -0.001:
        side = False
        assert stop < start
    else:
        raise ValueError(step)
    while start < stop if side else start > stop:
        yield Moment(start)
        start = start + step
