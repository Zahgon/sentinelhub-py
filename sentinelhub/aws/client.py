"""
Module implementing a download client that is adjusted to download from AWS
"""

import logging
import warnings
from typing import Any, Dict, Optional
from typing_extensions import deprecated

try:
    from boto3 import Session
    from botocore.exceptions import NoCredentialsError
except ImportError as import_exception:
    raise ImportError(
        "To use AWS functionalities of this package you have to install sentinelhub[AWS] package extension"
    ) from import_exception

from ..config import SHConfig
from ..download.client import DownloadClient
from ..download.handlers import fail_missing_file
from ..download.models import DownloadRequest, DownloadResponse
from ..exceptions import AwsDownloadFailedException, SHDeprecationWarning

LOGGER = logging.getLogger(__name__)


@deprecated(
    "AWS functionality will remain in the codebase for now, but won't be actively maintained.",
    category=SHDeprecationWarning,
)
class AwsDownloadClient(DownloadClient):
    """An AWS download client class"""

    GLOBAL_S3_CLIENTS: Dict[str, Any] = {}

    def __init__(self, *args: Any, boto_params: Optional[Dict[str, Any]] = None, **kwargs: Any):
        """
        :param args: Positional arguments propagated to `DownloadClient` class.
        :param boto_params: A dictionary of extra parameters that will be propagated to `botocore.client.S3.get_object`
            method. E.g. `{"RequestPayer": "requester"}`.
        :param kwargs: Keyword arguments propagated to `DownloadClient` class.
        """
        super().__init__(*args, **kwargs)

        self.boto_params = boto_params or {}

    @fail_missing_file
    def _execute_download(self, request: DownloadRequest) -> DownloadResponse:
        """Executes a download procedure"""
        pass

    @classmethod
    def get_s3_client(cls, config: SHConfig) -> Any:
        """Provides a s3 client object"""
        pass

    def _do_download(self, request: DownloadRequest, s3_client: Any) -> bytes:
        """Does the download from s3"""
        pass

    @staticmethod
    def is_s3_request(request: DownloadRequest) -> bool:
        """Checks if data has to be downloaded from AWS s3 bucket

        :return: `True` if url describes location at AWS s3 bucket and `False` otherwise
        """
        pass
