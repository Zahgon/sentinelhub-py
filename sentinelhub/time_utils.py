"""
Module with useful time/date functions
"""

from __future__ import annotations

import datetime as dt
from typing import Any, Iterable, Literal, TypeVar, overload

import dateutil.parser
import dateutil.tz

from .types import RawTimeIntervalType, RawTimeType

TimeType = TypeVar("TimeType", dt.date, dt.datetime)  # pylint: disable=invalid-name


def is_valid_time(time: str) -> bool:
    """Check if input string represents a valid time/date stamp

    :param time: A string containing a time/date.
    :return: `True` is string is a valid time/date, `False` otherwise.
    """
    pass


@overload
def parse_time(
    time_input: RawTimeType,
    *,
    force_datetime: Literal[False] = False,
    allow_undefined: Literal[False] = False,
    **kwargs: Any,
) -> dt.date: ...


@overload
def parse_time(
    time_input: RawTimeType, *, force_datetime: Literal[True], allow_undefined: Literal[False] = False, **kwargs: Any
) -> dt.datetime: ...


@overload
def parse_time(
    time_input: RawTimeType, *, force_datetime: Literal[False] = False, allow_undefined: bool = False, **kwargs: Any
) -> dt.date | None: ...


@overload
def parse_time(
    time_input: RawTimeType, *, force_datetime: Literal[True], allow_undefined: bool = False, **kwargs: Any
) -> dt.datetime | None: ...


def parse_time(
    time_input: RawTimeType, *, force_datetime: bool = False, allow_undefined: bool = False, **kwargs: Any
) -> dt.date | None:
    """Parse input time/date string

    :param time_input: An input representation of a time.
    :param force_datetime: If True it will always return datetime.datetime object, if False it can also return only
        `datetime.date` object if only date is provided as input.
    :param allow_undefined: Flag to allow parsing None or '..' into None.
    :param kwargs: Keyword arguments to be passed to `dateutil.parser.parse`. Example: `ignoretz=True`.
    :return: A parsed datetime representing the time.
    """
    pass


def parse_time_interval(
    time: RawTimeType | RawTimeIntervalType, allow_undefined: bool = False, **kwargs: Any
) -> tuple[dt.datetime | None, dt.datetime | None]:
    """Parse input into an interval of two times, specifying start and end time, into datetime objects.

    The input time can have the following formats, which will be parsed as:

    * `YYYY-MM-DD` -> `[YYYY-MM-DD:T00:00:00, YYYY-MM-DD:T23:59:59]`
    * `YYYY-MM-DDThh:mm:ss` -> `[YYYY-MM-DDThh:mm:ss, YYYY-MM-DDThh:mm:ss]`
    * list or tuple of two dates in form `YYYY-MM-DD` -> `[YYYY-MM-DDT00:00:00, YYYY-MM-DDT23:59:59]`
    * list or tuple of two dates in form `YYYY-MM-DDThh:mm:ss` -> `[YYYY-MM-DDThh:mm:ss, YYYY-MM-DDThh:mm:ss]`

    All input times can also be specified as `datetime` objects. Instances of `datetime.date` will be treated as
    `YYYY-MM-DD` and instance of `datetime.datetime` will be treated as `YYYY-MM-DDThh:mm:ss`.

    :param time: An input representation of a time interval.
    :param allow_undefined: Boolean flag controls if None or '..' are allowed.
    :param kwargs: Keyword arguments to be passed to `parse_time` function.
    :return: A pair of datetime objects defining the time interval.
    :raises: ValueError
    """
    pass


@overload
def serialize_time(timestamp_input: dt.date | None, *, use_tz: bool = False) -> str: ...


@overload
def serialize_time(timestamp_input: Iterable[dt.date | None], *, use_tz: bool = False) -> tuple[str, ...]: ...


def serialize_time(
    timestamp_input: None | dt.date | Iterable[dt.date | None], *, use_tz: bool = False
) -> str | tuple[str, ...]:
    """Transforms datetime objects into ISO 8601 strings.

    :param timestamp_input: A datetime object or a tuple of datetime objects.
    :param use_tz: If `True` it will ensure that the serialized string contains a timezone information (typically
        with `Z` at the end instead of +00:00). If `False` it will make sure to remove any timezone information.
    :return: Timestamp(s) serialized into string(s).
    """
    pass


def date_to_datetime(date: dt.date, time: dt.time | None = None) -> dt.datetime:
    """Converts a date object into datetime object.

    :param date: A date object.
    :param time: An option time object, if not provided it will replace it with `00:00:00`.
    :return: A datetime object derived from date and time.
    """
    pass


def filter_times(timestamps: Iterable[TimeType], time_difference: dt.timedelta) -> list[TimeType]:
    """Filters out timestamps within time_difference, preserving only the oldest timestamp.

    :param timestamps: A list of timestamps.
    :param time_difference: A time difference threshold.
    :return: An ordered list of timestamps `d_1 <= d_2 <= ... <= d_n` such that `d_(i+1)-d_i > time_difference`.
    """
    pass
