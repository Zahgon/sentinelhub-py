"""
Module with statistics to dataframe transformation.
"""

from __future__ import annotations

from typing import Any, Iterable

from .time_utils import parse_time
from .types import JsonDict

_PANDAS_IMPORT_MESSAGE = (
    "To use this function you need to install the `pandas` library, which is not a dependency of sentinelhub-py."
)
_FULL_TIME_RANGE = "full time range"


def _extract_hist(hist_data: list[dict[str, float]]) -> tuple[list[float], list[float]]:
    """Transform Statistical API histogram into sequences of bins and counts

    :param hist_data: An input representation of Statistical API histogram data in a form of the low edges,
        the high edges, and the counts for each bin.
    :return: Statistical histogram bins and counts value as sequences.
    """
    pass


def _extract_stats(interval_output: JsonDict, exclude_stats: list[str]) -> dict[str, list[float] | float]:
    """Transform statistics into pandas.DataFrame entry

    :param interval_output: An input representation of statistics of an aggregation interval.
    :param exclude_stats: Statistics that will be excluded from output.
    :return: Statistics as a pandas.DataFrame entry.
    """
    pass


def _extract_response_data(response_data: list[JsonDict], exclude_stats: list[str]) -> list[JsonDict]:
    """Transform Statistical API response into a pandas.DataFrame

    :param response_data: An input representation of Statistical API response. The response is a list of JsonDict and
        each contains the statistics of an aggregation interval.
    :param exclude_stats: Statistics that will be excluded from output.
    :return: DataFrame entries of all aggregation intervals of a single geometry.
    """
    pass


def _is_batch_stat(result_data: JsonDict) -> bool:
    """Identifies whether the resulting data belongs to a batch statistical request or not"""
    pass


def _is_valid_batch_response(result_data: JsonDict) -> bool:
    """Identifies whether there is a valid batch response"""
    pass


def statistical_to_dataframe(result_data: list[JsonDict], exclude_stats: list[str] | None = None) -> Any:
    """Transform (Batch) Statistical API results into a pandas.DataFrame

    This function has a dependency of the `pandas` library, which is not a requirement of sentinelhub-py and needs to be
    installed before using the function.

    :param result_data: An input representation of (Batch) Statistical API result returned from
        `AwsBatchStatisticalResults.get_data()`. Each JsonDict in the list is a Statistical API response of an input
        geometry.
    :param exclude_stats: The statistic names defined in this parameter will be excluded from the output DataFrame.

    :return: Statistical dataframe.
    """
    pass


def _get_failed_intervals(response_data: list[JsonDict]) -> list[tuple[str, str]]:
    """Collect failed intervals of a single geometry from the (Batch) Statistical result

    :param response_data: An input representation of the (Batch) Statistical API response of a geometry.
    :return: The failed intervals for a geometry.
    """
    pass


def _get_failed_batch_response(result_data: JsonDict) -> str | list[tuple[str, str]]:
    """Collect failed responses

    :param result_data: An input representation of the (Batch) Statistical API result of a geometry.
    :return: Failed responses and responses with failed intervals
    """
    pass


def get_failed_statistical_requests(result_data: list[JsonDict]) -> list[JsonDict]:
    """Collect failed requests of (Batch) Statistical Results

    :param result_data: An input representation of (Batch) Statistical API result.
    :return: Failed requests of (Batch) Statistical Results.
    """
    pass
