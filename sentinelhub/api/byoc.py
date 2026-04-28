"""
Module implementing an interface with
`Sentinel Hub Bring Your Own COG API <https://docs.sentinel-hub.com/api/latest/api/byoc/>`__.
"""

# ruff: noqa: FA100
# do not use `from __future__ import annotations`, it clashes with `dataclass_json`
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Union

from dataclasses_json import CatchAll, LetterCase, Undefined, dataclass_json
from dataclasses_json import config as dataclass_config

from ..constants import MimeType, RequestType
from ..data_collections import DataCollection
from ..geometry import Geometry
from ..types import Json, JsonDict
from .base import BaseCollection, SentinelHubFeatureIterator, SentinelHubService
from .utils import datetime_config, geometry_config, remove_undefined

CollectionType = Union["ByocCollection", DataCollection, dict, str]
TileType = Union["ByocTile", dict, str]


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.INCLUDE)
@dataclass
class ByocCollectionBand:
    """Dataclass to hold BYOC collection band specification"""

    source: Optional[str] = None
    band_index: Optional[int] = None
    bit_depth: int = 8
    sample_format: str = "UINT"
    no_data: Optional[float] = None
    other_data: CatchAll = field(default_factory=dict)


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.INCLUDE)
@dataclass
class ByocCollectionAdditionalData:
    """Dataclass to hold BYOC collection additional data"""

    bands: Optional[Dict[str, ByocCollectionBand]] = None
    max_meters_per_pixel: Optional[float] = None
    max_meters_per_pixel_override: Optional[float] = None
    other_data: CatchAll = field(default_factory=dict)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ByocCollection(BaseCollection):
    """Dataclass to hold BYOC collection data"""

    additional_data: Optional[ByocCollectionAdditionalData] = None


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.INCLUDE)
@dataclass
class ByocTile:
    """Dataclass to hold BYOC tile data"""

    path: str
    status: Optional[str] = None
    tile_id: Optional[str] = field(metadata=dataclass_config(field_name="id"), default=None)
    tile_geometry: Optional[Geometry] = field(metadata=geometry_config, default=None)
    cover_geometry: Optional[Geometry] = field(metadata=geometry_config, default=None)
    created: Optional[datetime] = field(metadata=datetime_config, default=None)
    sensing_time: Optional[datetime] = field(metadata=datetime_config, default=None)
    ingestion_start: Optional[datetime] = field(metadata=datetime_config, default=None)
    additional_data: Optional[dict] = None
    other_data: CatchAll = field(default_factory=dict)


class SentinelHubBYOC(SentinelHubService):
    """An interface class for Sentinel Hub Bring your own COG (BYOC) API

    For more info check `BYOC API reference
    <https://docs.sentinel-hub.com/api/latest/reference/#tag/byoc_collection>`__.
    """

    @staticmethod
    def _get_service_url(base_url: str) -> str:
        """Provides URL to Catalog API"""
        pass

    def iter_collections(self, search: Optional[str] = None, **kwargs: Any) -> SentinelHubFeatureIterator:
        """Retrieve collections

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/getByocCollections>`__

        :param search: A search query
        :param kwargs: Any other request parameters
        :return: iterator over collections
        """
        pass

    def get_collection(self, collection: CollectionType) -> JsonDict:
        """Get collection by its id

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/getByocCollectionById>`__

        :param collection: a ByocCollection, dict or collection id string
        :return: dictionary of the collection
        """
        pass

    def create_collection(self, collection: CollectionType) -> JsonDict:
        """Create a new collection

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/createByocCollection>`__

        :param collection: ByocCollection object or a dictionary
        :return: dictionary of the created collection
        """
        pass

    def update_collection(self, collection: CollectionType) -> Json:
        """Update an existing collection

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/updateByocCollectionById>`__

        :param collection: ByocCollection object or a dictionary
        """
        pass

    def delete_collection(self, collection: CollectionType) -> Json:
        """Delete existing collection by its id

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/deleteByocCollectionById>`__

        :param collection: a ByocCollection, dict or collection id string
        """
        pass

    def copy_tiles(self, from_collection: CollectionType, to_collection: CollectionType) -> Json:
        """Copy tiles from one collection to another

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/copyByocCollectionTiles>`__

        :param from_collection: a ByocCollection, dict or collection id string
        :param to_collection: a ByocCollection, dict or collection id string
        """
        pass

    def iter_tiles(
        self, collection: CollectionType, sort: Optional[str] = None, path: Optional[str] = None, **kwargs: Any
    ) -> SentinelHubFeatureIterator:
        """Iterator over collection tiles

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/getByocCollectionTiles>`__

        :param collection: a ByocCollection, dict or collection id string
        :param sort: Order in which to return tiles
        :param path: An exact path where tiles are located
        :param kwargs: Any other request parameters
        :return: An iterator over payloads of tiles from the collection
        """
        pass

    def get_tile(self, collection: CollectionType, tile: TileType) -> JsonDict:
        """Get a tile of collection

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/getByocCollectionTileById>`__

        :param collection: a ByocCollection, dict or collection id string
        :param tile: a ByocTile, dict or tile id string
        :return: dictionary of the tile
        """
        pass

    def create_tile(self, collection: CollectionType, tile: TileType) -> JsonDict:
        """Create tile within collection

        `BYOC API reference <https://docs.sentinel-hub.com/api/latest/reference/#operation/createByocCollectionTile>`__

        :param collection: a ByocCollection, dict or collection id string
        :param tile: a ByocTile or dict
        :return: dictionary of the tile
        """
        pass

    def update_tile(self, collection: CollectionType, tile: TileType) -> Json:
        """Update a tile within collection

        `BYOC API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/updateByocCollectionTileById>`__

        :param collection: a ByocCollection, dict or collection id string
        :param tile: a ByocTile or dict
        """
        pass

    def delete_tile(self, collection: CollectionType, tile: TileType) -> Json:
        """Delete a tile from collection

        `BYOC API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/deleteByocCollectionTileById>`__

        :param collection: a ByocCollection, dict or collection id string
        :param tile: a ByocTile, dict or tile id string
        """
        pass

    def reingest_tile(self, collection: CollectionType, tile: TileType) -> Json:
        """Re-ingests a tile into a collection

        `BYOC API reference
        <https://docs.sentinel-hub.com/api/latest/reference/#operation/reingestByocCollectionTileById>`__

        :param collection: a ByocCollection, dict or collection id string
        :param tile: a ByocTile, dict or tile id string
        """
        pass

    @staticmethod
    def _parse_id(data: object) -> Optional[str]:
        pass

    @staticmethod
    def _to_dict(data: object) -> dict:
        """Constructs dict from an object (either dataclass or dict)"""
        pass
