"""
Module implementing the main download client class
"""

from __future__ import annotations

import json
import logging
import os
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import nullcontext
from typing import Any, Iterable
from xml.etree import ElementTree

import requests
from tqdm.auto import tqdm

from ..config import SHConfig
from ..constants import MimeType, RequestType
from ..exceptions import (
    DownloadFailedException,
    HashedNameCollisionException,
    MissingDataInRequestException,
    SHDeprecationWarning,
    SHRuntimeWarning,
)
from ..io_utils import read_data
from ..types import JsonDict
from .handlers import fail_user_errors, retry_temporary_errors
from .models import DownloadRequest, DownloadResponse

LOGGER = logging.getLogger(__name__)


class DownloadClient:
    """A basic download client object

    It does the following:

    - downloads the data with multiple threads in parallel,
    - handles any exceptions that occur during download,
    - decodes downloaded data,
    - reads and writes locally stored/cached data
    """

    def __init__(self, *, redownload: bool = False, raise_download_errors: bool = True, config: SHConfig | None = None):
        """
        :param redownload: If `True` the data will always be downloaded again. By default, this is set to `False` and
            the data that has already been downloaded and saved to an expected location will be read from the
            location instead of being downloaded again.
        :param raise_download_errors: If `True` any error in download process will be raised as
            `DownloadFailedException`. If `False` failed downloads will only raise warnings.
        :param config: An instance of configuration class
        """
        self.redownload = redownload
        self.raise_download_errors = raise_download_errors

        self.config = config or SHConfig()

    def download(
        self,
        download_requests: Iterable[DownloadRequest],
        max_threads: int | None = None,
        decode_data: bool = True,
        show_progress: bool = False,
    ) -> list[Any]:
        """Download one or multiple requests, provided as a request list.

        :param download_requests: A list of requests to be executed.
        :param max_threads: Maximum number of threads to be used for download in parallel. The default is
            `max_threads=None` which will use the number of processors on the system multiplied by 5.
        :param decode_data: If `True` it will decode data otherwise it will return it in form of a `DownloadResponse`
            objects which contain binary data and response metadata.
        :param show_progress: Whether a progress bar should be displayed while downloading
        :return: A list of results
        """
        pass

    def _single_download_decoded(self, request: DownloadRequest) -> Any:
        """Downloads a response and decodes it into data. By decoding a single response"""
        pass

    def _single_download(self, request: DownloadRequest) -> DownloadResponse | None:
        """Method for downloading a single request."""
        pass

    @retry_temporary_errors
    @fail_user_errors
    def _execute_download(self, request: DownloadRequest) -> DownloadResponse:
        """A default way of executing a single download request"""
        pass

    @staticmethod
    def _check_cached_request_is_matching(request: DownloadRequest, request_path: str | None) -> None:
        """Ensures that the cached request matches the current one. Serves as protection against hash collisions"""
        pass

    def _process_response(self, _: DownloadRequest, response: DownloadResponse) -> DownloadResponse:
        """This method is meant to be overwritten by inherited implementations of the client object."""
        pass

    def get_json(
        self,
        url: str,
        post_values: JsonDict | None = None,
        headers: JsonDict | None = None,
        request_type: RequestType | None = None,
        **kwargs: Any,
    ) -> JsonDict | list | str | None:
        """Download request as JSON data type

        :param url: A URL from where the data will be downloaded
        :param post_values: A dictionary of parameters for a POST request
        :param headers: A dictionary of additional request headers
        :param request_type: A type of HTTP request to make. If not specified, then it will be a GET request if
            `post_values=None` and a POST request otherwise
        :param kwargs: Any other parameters that are passed to DownloadRequest class
        :return: JSON data parsed into Python objects
        """
        pass

    def get_json_dict(self, url: str, *args: Any, extract_key: str | None = None, **kwargs: Any) -> JsonDict:
        """Download request as JSON data type, failing if the result is not a dictionary

        For other parameters see `get_json` method.

        :param url: A URL from where the data will be downloaded
        :param extract_key: If provided, the field is automatically extracted, checked, and returned
        """
        pass

    def get_xml(self, url: str, **kwargs: Any) -> ElementTree.ElementTree:
        """Download request as XML data type

        :param url: url to Sentinel Hub's services or other sources from where the data is downloaded
        :param kwargs: Any other parameters that are passed to DownloadRequest class
        :return: request response as XML instance
        """
        pass
