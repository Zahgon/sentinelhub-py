"""
Module implementing some utility functions not suitable for other utility modules
"""

# ruff: noqa: FA100
# do not use `from __future__ import annotations`, it clashes with `dataclass_json`
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, Optional, Protocol, Union
from urllib.parse import urlencode

from dataclasses_json import CatchAll, LetterCase, Undefined, dataclass_json
from dataclasses_json import config as dataclass_config

from ..base import FeatureIterator
from ..config import SHConfig
from ..data_collections import DataCollection
from ..download.sentinelhub_client import SentinelHubDownloadClient
from ..exceptions import MissingDataInRequestException
from ..types import JsonDict
from .utils import datetime_config, remove_undefined


class SentinelHubService(metaclass=ABCMeta):
    """A base class for classes interacting with different Sentinel Hub APIs"""

    _DEFAULT_RETRY_TIME = 30

    def __init__(self, config: Optional[SHConfig] = None):
        """
        :param config: A configuration object with required parameters `sh_client_id`, `sh_client_secret`, and
            `sh_auth_base_url` which is used for authentication and `sh_base_url` which defines the service
            deployment that will be used.
        """
        self.config = config or SHConfig()

        base_url = self.config.sh_base_url.rstrip("/")
        self.service_url = self._get_service_url(base_url)

        self.client = SentinelHubDownloadClient(config=self.config, default_retry_time=self._DEFAULT_RETRY_TIME)

    @staticmethod
    @abstractmethod
    def _get_service_url(base_url: str) -> str:
        """Provides the URL to a specific service"""
        pass


class SentinelHubFeatureIterator(FeatureIterator[JsonDict]):
    """Feature iterator for the most common implementation of feature pagination at Sentinel Hub services"""

    def __init__(self, *args: Any, exception_message: Optional[str] = None, **kwargs: Any):
        """
        :param args: Arguments passed to FeatureIterator
        :param exception_message: A message to be raised if no features are found
        :param kwargs: Keyword arguments passed to FeatureIterator
        """
        self.exception_message = exception_message or "No data found"
        self.next: Optional[JsonDict] = None

        super().__init__(*args, **kwargs)

    def _fetch_features(self) -> Iterable[JsonDict]:
        """Collect more results from the service"""
        pass


class _AdditionalData(Protocol):
    """Describes minimum requirements for additional data passed to BaseCollection"""

    bands: Optional[Dict[str, Any]]


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.INCLUDE)
@dataclass
class BaseCollection:
    """Dataclass to hold data about a collection"""

    name: str
    s3_bucket: str
    additional_data: Optional[_AdditionalData]
    collection_id: Optional[str] = field(metadata=dataclass_config(field_name="id"), default=None)
    user_id: Optional[str] = None
    created: Optional[datetime] = field(metadata=datetime_config, default=None)
    no_data: Optional[Union[int, float]] = None
    other_data: CatchAll = field(default_factory=dict)

    def to_data_collection(self) -> DataCollection:
        """Returns a DataCollection enum for this collection"""
        pass
