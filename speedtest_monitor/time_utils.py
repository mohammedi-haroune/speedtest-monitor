from typing import Callable, Dict, Union
from datetime import datetime
import pandas as pd

# It's a map between Time's fields and either an int or a callable
GrouperKwargs = Dict[str, Union[int, Callable[[int], int]]]

Time = Union[datetime, pd.Timestamp]
Grouper = Callable[[Time], Time]

UNITS = ['microsecond', 'nanosecond', 'second', 'minute', 'hour', 'day', 'month']


def round_to(to: int):
    def round_(value: int):
        """Round a value to the nearst nth ~:`to`
        
        It could be used to group time objects together, say group time by quarter
        
        >>> round_to(15)(5)
        15
        >>> round_to(15)(15)
        15
        >>> round_to(15)(23)
        30
        >>> round_to(15)(59)
        45
        """
        return int(value / to)*to
    return round_


def grouper_kwargs_for_scope(scope):
    [n, unit] = scope.split('-')

    n = int(n)

    # plural nouns are accepted
    if unit.endswith('s'):
        unit = unit[:-1]

    if unit not in UNITS:
        raise ValueError(f'Unit {unit} not supported. Supported units are {UNITS}')

    grouper_kwargs = {}

    for u in UNITS:
        if u != unit:
            # set all preceeding units to zeros
            grouper_kwargs[u] = 0
        elif u == unit:
            grouper_kwargs[u] = round_to(n)
            return grouper_kwargs


def time_grouper(scope: str) -> Grouper:
    """Retruns a function that could be used in df.groupby to groupby datetime objects by hours, dates, ..."""
    kwargs = grouper_kwargs_for_scope(scope)
    def group_by_scope(timestamp: Time, replace_kwargs: GrouperKwargs = kwargs) -> Time:
        copy_kwargs = {}
        for param, value in replace_kwargs.items():
            if callable(value):
                copy_kwargs[param] = value(getattr(timestamp, param))
            else:
                copy_kwargs[param] = value
        return timestamp.replace(**copy_kwargs)
    return group_by_scope


def group_by(
    df: pd.DataFrame,
    scope: str = 'hour',
    agg: str = 'max',
) -> pd.DataFrame:
    by = time_grouper(scope)
    return df.groupby(by).agg(agg)
