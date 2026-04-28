"""
Module for communication with Sentinel Hub Opensearch service.

For more search parameters check
`service description <http://opensearch.sentinel-hub.com/resto/api/collections/Sentinel2/describe.xml>`__.
"""

from __future__ import annotations

import datetime as dt
import logging
from typing import Iterable, Iterator
from urllib.parse import urlencode

from ..config import SHConfig
from ..constants import CRS
from ..download import DownloadClient
from ..geometry import BBox
from ..time_utils import RawTimeIntervalType, RawTimeType, parse_time, parse_time_interval, serialize_time
from ..types import JsonDict

LOGGER = logging.getLogger(__name__)


class TileMissingException(Exception):
    """This exception is raised when requested tile is missing at Sentinel Hub Opensearch service"""


def get_tile_info_id(tile_id: str) -> JsonDict:
    """Get basic information about image tile

    :param tile_id: original tile identification string provided by ESA (e.g.
        'S2A_OPER_MSI_L1C_TL_SGS__20160109T230542_A002870_T10UEV_N02.01')
    :return: dictionary with info provided by Opensearch REST service
    :raises: TileMissingException if no tile with tile ID `tile_id` exists
    """
    pass


def get_tile_info(
    tile: str, time: RawTimeType | RawTimeIntervalType, aws_index: int | None = None, all_tiles: bool = False
) -> JsonDict | list[JsonDict]:
    """Get basic information about image tile

    :param tile: tile name (e.g. ``'T10UEV'``)
    :param time: A single date or a time interval
    :param aws_index: index of tile on AWS
    :param all_tiles: If `True` it will return list of all tiles otherwise only the first one
    :return: dictionary (or list of dictionaries) with info provided by Opensearch REST service
    """
    pass


def get_area_info(bbox: BBox, date_interval: RawTimeIntervalType, maxcc: float | None = None) -> list[JsonDict]:
    """Get information about all images from specified area and time range

    :param bbox: bounding box of requested area
    :param date_interval: a pair of time strings in ISO8601 format
    :param maxcc: filter images by maximum percentage of cloud coverage
    :return: iterator of dictionaries containing info provided by Opensearch REST service
    """
    pass


def get_area_dates(bbox: BBox, date_interval: RawTimeIntervalType, maxcc: float | None = None) -> list[dt.date]:
    """Get list of times of existing images from specified area and time range

    :param bbox: bounding box of requested area
    :param date_interval: a pair of time strings in ISO8601 format
    :param maxcc: filter images by maximum percentage of cloud coverage
    :return: list of time strings in ISO8601 format
    """
    pass


def reduce_by_maxcc(result_list: Iterable[JsonDict], maxcc: float) -> list[JsonDict]:
    """Filter list image tiles by maximum cloud coverage

    :param result_list: list of dictionaries containing info provided by Opensearch REST service
    :param maxcc: filter images by maximum percentage of cloud coverage
    :return: list of dictionaries containing info provided by Opensearch REST service
    """
    pass


def search_iter(
    tile_id: str | None = None,
    bbox: BBox | None = None,
    start_date: RawTimeType | None = None,
    end_date: RawTimeType | None = None,
    absolute_orbit: int | None = None,
    config: SHConfig | None = None,
) -> Iterator[JsonDict]:
    """A generator function that implements OpenSearch search queries and returns results

    All parameters for search are optional.

    :param tile_id: original tile identification string provided by ESA (e.g.
                    'S2A_OPER_MSI_L1C_TL_SGS__20160109T230542_A002870_T10UEV_N02.01')
    :param bbox: bounding box of requested area
    :param start_date: beginning of time range
    :param end_date: end of time range
    :param absolute_orbit: An absolute orbit number of Sentinel-2 L1C products as defined by ESA
    :return: An iterator returning dictionaries with info provided by Sentinel Hub OpenSearch REST service
    :param config: A custom instance of config class to override parameters from the saved configuration.
    """
    pass


def _prepare_url_params(
    tile_id: str | None,
    bbox: BBox | None,
    end_date: dt.date | None,
    start_date: dt.date | None,
    absolute_orbit: int | None,
) -> JsonDict:
    """Constructs dict with URL params

    :param tile_id: original tile identification string provided by ESA (e.g.
                    'S2A_OPER_MSI_L1C_TL_SGS__20160109T230542_A002870_T10UEV_N02.01')
    :param bbox: bounding box of requested area in WGS84 CRS
    :param start_date: beginning of time range
    :param end_date: end of time range
    :param absolute_orbit: An absolute orbit number of Sentinel-2 L1C products as defined by ESA
    :return: dictionary with parameters as properties when arguments not None
    """
    pass
