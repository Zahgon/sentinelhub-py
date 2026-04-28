"""
Utility tools for writing unit tests for packages which rely on `sentinelhub-py`
"""

from __future__ import annotations

import os
from typing import Any, Callable

import numpy as np
import pytest


def get_input_folder(current_file: str) -> str:
    """Use fixtures if possible. This is meant only for test cases"""
    pass


def get_output_folder(current_file: str) -> str:
    """Use fixtures if possible. This is meant only for test cases"""
    pass


def assert_statistics_match(
    data: np.ndarray,
    exp_shape: tuple[int, ...] | None = None,
    exp_dtype: None | type | np.dtype = None,
    exp_min: float | None = None,
    exp_max: float | None = None,
    exp_mean: float | None = None,
    exp_median: float | None = None,
    exp_std: float | None = None,
    rel_delta: float | None = None,
    abs_delta: float | None = None,
) -> None:
    """Validates basic statistics of data array
    :param data: Data array
    :param exp_shape: Expected shape
    :param exp_dtype: Expected dtype
    :param exp_min: Expected minimal value
    :param exp_max: Expected maximal value
    :param exp_mean: Expected mean value
    :param exp_median: Expected median value
    :param exp_std: Expected standard deviation value
    :param rel_delta: Precision of validation (relative)
    :param abs_delta: Precision of validation (absolute)
    """
    pass
