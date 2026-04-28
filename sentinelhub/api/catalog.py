"""
A client interface for `Sentinel Hub Catalog API <https://docs.sentinel-hub.com/api/latest/api/catalog>`__.
"""

from __future__ import annotations

import datetime as dt
from typing import Any, Iterable, Literal

from ..base import FeatureIterator
from ..config import SHConfig
from ..data_collections import DataCollection, OrbitDirection
from ..geometry import CRS, BBox, Geometry
from ..time_utils import filter_times, parse_time, parse_time_interval, serialize_time
from ..types import JsonDict, RawTimeIntervalType, RawTimeType
from .base import SentinelHubService
from .utils import remove_undefined


class SentinelHubCatalog(SentinelHubService):
    """The main class for interacting with Sentinel Hub Catalog API

    For more details about certain endpoints and parameters check
    `Catalog API documentation <https://docs.sentinel-hub.com/api/latest/api/catalog>`__.
    """

    @staticmethod
    def _get_service_url(base_url: str) -> str:
        """Provides URL to Catalog API"""
        pass

    def get_info(self) -> JsonDict:
        """Provides the main information that define Sentinel Hub Catalog API

        `Catalog API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/getLandingPage>`__

        :return: A service payload with information
        """
        pass

    def get_conformance(self) -> JsonDict:
        """Get information about specifications that this API conforms to

        `Catalog API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/getConformanceDeclaration>`__

        :return: A service payload with information
        """
        pass

    def get_collections(self) -> list[JsonDict]:
        """Provides a list of collections that are available to a user

        `Catalog API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/getCollections>`__

        :return: A list of collections with information
        """
        pass

    def get_collection(self, collection: DataCollection | str) -> JsonDict:
        """Provides information about given collection

        `Catalog API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/describeCollection>`__

        :param collection: A data collection object or a collection ID
        :return: Information about a collection
        """
        pass

    def get_feature(self, collection: DataCollection, feature_id: str) -> JsonDict:
        """Provides information about a single feature in a collection

        `Catalog API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/getFeature>`__

        :param collection: A data collection object or a collection ID
        :param feature_id: A feature ID
        :return: Information about a feature in a collection
        """
        pass

    # pylint: disable=too-many-arguments
    def search(
        self,
        collection: DataCollection | str,
        *,
        time: RawTimeType | RawTimeIntervalType = None,
        bbox: BBox | None = None,
        geometry: Geometry | None = None,
        ids: list[str] | None = None,
        filter: None | str | JsonDict = None,  # pylint: disable=redefined-builtin # noqa: A002
        filter_lang: Literal["cql2-text", "cql2-json"] = "cql2-text",
        filter_crs: str | None = None,
        fields: JsonDict | None = None,
        distinct: str | None = None,
        limit: int = 100,
        **kwargs: Any,
    ) -> CatalogSearchIterator:
        """Catalog STAC search

        `Catalog API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/postSearchSTAC>`__

        :param collection: A data collection object or a collection ID
        :param time: A time interval or a single time. It can either be a string in form  YYYY-MM-DDThh:mm:ss or
            YYYY-MM-DD or a datetime object
        :param bbox: A search bounding box, it will always be reprojected to WGS 84 before being sent to the service.
            Re-projection will be done with BBox.transform_bounds method which can produce a slightly larger bounding
            box. If that is a problem then transform a BBox object into a Geometry object and search with geometry
            parameter instead.
        :param geometry: A search geometry, it will always reprojected to WGS 84 before being sent to the service.
            This parameter is defined with parameter `intersects` at the service.
        :param ids: A list of feature ids as defined in service documentation
        :param filter: A STAC filter in CQL2, described in Catalog API documentation
        :param filter_lang: How to parse CQL2 of the `filter` input, described in Catalog API documentation
        :param filter_crs: The CRS used by spatial literals in the 'filter' value, provided in URI form. Example input
            is `"http://www.opengis.net/def/crs/OGC/1.3/CRS84"`
        :param fields: A dictionary of fields to include or exclude described in Catalog API documentation
        :param distinct: A special query attribute described in Catalog API documentation
        :param limit: A number of results to return per each request. At the end iterator will always provide all
            results the difference is only in how many requests it will have to make in the background.
        :param kwargs: Any other parameters that will be passed directly to the service
        """
        pass

    @staticmethod
    def _parse_collection_id(collection: str | DataCollection) -> str:
        """Extracts catalog collection id from an object defining a collection."""
        pass

    def _prepare_filters(
        self,
        filter_query: None | str | JsonDict,
        collection: DataCollection | str,
        filter_lang: Literal["cql2-text", "cql2-json"],
    ) -> None | str | JsonDict:
        """Asserts that the input coincides with the selected filter language and adds any collection filters."""
        pass

    @staticmethod
    def _get_data_collection_filters(data_collection: DataCollection | str) -> dict[str, str]:
        """Builds a `field: value` dictionary to create filters for catalog API corresponding to a data collection
        definition.
        """
        pass


class CatalogSearchIterator(FeatureIterator[JsonDict]):
    """Searches a catalog with a given query and provides results"""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.next: JsonDict | None = None

    def _fetch_features(self) -> Iterable[JsonDict]:
        """Collects more results from the service"""
        pass

    def get_timestamps(self) -> list[dt.datetime]:
        """Provides features timestamps

        :return: A list of sensing times
        """
        pass

    def get_geometries(self) -> list[Geometry]:
        """Provides features geometries

        :return: A list of geometry objects with CRS
        """
        pass

    def get_ids(self) -> list[str]:
        """Provides features IDs

        :return: A list of IDs
        """
        pass


def get_available_timestamps(
    bbox: BBox,
    time_interval: RawTimeIntervalType | None,
    data_collection: DataCollection,
    *,
    time_difference: dt.timedelta | None = None,
    ignore_tz: bool = True,
    maxcc: float | None = None,
    config: SHConfig | None = None,
) -> list[dt.datetime]:
    """Helper function to search for all available timestamps for a given area and query parameters.

    :param bbox: A bounding box of the search area.
    :param data_collection: A collection specifying the satellite data source for finding available timestamps.
    :param time_interval: A time interval from which to provide the timestamps.
    :param time_difference: Shortest allowed time difference. Consecutive timestamps will be skipped if too close to
        the previous one. Defaults to keeping all timestamps.
    :param ignore_tz: Ignore the time zone part in the returned timestamps. Default is True.
    :param maxcc: Maximum cloud coverage filter from interval [0, 1]. Default is None.
    :param config: The SH configuration object.
    :return: A list of timestamps of available observations.
    """
    pass
