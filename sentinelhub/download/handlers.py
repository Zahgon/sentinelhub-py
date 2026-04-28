"""
Module implementing error handlers which can occur during download procedure
"""

from __future__ import annotations

import functools
import logging
import time
from typing import Callable, Protocol, TypeVar

import requests

from ..config import SHConfig
from ..decoding import decode_sentinelhub_err_msg
from ..exceptions import DownloadFailedException
from .models import DownloadRequest


class _HasConfig(Protocol):
    """Interface of objects with a config."""

    config: SHConfig


Self = TypeVar("Self")
SelfWithConfig = TypeVar("SelfWithConfig", bound=_HasConfig)
T = TypeVar("T")


LOGGER = logging.getLogger(__name__)


def fail_user_errors(download_func: Callable[[Self, DownloadRequest], T]) -> Callable[[Self, DownloadRequest], T]:
    """Decorator function for handling user errors"""
    def new_download_func(request):
        pass

    pass


def retry_temporary_errors(
    download_func: Callable[[SelfWithConfig, DownloadRequest], T],
) -> Callable[[SelfWithConfig, DownloadRequest], T]:
    """Decorator function for handling server and connection errors"""
    def new_download_func(request):
        pass

    pass


def fail_missing_file(download_func: Callable[[Self, DownloadRequest], T]) -> Callable[[Self, DownloadRequest], T]:
    """A decorator for raising an error if a file is missing"""
    def new_download_func(request):
        pass

    pass


def _is_temporary_problem(exception: Exception) -> bool:
    """Checks if the obtained exception is temporary and if download attempt should be repeated

    :param exception: Exception raised during download
    :return: `True` if exception is temporary and `False` otherwise
    """
    pass


def _create_download_failed_message(exception: Exception, url: str | None) -> str:
    """Creates message describing why download has failed

    :param exception: Exception raised during download
    :param url: A URL from where download was attempted
    :return: Error message
    """
    pass
