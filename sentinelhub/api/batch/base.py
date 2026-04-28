"""
Module containing shared code of Batch Process API and Batch Statistical API
"""

# ruff: noqa: FA100
# do not use `from __future__ import annotations`, it clashes with `dataclass_json` (even through inheritance)
from abc import ABCMeta
from enum import Enum
from typing import Generic, Iterable, Optional, Sequence, Type, TypeVar, Union

from ...constants import RequestType
from ...types import Json, JsonDict
from ..base import SentinelHubService

BatchRequestType = TypeVar("BatchRequestType", bound="BaseBatchRequest")  # pylint: disable=invalid-name
RequestSpec = Union[str, dict, BatchRequestType]
Self = TypeVar("Self")


class BatchRequestStatus(Enum):
    """An enum class with all possible batch request statuses"""

    CREATED = "CREATED"
    ANALYSING = "ANALYSING"
    ANALYSIS_DONE = "ANALYSIS_DONE"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"
    STOPPED = "STOPPED"


class BatchUserAction(Enum):
    """An enum class with all possible batch user actions"""

    START = "START"
    ANALYSE = "ANALYSE"
    STOP = "STOP"
    NONE = "NONE"


class StoppedStatusReason(Enum):
    """Description of why job status is STOPPED"""

    OUT_OF_PU = "OUT_OF_PU"
    USER_ACTION = "USER_ACTION"
    UNHEALTHY = "UNHEALTHY"


class BaseBatchClient(SentinelHubService, Generic[BatchRequestType], metaclass=ABCMeta):
    """Class containing common methods and helper functions for Batch Client classes"""

    def _call_job(self, batch_request: RequestSpec, endpoint_name: str) -> Json:
        """Makes a POST request to the service that triggers a processing job"""
        pass

    def _get_processing_url(self, request_id: Optional[str] = None) -> str:
        """Creates a URL for the batch statistical endpoint"""
        pass

    @staticmethod
    def _parse_request_id(data: RequestSpec) -> str:
        """Parses batch request id from multiple possible inputs"""
        pass


class BaseBatchRequest:
    """Class containing helper functions for Batch Request classes"""

    _REPR_PARAM_NAMES: Sequence[str]

    request_id: str
    error: Optional[str]
    status: BatchRequestStatus

    def to_dict(self) -> JsonDict:
        """Transforms itself into a dictionary form."""
        pass

    @classmethod
    def from_dict(cls: Type[Self], json_dict: JsonDict) -> Self:
        """Transforms itself into a dictionary form."""
        pass

    def __repr__(self) -> str:
        """A representation that shows the basic parameters of a batch job"""
        repr_params = {name: getattr(self, name) for name in self._REPR_PARAM_NAMES if getattr(self, name) is not None}
        repr_params_str = "\n  ".join(f"{name}={value}" for name, value in repr_params.items())
        return f"{self.__class__.__name__}(\n  {repr_params_str}\n  ...\n)"

    def raise_for_status(
        self,
        status: Union[str, BatchRequestStatus, Iterable[Union[str, BatchRequestStatus]]] = BatchRequestStatus.FAILED,
    ) -> None:
        """Raises an error in case batch request has a given status

        :param status: One or more status codes on which to raise an error. The default is `'FAILED'`.
        :raises: RuntimeError
        """
        pass
