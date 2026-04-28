"""
Implementation of base Sentinel Hub interfaces
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any

from ..base import DataRequest
from ..constants import MimeType, MosaickingOrder, RequestType, ResamplingType
from ..data_collections import DataCollection, OrbitDirection
from ..download import DownloadRequest
from ..geometry import BBox, Geometry
from ..time_utils import RawTimeIntervalType, parse_time_interval, serialize_time
from .utils import _update_other_args


class SentinelHubBaseApiRequest(DataRequest, metaclass=ABCMeta):
    """A base class for Sentinel Hub interfaces"""

    _SERVICE_ENDPOINT = ""
    payload: dict[str, Any] = {}  # noqa: RUF012

    @property
    @abstractmethod
    def mime_type(self) -> MimeType:
        """The mime type of the request."""

    def create_request(self) -> None:
        """Prepares a download request"""
        pass

    @staticmethod
    def input_data(
        data_collection: DataCollection,
        *,
        identifier: str | None = None,
        time_interval: RawTimeIntervalType | None = None,
        maxcc: float | None = None,
        mosaicking_order: MosaickingOrder | None = None,
        upsampling: ResamplingType | None = None,
        downsampling: ResamplingType | None = None,
        other_args: dict[str, Any] | None = None,
    ) -> InputDataDict:
        """Generate the `input data` part of the request body

        :param data_collection: One of supported Process API data collections.
        :param identifier: A collection identifier that can be referred to in the evalscript. Parameter is referenced
            as `"id"` in service documentation. To learn more check
            `data fusion documentation <https://docs.sentinel-hub.com/api/latest/data/data-fusion>`__.
        :param time_interval: A time interval with start and end date of the form YYYY-MM-DDThh:mm:ss or YYYY-MM-DD or
            a datetime object
        :param maxcc: Maximum accepted cloud coverage of an image. Float between 0.0 and 1.0. Default is 1.0.
        :param mosaicking_order: Mosaicking order, which has to be either 'mostRecent', 'leastRecent' or 'leastCC'.
        :param upsampling: A type of upsampling to apply on data
        :param downsampling: A type of downsampling to apply on data
        :param other_args: Additional dictionary of arguments. If provided, the resulting dictionary will get updated
            by it.
        :return: A dictionary-like object that also contains additional attributes
        """
        pass

    @staticmethod
    def bounds(
        bbox: BBox | None = None, geometry: Geometry | None = None, other_args: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Generate a `bound` part of the API request

        :param bbox: Bounding box describing the area of interest.
        :param geometry: Geometry describing the area of interest.
        :param other_args: Additional dictionary of arguments. If provided, the resulting dictionary will get updated
            by it.
        """
        pass

    def _get_base_url(self) -> str:
        """It decides which base URL to use. Restrictions from data collection definitions overrule the
        settings from config object. In case different collections have different restrictions then
        `SHConfig.sh_base_url` breaks the tie in case it matches one of the data collection URLs.
        """
        pass


class InputDataDict(dict):
    """An input data dictionary which also holds additional attributes"""

    def __init__(self, input_data_dict: dict[str, Any], *, service_url: str | None = None):
        """
        :param input_data_dict: A normal dictionary with input parameters
        :param service_url: A service URL defined by a data collection
        """
        super().__init__(input_data_dict)
        self.service_url = service_url

    def __repr__(self) -> str:
        """Modified dictionary representation that also shows additional attributes"""
        normal_dict_repr = super().__repr__()
        return f"{self.__class__.__name__}({normal_dict_repr}, service_url={self.service_url})"


def _get_data_filters(
    data_collection: DataCollection,
    time_interval: RawTimeIntervalType | None,
    maxcc: float | None,
    mosaicking_order: MosaickingOrder | None,
) -> dict[str, Any]:
    """Builds a dictionary of data filters for Process API"""
    pass


def _get_data_collection_filters(data_collection: DataCollection) -> dict[str, Any]:
    """Builds a dictionary of filters for Process API from a data collection definition"""
    pass


def _get_processing_params(upsampling: ResamplingType | None, downsampling: ResamplingType | None) -> dict[str, Any]:
    """Builds a dictionary of processing parameters for Process API"""
    pass
