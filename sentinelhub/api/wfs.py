"""
Interface of
`Sentinel Hub Web Feature Service (WFS) <https://www.sentinel-hub.com/develop/api/ogc/standard-parameters/wfs/>`__.
"""

from __future__ import annotations

import datetime as dt
from typing import Iterable
from urllib.parse import urlencode

import shapely.geometry

from ..base import FeatureIterator
from ..config import SHConfig
from ..constants import CRS, MimeType, ServiceType, SHConstants
from ..data_collections import DataCollection
from ..download import SentinelHubDownloadClient
from ..geometry import BBox
from ..time_utils import parse_time, parse_time_interval, serialize_time
from ..types import JsonDict, RawTimeIntervalType, RawTimeType


class WebFeatureService(FeatureIterator[JsonDict]):
    """Class for interaction with Sentinel Hub WFS service

    The class is an iterator over info about all available satellite tiles for requested parameters. It collects data
    from Sentinel Hub service only during the first iteration. During next iterations it returns already obtained data.
    The data is in the same order as returned by the service.

    For more info check `WFS documentation <https://www.sentinel-hub.com/develop/api/ogc/standard-parameters/wfs/>`__.
    """

    def __init__(
        self,
        bbox: BBox,
        time_interval: RawTimeType | RawTimeIntervalType,
        *,
        data_collection: DataCollection,
        maxcc: float = 1.0,
        config: SHConfig | None = None,
    ):
        """
        :param bbox: Bounding box of the requested image. Coordinates must be in the specified coordinate reference
            system.
        :param time_interval: interval with start and end date of the form YYYY-MM-DDThh:mm:ss or YYYY-MM-DD
        :param data_collection: A collection of requested satellite data
        :param maxcc: Maximum accepted cloud coverage of an image. Float between 0.0 and 1.0. Default is 1.0.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.config = config or SHConfig()
        if not self.config.instance_id:
            raise ValueError(
                "Sentinel Hub instance ID should be provided with SHConfig or saved into the configuration file."
                "Check https://sentinelhub-py.readthedocs.io/en/latest/configure.html for more info."
            )

        self.bbox = bbox

        self.latest_time_only = time_interval == SHConstants.LATEST
        if not self.latest_time_only:
            self.time_interval = parse_time_interval(time_interval)
        else:
            self.time_interval = dt.datetime(year=1985, month=1, day=1), dt.datetime.now()

        self.data_collection = data_collection
        self.maxcc = maxcc
        self.max_features_per_request = 1 if self.latest_time_only else self.config.max_wfs_records_per_query

        client = SentinelHubDownloadClient(config=self.config)
        url = self._build_service_url()
        params = self._build_request_params()

        super().__init__(client, url, params)
        self.next: int = 0

    def _build_service_url(self) -> str:
        """Creates a base URL for WFS service"""
        pass

    def _build_request_params(self) -> JsonDict:
        """Builds URL parameters for WFS service"""
        pass

    def _fetch_features(self) -> Iterable[JsonDict]:
        """Collects data from WFS service"""
        pass

    def get_dates(self) -> list[dt.date | None]:
        """Returns a list of acquisition times from tile info data

        :return: List of acquisition times in the order returned by WFS service.
        """
        pass

    def get_geometries(self) -> list[shapely.geometry.MultiPolygon]:
        """Returns a list of geometries from tile info data

        :return: List of multipolygon geometries in the order returned by WFS service.
        """
        pass

    def get_tiles(self) -> list[tuple[str, str, int]]:
        """Returns list of tiles with tile name, date and AWS index

        :return: List of tiles in form of (tile_name, date, aws_index)
        """
        pass

    @staticmethod
    def _parse_tile_url(tile_url: str) -> tuple[str, str, int]:
        """Extracts tile name, data and AWS index from tile URL

        :param tile_url: Location of tile at AWS
        :return: Tuple in a form (tile_name, date, aws_index)
        """
        pass

    def _sentinel1_product_check(self, tile_info: JsonDict) -> bool:
        """Checks if Sentinel-1 tile info match the data collection definition"""
        pass
