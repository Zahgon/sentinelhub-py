"""
Module implementing Sentinel Hub session object
"""

from __future__ import annotations

import base64
import json
import logging
import time
import warnings
from multiprocessing.shared_memory import SharedMemory
from threading import Event, Thread
from typing import Any, ClassVar

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests import Response
from requests.exceptions import JSONDecodeError
from requests_oauthlib import OAuth2Session

from ..config import SHConfig
from ..constants import SHConstants
from ..download.handlers import fail_user_errors, retry_temporary_errors
from ..download.models import DownloadRequest
from ..exceptions import SHUserWarning
from ..types import JsonDict

LOGGER = logging.getLogger(__name__)


class SentinelHubSession:
    """Sentinel Hub authentication class

    The class will do OAuth2 authentication with Sentinel Hub service and store the token. It is able to refresh the
    token before it expires and decode user information from the token.

    For more info about Sentinel Hub authentication check
    `service documentation <https://docs.sentinel-hub.com/api/latest/api/overview/authentication/>`__.
    """

    DEFAULT_SECONDS_BEFORE_EXPIRY = 120
    # Following SH API documentation
    DEFAULT_HEADERS: ClassVar[dict[str, str]] = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(
        self,
        config: SHConfig | None = None,
        refresh_before_expiry: float | None = DEFAULT_SECONDS_BEFORE_EXPIRY,
        *,
        _token: JsonDict | None = None,
    ):
        """
        :param config: A config object containing Sentinel Hub OAuth credentials and the base URL of the service.
        :param refresh_before_expiry: A number of seconds before authentication token expiry at which time a refreshing
            mechanism is activated. When this is activated it means that whenever a valid token will be again
            required the `SentinelHubSession` will re-authenticate to Sentinel Hub service and obtain a new token.
            By default, the parameter is set to `60` seconds. If this parameter is set to `None` it will deactivate
            token refreshing and `SentinelHubSession` might provide a token that is already expired. This can be used
            to avoid re-authenticating too many times.
        """
        self.config = config or SHConfig()
        self.refresh_before_expiry = refresh_before_expiry

        token_fetching_required = _token is None or self.refresh_before_expiry is not None
        if token_fetching_required and not (self.config.sh_client_id and self.config.sh_client_secret):
            raise ValueError(
                "Configuration parameters 'sh_client_id' and 'sh_client_secret' have to be set in order "
                "to authenticate with Sentinel Hub service. Check "
                "https://sentinelhub-py.readthedocs.io/en/latest/configure.html for more info."
            )

        self._token = self._collect_new_token() if _token is None else _token

    @classmethod
    def from_token(cls, token: JsonDict) -> SentinelHubSession:
        """Create a session object from the given token. The created session is configured not to refresh its token.

        :param token: A dictionary containing token object.
        """
        pass

    @property
    def token(self) -> JsonDict:
        """Always up-to-date session's token

        :return: A token in a form of dictionary of parameters
        """
        pass

    def info(self) -> JsonDict:
        """Decode token to get token info"""
        pass

    @property
    def session_headers(self) -> dict[str, str]:
        """Provides session authorization headers

        :return: A dictionary with authorization headers.
        """
        pass

    def _collect_new_token(self) -> JsonDict:
        """Creates a download request and fetches a token from the service.

        Note that the `DownloadRequest` object is created only because retry decorators of `_fetch_token` method
        require it.
        """
        pass

    @retry_temporary_errors
    @fail_user_errors
    def _fetch_token(self, request: DownloadRequest) -> JsonDict:
        """Collects a new token from Sentinel Hub service"""
        pass

    @staticmethod
    def _compliance_hook(response: Response) -> Response:
        """Checks if a response from Sentinel Hub Authentication service has an error status code but no error message.

        By default, `requests_oauthlib` ignores status of a response and only looks at an error message in a
        response body. However, Sentinel Hub service can return a response with an error status code and
        without an error message. In such cases `requests_oauthlib` would raise a completely wrong error message. This
        hook makes sure that a correct error message is raised.

        It is important that in case of 5xx errors an error is always raised so that authentication can be retried.
        But in case of 4xx errors where response contains an error message this method intentionally doesn't raise
        an error so that `oauthlib` can later raise a more descriptive error.
        """
        pass


_DEFAULT_SESSION_MEMORY_NAME = "sh-session-token"
_NULL_MEMORY_VALUE = b"\x00"


class SessionSharingThread(Thread):
    """A thread for sharing a token from `SentinelHubSession` object in a shared memory object that can be accessed by
    other Python processes during multiprocessing parallelization.

    How to use it:

    .. code-block:: python

        thread = SessionSharingThread(session)
        thread.start()

        # Run a parallelization process here
        # Use collect_shared_session() to retrieve the session with other processes

        thread.join()
    """

    _EXTRA_MEMORY_BYTES = 100

    def __init__(self, session: SentinelHubSession, memory_name: str = _DEFAULT_SESSION_MEMORY_NAME, **kwargs: Any):
        """
        :param session: A Sentinel Hub session to be used for sharing its authentication token.
        :param memory_name: A unique name for the requested shared memory block.
        :param kwargs: Keyword arguments to be propagated to `threading.Thread` parent class.
        """
        super().__init__(**kwargs)

        self.session = session
        self.memory_name = memory_name

        if self.session.refresh_before_expiry is None:
            raise ValueError(f"Given instance of {self.session.__class__.__name__} must be self-refreshing")
        self._refresh_time = self.session.refresh_before_expiry

        self._stop_event = Event()
        self._is_memory_shared_event = Event()

    def start(self) -> None:
        """Start running the thread.

        After starting the thread it also waits for the token to be shared. This way no other process would try to
        access the memory before it even exists."""
        pass

    def run(self) -> None:
        """A running thread is running an infinite loop of sharing a token and waiting for token to expire. The loop
        ends only when the thread is stopped."""
        pass

    def _share_token(self, token: JsonDict) -> None:
        """A token is encoded into bytes and written into a shared memory block."""
        pass

    def _get_shared_memory(self, encoded_token: bytes) -> SharedMemory:
        """Provides a shared memory object.

        The method also handles a case where a shared memory with the same name would be left unclosed from before.
        Because the memory can be persistent and requires low-level knowledge of `multiprocessing.shared_memory` to
        close it manually this method will close it automatically and inform users about the problem.
        """
        pass

    def _create_shared_memory(self, encoded_token: bytes) -> SharedMemory:
        """Create a new shared memory space.

        Note that the `SharedMemory` object allocates extra `self._EXTRA_MEMORY_BYTES` bytes of memory because the
        length of encoded token can vary a bit.
        """
        pass

    def join(self, timeout: float | None = None) -> None:
        """The method stops the thread that would otherwise run indefinitely and joins it with the main thread.

        :param timeout: Parameter that is propagated to `threading.Thread.join` method.
        """
        pass


class SessionSharing:
    """An object that in the background runs a `SessionSharingThread` which shares a Sentinel Hub authentication
    token in a shared memory object that can be accessed by other Python processes during multiprocessing
    parallelization. The object also makes sure that the thread is always closed at the end.

    How to use it:

    .. code-block:: python

        with SessionSharing(session):
            # Run a parallelization process here
    """

    def __init__(self, session: SentinelHubSession, **kwargs: Any):
        """
        :param args: A Sentinel Hub session to be used for sharing its authentication token.
        :param kwargs: Keyword arguments to be propagated to `SessionSharingThread`.
        """
        self.thread = SessionSharingThread(session, **kwargs)

    def __enter__(self) -> None:
        """Starts running the session-sharing thread."""
        self.thread.start()

    def __exit__(self, *_: Any, **__: Any) -> None:
        """Closes the running session-sharing thread."""
        self.thread.join()


def collect_shared_session(memory_name: str = _DEFAULT_SESSION_MEMORY_NAME) -> SentinelHubSession:
    """This utility function is meant to be used in combination with `SessionSharingThread`. It retrieves an
    authentication token from the shared memory and returns it in an `SentinelHubSession` object.

    :param memory_name: A unique name of the requested shared memory block from where to read the session. It should
        match the one used in `SessionSharingThread`.
    :return: An instance of `SentinelHubSession` that contains the shared token but is not self-refreshing.
    """
    pass
