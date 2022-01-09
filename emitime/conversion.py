import datetime as dt



def str_to_datetime(value: str) -> dt.datetime:
    raise NotImplementedError


def add_conversion_methods():
    from plum import add_conversion_method
    add_conversion_method(type_from=str, type_to=dt.datetime, f=str_to_datetime)
