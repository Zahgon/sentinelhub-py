"""
Download process for Sentinel Hub Statistical API
"""

from __future__ import annotations

import concurrent.futures
import copy
import json
import logging
from typing import Any

from ..exceptions import DownloadFailedException
from ..types import JsonDict
from .models import DownloadRequest, DownloadResponse
from .sentinelhub_client import SentinelHubDownloadClient

LOGGER = logging.getLogger(__name__)


class SentinelHubStatisticalDownloadClient(SentinelHubDownloadClient):
    """A special download client for Sentinel Hub Statistical API

    Beside a normal download from Sentinel Hub services it implements an additional process of retrying and caching.
    """

    _RETRIABLE_ERRORS = ("EXECUTION_ERROR", "TIMEOUT")

    def __init__(self, *args: Any, n_interval_retries: int = 1, max_retry_threads: int = 5, **kwargs: Any):
        """
        :param n_interval_retries: Number of retries if a request fails just for a certain timestamp. (This parameter
            is experimental and might be changed in the future.)
        :param max_retry_threads: Number of threads used for retrying. (This parameter is experimental and might be
            changed in the future.)
        """
        super().__init__(*args, **kwargs)

        self.n_interval_retries = n_interval_retries
        self.max_retry_threads = max_retry_threads

    def _process_response(self, request: DownloadRequest, response: DownloadResponse) -> DownloadResponse:
        """After downloading the response for all timestamps this method handles redownload for those timestamps for
        which download failed."""
        pass

    def _download_per_interval(self, request: DownloadRequest, time_intervals: dict[int, Any]) -> dict:
        """Download statistics per each time interval"""
        pass

    def _execute_single_stat_download(self, request: DownloadRequest) -> JsonDict:
        """Makes sure a download for a single time interval is retried"""
        pass

    def _has_retriable_error(self, stat_info: JsonDict) -> bool:
        """Checks if a dictionary of Stat API info for a single time interval has an error that can fixed by retrying
        a request
        """
        pass
