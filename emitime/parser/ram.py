__all__ = (
    "MomentParserRAM",
    "IntervalParserRAM"
)

import pickle
from typing import Any, Callable, Dict

import xxhash
from emitime.base import Interval, Moment


class ParserRAM:
    def __init__(self, factory: Callable):
        self._mem: Dict[bytes, Any] = dict()
        self._hash = xxhash.xxh3_128_digest
        self._make = factory

    def __call__(self, *args, **kwargs) -> Any:
        dump = pickle.dumps(args) + pickle.dumps(kwargs)
        hash = self._hash(dump)
        if hash in self._mem:
            return self._mem[hash]
        obj = Moment(*args, **kwargs)
        self._mem[hash] = obj
        return obj


class MomentParserRAM(ParserRAM):
    def __init__(self):
        super().__init__(Moment)

    def __call__(self, *args, **kwargs) -> Moment:
        return super().__call__(*args, **kwargs)


class IntervalParserRAM(ParserRAM):
    def __init__(self):
        super().__init__(Interval)

    def __call__(self, *args, **kwargs) -> Interval:
        return super().__call__(*args, **kwargs)
