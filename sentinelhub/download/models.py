"""
Module implementing model classes to store download-related parameters and data.
"""

from __future__ import annotations

import datetime as dt
import functools
import hashlib
import json
import os
import platform
import warnings
from dataclasses import dataclass, field, fields
from typing import Any

from requests import Response

from ..constants import MimeType, RequestType
from ..decoding import decode_data
from ..exceptions import SHRuntimeWarning
from ..io_utils import read_data, write_data
from ..types import JsonDict


@dataclass
class DownloadRequest:
    """A class defining a single download request.

    The class is a container with all parameters needed to execute a single download request and save or return
    downloaded data.

    :param url: A URL from where to download
    :param headers: Headers of an HTTP request
    :param request_type: Type of request, either GET or POST. Default is `RequestType.GET`
    :param post_values: A dictionary of values that will be sent with a POST request. Default is `None`
    :param use_session: A flag that specifies if the download request will require a session header
    :param data_type: An expected file format of downloaded data. Default is `MimeType.RAW`
    :param save_response: A flag defining if the downloaded data will be saved to disk. Default is `False`.
    :param data_folder: A folder path where the fetched data will be (or already is) saved. Default is `None`
    :param filename: A custom filename where the data will be saved. By default, data will be saved in a folder
        which name are hashed request parameters.
    :param return_data: A flag defining if the downloaded data will be returned as an output of download procedure.
        Default is `True`.
    :param extra_params: Any additional parameters.
    """

    url: str | None = None
    headers: JsonDict = field(default_factory=dict)
    request_type: RequestType = RequestType.GET
    post_values: JsonDict | None = None
    use_session: bool = False
    data_type: MimeType = MimeType.RAW
    save_response: bool = False
    data_folder: str | None = None
    filename: str | None = None
    return_data: bool = True
    extra_params: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Additional parsing of init parameters."""
        self.request_type = RequestType(self.request_type)
        self.data_type = MimeType(self.data_type)

    def __hash__(self) -> int:
        """This dataclass is mutable, but we still assign its id as its hash."""
        return id(self)

    def raise_if_invalid(self) -> None:
        """Method that raises an error if something is wrong with request parameters

        :raises: ValueError
        """
        pass

    def get_request_params(self, include_metadata: bool = False) -> JsonDict:
        """Provides parameters that define the request in form of a dictionary

        :param include_metadata: A flag defining if also metadata parameters should be included, such as headers and
            current time
        :return: A dictionary of parameters
        """
        pass

    def get_hashed_name(self) -> str:
        """It takes request url and payload and calculates a unique hashed string from them.

        :return: A hashed string
        """
        pass

    def get_relative_paths(self) -> tuple[str | None, str]:
        """A method that calculates file paths relative to `data_folder`

        :return: Returns a pair of file paths, a request payload path and a response path. If request path is not
            defined it returns `None`.
        """
        pass

    def get_storage_paths(self) -> tuple[str | None, str | None]:
        """A method that calculates file paths where request payload and response will be saved.

        :return: Returns a pair of file paths, a request payload path and a response path. Each of them can also be
            `None` if it is not defined.
        """
        pass

    @staticmethod
    def _check_path(file_path: str) -> None:
        """Checks file path and warns about potential problems during saving"""
        pass


@dataclass(frozen=True)
class DownloadResponse:
    """A class defining a single download response.

    :param request: A download request object for which the response is obtained.
    :param content: Raw encoded data of the response.
    :param headers: Headers obtained with the response.
    :param status_code: Status code of the response.
    :param elapsed: Number of seconds it took to obtain the response.
    """

    request: DownloadRequest
    content: bytes
    headers: JsonDict = field(default_factory=dict)
    status_code: int | None = None
    elapsed: float | None = None

    @classmethod
    def from_response(cls, response: Response, request: DownloadRequest) -> DownloadResponse:
        """Creates `DownloadResponse` object from obtained from a service response and request info.

        :param: A service response object.
        :param: A request for which response was obtained.
        :return: An instance of a download response object.
        """
        pass

    @classmethod
    def from_local(cls, request: DownloadRequest) -> DownloadResponse:
        """Creates `DownloadResponse` object by loading it from locally cached data.

        :param request: A request object for which data is cached locally.
        :return: An instance of a download response object.
        """
        pass

    def to_local(self) -> None:
        """Caches data about a request and a response locally."""
        pass

    @property
    def response_type(self) -> MimeType:
        """Provides the expected mime type of the response data."""
        pass

    def decode(self) -> Any:
        """Decodes binary data into a Python object."""
        pass

    def derive(self, **params: Any) -> DownloadResponse:
        """Create a new response by changing some parameters of the existing one.

        :param params: Any of `DownloadResponse` attributes.
        :return: A new instance of `DownloadResponse` with modified parameters
        """
        pass
