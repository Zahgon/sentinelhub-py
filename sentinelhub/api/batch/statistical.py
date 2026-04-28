"""
Module implementing an interface with
`Sentinel Hub Batch Processing API <https://docs.sentinel-hub.com/api/latest/api/batch-statistical/>`__.
"""

# ruff: noqa: FA100
# do not use `from __future__ import annotations`, it clashes with `dataclass_json`
import datetime as dt
import logging
from dataclasses import dataclass, field
from typing import Any, Optional, Sequence, Union

from dataclasses_json import CatchAll, LetterCase, Undefined, dataclass_json
from dataclasses_json import config as dataclass_config
from typing_extensions import deprecated

from ...exceptions import SHDeprecationWarning
from ...types import Json, JsonDict
from ..base_request import InputDataDict
from ..statistical import SentinelHubStatistical
from ..utils import AccessSpecification, datetime_config, enum_config, remove_undefined, s3_specification
from .base import BaseBatchClient, BaseBatchRequest, BatchRequestStatus, BatchUserAction

LOGGER = logging.getLogger(__name__)

BatchStatisticalRequestType = Union[str, dict, "BatchStatisticalRequest"]


class SentinelHubBatchStatistical(BaseBatchClient["BatchStatisticalRequest"]):
    """An interface class for Sentinel Hub Batch Statistical API

    Check `Batch Statistical API <https://docs.sentinel-hub.com/api/latest/reference/#tag/batch_statistical>`__ for more
    information.
    """

    s3_specification = staticmethod(s3_specification)

    @staticmethod
    def _get_service_url(base_url: str) -> str:
        """Provides URL to Batch Statistical API"""
        pass

    def create(
        self,
        *,
        input_features: AccessSpecification,
        input_data: Sequence[Union[JsonDict, InputDataDict]],
        aggregation: JsonDict,
        calculations: Optional[JsonDict],
        output: AccessSpecification,
        **kwargs: Any,
    ) -> "BatchStatisticalRequest":
        """Create a new batch statistical request

        `Batch Statistical API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/createNewBatchStatisticsRequest>`__
        """
        pass

    def create_from_request(
        self,
        statistical_request: SentinelHubStatistical,
        input_features: AccessSpecification,
        output: AccessSpecification,
        **kwargs: Any,
    ) -> "BatchStatisticalRequest":
        """Create a new batch statistical request from an existing statistical request.

        :param statistical_request: A Sentinel Hub Statistical request.
        :param input_features: A dictionary describing the S3 path and credentials to access the input GeoPackage.
        :param output: A dictionary describing the S3 path and credentials to access the output folder.
        :param kwargs: Any other arguments to be added to a dictionary of parameters
        :returns: A Batch Statistical request with the same calculations and aggregations but using geometries
            specified in the input GeoPackage.
        """
        pass

    def get_request(self, batch_request: BatchStatisticalRequestType) -> "BatchStatisticalRequest":
        """Collects information about a single batch request

        `Batch Statistical API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/getSingleBatchStatisticalRequestById>`__

        :return: Batch request info
        """
        pass

    def get_status(self, batch_request: BatchStatisticalRequestType) -> JsonDict:
        """Collects information about a status of a request

        `Batch Statistical API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/batchStatisticalGetStatus>`__

        :return: Batch request status dictionary
        """
        pass

    def start_analysis(self, batch_request: BatchStatisticalRequestType) -> Json:
        """Starts analysis of a batch job request

        `Batch Statistical API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/batchStatisticalAnalyse>`__

        :param batch_request: It could be a batch request object, a raw batch request payload or only a batch
            request ID.
        """
        pass

    def start_job(self, batch_request: BatchStatisticalRequestType) -> Json:
        """Starts running a batch job

        `Batch Statistical API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/batchStartStatisticalRequest>`__

        :param batch_request: It could be a batch request object, a raw batch request payload or only a batch
            request ID.
        """
        pass

    @deprecated("The method `cancel_job` has been replaced with use `stop_job`.", category=SHDeprecationWarning)
    def cancel_job(self, batch_request: BatchStatisticalRequestType) -> Json:
        """Cancels a batch job

        `Batch Statistical API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/batchCancelStatisticalRequest>`__

        :param batch_request: It could be a batch request object, a raw batch request payload or only a batch
            request ID.
        """
        pass

    def stop_job(self, batch_request: BatchStatisticalRequestType) -> Json:
        """Stop a batch job

        `Batch Statistical API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#tag/batch_statistical/operation/batchStopStatisticalRequest>`__

        :param batch_request: It could be a batch request object, a raw batch request payload or only a batch
            request ID.
        """
        pass


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class BatchStatisticalRequest(BaseBatchRequest):  # pylint: disable=abstract-method
    """A dataclass object that holds information about a batch statistical request"""

    # dataclass_json doesn't handle parameter inheritance correctly
    # pylint: disable=duplicate-code

    request_id: str = field(metadata=dataclass_config(field_name="id"))
    completion_percentage: float
    request: dict
    status: BatchRequestStatus = field(metadata=enum_config(BatchRequestStatus))
    user_id: Optional[str] = None
    created: Optional[dt.datetime] = field(metadata=datetime_config, default=None)
    cost_pu: Optional[float] = field(metadata=dataclass_config(field_name="costPU"), default=None)
    user_action: Optional[BatchUserAction] = field(metadata=enum_config(BatchUserAction), default=None)
    user_action_updated: Optional[str] = field(metadata=datetime_config, default=None)
    error: Optional[str] = None
    other_data: CatchAll = field(default_factory=dict)

    _REPR_PARAM_NAMES = (
        "request_id",
        "created",
        "status",
        "user_action",
        "cost_pu",
        "error",
        "completion_percentage",
    )
