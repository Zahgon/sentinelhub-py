"""
Module implementing a rate-limited multithreaded download client for downloading from Sentinel Hub service
"""

from __future__ import annotations

import logging
import time
import warnings
from threading import Lock
from typing import Any, Callable, ClassVar, TypeVar

import requests
from requests import Response

from ..config import SHConfig
from ..constants import SHConstants
from ..exceptions import OutOfRequestsException, SHRateLimitWarning, SHRuntimeWarning
from ..types import JsonDict
from .client import DownloadClient
from .handlers import fail_user_errors, retry_temporary_errors
from .models import DownloadRequest, DownloadResponse
from .rate_limit import SentinelHubRateLimit
from .session import SentinelHubSession

LOGGER = logging.getLogger(__name__)

T = TypeVar("T")


class SentinelHubDownloadClient(DownloadClient):
    """Download client specifically configured for download from Sentinel Hub service"""

    _CACHED_SESSIONS: ClassVar[dict[tuple[str, str], SentinelHubSession]] = {}
    _UNIVERSAL_CACHE_KEY = "universal-user", "default-url"

    def __init__(self, *, session: SentinelHubSession | None = None, default_retry_time: float = 30, **kwargs: Any):
        """
        :param session: If a session object is provided here then this client instance will always use only the
            provided session. Otherwise, it will either use a cached session or create a new session and cache
            it.
        :param default_retry_time: The default waiting time (in seconds) when retrying after getting a TOO_MANY_REQUESTS
            response without appropriate retry headers.
        :param kwargs: Optional parameters from DownloadClient
        """
        super().__init__(**kwargs)

        if session is not None and not isinstance(session, SentinelHubSession):
            raise ValueError(
                f"A session parameter has to be an instance of {SentinelHubSession.__name__} or None, but "
                f"{session} was given"
            )
        self.session = session
        self.default_retry_time = default_retry_time * 1000  # rescale to milliseconds

        self.rate_limit = SentinelHubRateLimit(num_processes=self.config.number_of_download_processes)
        self.lock: Lock | None = None

    def download(self, *args: Any, **kwargs: Any) -> Any:
        """The main download method

        :param args: Passed to `DownloadClient.download`
        :param kwargs: Passed to `DownloadClient.download`
        """
        pass

    @retry_temporary_errors
    @fail_user_errors
    def _execute_download(self, request: DownloadRequest) -> DownloadResponse:
        """
        Executes the download with a single thread and uses a rate limit object, which is shared between all threads
        """
        pass

    def _execute_thread_safe(self, thread_unsafe_function: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Executes a function inside a thread lock and handles potential errors"""
        pass

    def _do_download(self, request: DownloadRequest) -> Response:
        """Runs the download"""
        pass

    def _prepare_headers(self, request: DownloadRequest) -> JsonDict:
        """Prepares final headers by potentially joining them with session headers. Note that in the current
        implementation of this method request headers have priority to overwrite default and session headers with the
        same keys.
        """
        pass

    def _get_session_headers(self) -> JsonDict:
        """Provides up-to-date session headers

        Note that calling session_headers property triggers update if session has expired therefore this has to be
        called in a thread-safe way
        """
        pass

    def get_session(self) -> SentinelHubSession:
        """Provides the session object used by the client

        :return: A Sentinel Hub session object
        """
        pass

    @staticmethod
    def cache_session(session: SentinelHubSession, universal: bool = False) -> None:
        """Cache a Sentinel Hub session for to be reused by all instances of `SentinelHubDownloadClient` and its child
        classes within the same Python runtime environment.

        :param session: A session object to be cached.
        :param universal: By default a session is cached for a specific OAuth user ID and Sentinel Hub deployment. But
            if this flag is set to `True` it will cache session for any OAuth user ID and deployment. The intended
            purpose of this parameter is that when a session is sent to a remote processing instance, which doesn't
            have configured Sentinel Hub OAuth credentials, then the session can still be used even without credentials.
        """
        pass

    @staticmethod
    def _get_cache_key(config_or_session: SentinelHubSession | SHConfig) -> tuple[str, str]:
        """Calculates a cache key for the given session or config object. The key consists of an OAuth client ID and
        a base service URL.
        """
        pass

    @staticmethod
    def clear_cache() -> None:
        """Clears cached sessions."""
        pass
