__all__ = [
    'DateTime',
]

from emitime import date as d
from emitime import time as t

class DateTime:
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @property
    def date(self) -> d.Date:
        raise NotImplementedError

    @property
    def time(self) -> t.Time:
        raise NotImplementedError
