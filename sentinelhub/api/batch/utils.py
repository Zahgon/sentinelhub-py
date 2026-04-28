"""
Module implementing utilities for working with batch jobs.
"""

from __future__ import annotations

import logging
import time
from typing import Union

from tqdm.auto import tqdm

from ...config import SHConfig
from ...types import JsonDict
from .base import BatchRequestStatus
from .process import BatchProcessClient, BatchProcessRequest
from .statistical import BatchStatisticalRequest, SentinelHubBatchStatistical

LOGGER = logging.getLogger(__name__)

BatchStatisticalRequestSpec = Union[str, dict, BatchStatisticalRequest]


_MIN_SLEEP_TIME = 60
_DEFAULT_SLEEP_TIME = 120
_MIN_STAT_SLEEP_TIME = 15
_DEFAULT_STAT_SLEEP_TIME = 30
_MIN_ANALYSIS_SLEEP_TIME = 5
_DEFAULT_ANALYSIS_SLEEP_TIME = 10


def monitor_batch_process_job(
    request: BatchProcessRequest,
    client: BatchProcessClient,
    sleep_time: int = _DEFAULT_SLEEP_TIME,
    analysis_sleep_time: int = _DEFAULT_ANALYSIS_SLEEP_TIME,
) -> BatchProcessRequest:
    """A utility function that keeps checking the progress of the batch processing job. Returns an updated version of
    the request

    Notes:

      - Before calling this function make sure to start a batch job by calling `BatchProcessingClient.start_job` method.
        In case a batch job is still being analysed this function will wait until the analysis ends.
      - This function will be continuously collecting information from Sentinel Hub service. To avoid making too many
        requests please make sure to adjust `sleep_time` parameter.

    :param request: The request to monitor.
    :param client: A batch processing client with appropriate configuration that is used to monitor the batch job.
    :param sleep_time: Number of seconds to sleep between consecutive progress bar updates.
    :param analysis_sleep_time: Number of seconds between consecutive status updates during analysis phase.
    """
    pass


def monitor_batch_statistical_job(
    batch_request: BatchStatisticalRequestSpec,
    config: SHConfig | None = None,
    sleep_time: int = _DEFAULT_STAT_SLEEP_TIME,
    analysis_sleep_time: int = _DEFAULT_ANALYSIS_SLEEP_TIME,
) -> JsonDict:
    """A utility function that keeps checking the completion percentage of a Batch Statistical request until complete.

    Notes:

      - Before calling this function make sure to start a batch job via `SentinelHubBatchStatistical.start_job` method.
        In case a batch job is still being analysed this function will wait until the analysis ends.
      - Some information about the progress of this function is reported to logging level INFO.

    :param batch_request: An object with information about a batch request. Alternatively, it could only be a batch
        request id or a payload.
    :param config: A configuration object with required parameters `sh_client_id`, `sh_client_secret`, and
        `sh_auth_base_url` which is used for authentication and `sh_base_url` which defines the service deployment
        where Batch API will be called.
    :param sleep_time: Number of seconds to sleep between consecutive progress bar updates.
    :param analysis_sleep_time: Number of seconds between consecutive status updates during analysis phase.
    :return: Final status of the batch request.
    """
    pass


def monitor_batch_process_analysis(
    request: BatchProcessRequest,
    client: BatchProcessClient,
    sleep_time: int = _DEFAULT_ANALYSIS_SLEEP_TIME,
) -> BatchProcessRequest:
    """A utility function that is waiting until analysis phase of a batch job finishes and regularly checks its status.
    In case analysis phase failed it raises an error at the end.

    :param request: The request to monitor.
    :param client: A batch processing client with appropriate configuration that is used to monitor the batch job.
    :param sleep_time: Number of seconds between consecutive status updates during analysis phase.
    """
    pass


def monitor_batch_statistical_analysis(
    batch_request: BatchStatisticalRequestSpec,
    config: SHConfig | None = None,
    sleep_time: int = _DEFAULT_ANALYSIS_SLEEP_TIME,
) -> BatchStatisticalRequest:
    """A utility function that is waiting until analysis phase of a batch job finishes and regularly checks its status.
    In case analysis phase failed it raises an error at the end.

    :param batch_request: An object with information about a batch request. Alternatively, it could only be a batch
        request id or a payload.
    :param config: A configuration object with required parameters `sh_client_id`, `sh_client_secret`, and
        `sh_auth_base_url` which is used for authentication and `sh_base_url` which defines the service deployment
        where Batch API will be called.
    :param sleep_time: Number of seconds between consecutive status updates during analysis phase.
    :return: Batch request info
    """
    pass
