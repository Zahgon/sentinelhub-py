"""
Module for working with large geographical areas
"""

from __future__ import annotations

import itertools
import json
import math
import os
from abc import ABCMeta, abstractmethod
from typing import Any, ClassVar, Iterable, TypeVar, cast

import shapely
import shapely.geometry
import shapely.ops
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry

from .api import SentinelHubCatalog
from .config import SHConfig
from .constants import CRS
from .data_collections import DataCollection
from .geo_utils import transform_point
from .geometry import BBox, Geometry, _BaseGeometry

T = TypeVar("T", float, int)


class AreaSplitter(metaclass=ABCMeta):
    """Abstract class for splitter classes. It implements common methods used for splitting large area into smaller
    parts.
    """

    def __init__(
        self,
        shape_list: Iterable[Polygon | MultiPolygon | _BaseGeometry],
        crs: CRS,
        reduce_bbox_sizes: bool = False,
    ):
        """
        :param shape_list: A list of geometrical shapes describing the area of interest
        :param crs: Coordinate reference system of the shapes in `shape_list`
        :param reduce_bbox_sizes: If `True` it will reduce the sizes of bounding boxes so that they will tightly fit
            the given geometry in `shape_list`.
        """
        self.crs = CRS(crs)
        self.shape_list = [self._parse_shape(shape, crs) for shape in shape_list]
        self.area_shape = self._join_shape_list(self.shape_list)
        self.reduce_bbox_sizes = reduce_bbox_sizes

        self.area_bbox = self.get_area_bbox()
        self.bbox_list, self.info_list = self._make_split()

    @staticmethod
    def _parse_shape(shape: Polygon | MultiPolygon | _BaseGeometry, crs: CRS) -> Polygon | MultiPolygon:
        """Helper method for parsing input shapes"""
        pass

    @staticmethod
    def _join_shape_list(shape_list: list[Polygon | MultiPolygon]) -> MultiPolygon:
        """Joins a list of shapes together into one shape

        :param shape_list: A list of geometrical shapes describing the area of interest
        :return: A multipolygon which is a union of shapes in given list
        """
        pass

    @abstractmethod
    def _make_split(self) -> tuple[list[BBox], list[dict[str, object]]]:
        """The abstract method where the splitting will happen"""
        pass

    def get_bbox_list(
        self,
        crs: CRS | None = None,
        buffer: None | float | tuple[float, float] = None,
        reduce_bbox_sizes: bool | None = None,
    ) -> list[BBox]:
        """Returns a list of bounding boxes that are the result of the split

        :param crs: Coordinate reference system in which the bounding boxes should be returned. If `None` the CRS will
            be the default CRS of the splitter.
        :param buffer: A percentage of each BBox size increase. This will cause neighbouring bounding boxes to overlap.
        :param reduce_bbox_sizes: If `True` it will reduce the sizes of bounding boxes so that they will tightly
            fit the given geometry in `shape_list`. This overrides the same parameter from constructor
        :return: List of bounding boxes
        """
        pass

    def get_geometry_list(self) -> list[Polygon | MultiPolygon]:
        """For each bounding box an intersection with the shape of entire given area is calculated. CRS of the returned
        shapes is the same as CRS of the given area.

        :return: List of polygons or multipolygons corresponding to the order of bounding boxes
        """
        pass

    def get_info_list(self) -> list[dict[str, object]]:
        """Returns a list of dictionaries containing information about bounding boxes obtained in split. The order in
        the list matches the order of the list of bounding boxes.

        :return: List of dictionaries
        """
        pass

    def get_area_shape(self) -> MultiPolygon:
        """Returns a single shape of entire area described with `shape_list` parameter

        :return: A multipolygon which is a union of shapes describing the area
        """
        pass

    def get_area_bbox(self, crs: CRS | None = None) -> BBox:
        """Returns a bounding box of the entire area

        :param crs: Coordinate reference system in which the bounding box should be returned. If `None` the CRS will
            be the default CRS of the splitter.
        :return: A bounding box of the area defined by the `shape_list`
        """
        pass

    def _intersects_area(self, bbox: BBox) -> bool:
        """Checks if the bounding box intersects the entire area

        :param bbox: A bounding box
        :return: `True` if bbox intersects the entire area else False
        """
        pass

    def _intersection_area(self, bbox: BBox) -> Polygon | MultiPolygon:
        """Calculates the intersection of a given bounding box and the entire area

        :param bbox: A bounding box
        :return: A shape of intersection
        """
        pass

    def _bbox_to_area_polygon(self, bbox: BBox) -> Polygon:
        """Transforms bounding box into a polygon object in the area CRS.

        :param bbox: A bounding box
        :return: A polygon
        """
        pass

    def _reduce_sizes(self, bbox_list: list[BBox]) -> list[BBox]:
        """Reduces sizes of bounding boxes"""
        pass


class BBoxSplitter(AreaSplitter):
    """A tool that splits the given area into smaller parts. Given the area it calculates its bounding box and splits
    it into smaller bounding boxes of equal size. Then it filters out the bounding boxes that do not intersect the
    area. If specified by user it can also reduce the sizes of the remaining bounding boxes to best fit the area.
    """

    def __init__(
        self,
        shape_list: Iterable[Polygon | MultiPolygon | _BaseGeometry],
        crs: CRS,
        split_shape: None | int | tuple[int, int] = None,
        split_size: None | int | tuple[int, int] = None,
        **kwargs: Any,
    ):
        """
        :param shape_list: A list of geometrical shapes describing the area of interest
        :param crs: Coordinate reference system of the shapes in `shape_list`
        :param split_shape: Parameter that describes the shape in which the area bounding box will be split.
            It can be a tuple of the form `(n, m)` which means the area bounding box will be split into `n` columns
            and `m` rows. It can also be a single integer `n` which is the same as `(n, n)`.
        :param split_size: Parameter that describes the size of patches (in the same Unit of Measure of the CRS)
            into which the area bounding box will be split. It can be a tuple of the form `(width, height)` which means
            the area bounding box will be split into patches of size (width, height). It can also be a single integer
            `size` which is the same as `(size, size)`.
        :param reduce_bbox_sizes: If `True` it will reduce the sizes of bounding boxes so that they will tightly fit
            the given area geometry from `shape_list`.
        """
        if (split_shape is not None) and (split_size is None):
            self.split_params = ("shape", _parse_to_pair(split_shape, allowed_types=(int,), param_name="split_shape"))
        elif (split_shape is None) and (split_size is not None):
            self.split_params = ("size", _parse_to_pair(split_size, allowed_types=(int,), param_name="split_size"))
        else:
            raise ValueError("Exactly one of 'split_shape' or 'split_size' needs to be specified.")
        super().__init__(shape_list, crs, **kwargs)

    def _make_split(self) -> tuple[list[BBox], list[dict[str, object]]]:
        pass


class OsmSplitter(AreaSplitter):
    """A tool that splits the given area into smaller parts. For the splitting it uses Open Street Map (OSM) grid on
    the specified zoom level. It calculates bounding boxes of all OSM tiles that intersect the area. If specified by
    user it can also reduce the sizes of the remaining bounding boxes to best fit the area.
    """

    def __init__(
        self,
        shape_list: Iterable[Polygon | MultiPolygon | _BaseGeometry],
        crs: CRS,
        zoom_level: int,
        **kwargs: Any,
    ):
        """
        :param shape_list: A list of geometrical shapes describing the area of interest
        :param crs: Coordinate reference system of the shapes in `shape_list`
        :param zoom_level: A zoom level defined by OSM. Level 0 is entire world, level 1 splits the world into
            4 parts, etc.
        :param reduce_bbox_sizes: If `True` it will reduce the sizes of bounding boxes so that they will tightly fit
            the given area geometry from `shape_list`.
        """
        self._POP_WEB_MAX = transform_point((180, 0), CRS.WGS84, CRS.POP_WEB)[0]  # pylint: disable=invalid-name

        self.zoom_level = zoom_level
        super().__init__(shape_list, crs, **kwargs)

    def _make_split(self) -> tuple[list[BBox], list[dict[str, object]]]:
        pass

    def _check_area_bbox(self) -> None:
        """The method checks if the area bounding box is completely inside the OSM grid. That means that its latitudes
        must be contained in the interval (-85.0511, 85.0511)

        :raises: ValueError
        """
        pass

    def get_world_bbox(self) -> BBox:
        """Creates a bounding box of the entire world in EPSG: 3857

        :return: Bounding box of entire world
        """
        pass

    def _recursive_split(
        self,
        bbox: BBox,
        zoom_level: int,
        column: int,
        row: int,
    ) -> tuple[list[BBox], list[dict[str, object]]]:
        """Method that recursively creates bounding boxes of OSM grid that intersect the area.

        :param bbox: Bounding box
        :param zoom_level: OSM zoom level
        :param column: Column in the OSM grid
        :param row: Row in the OSM grid
        """
        pass


class TileSplitter(AreaSplitter):
    """A splitter that uses Sentinel Hub Catalog API to obtain geometries of the original tiling grid of a given
    data collection. Additionally, it can further split these geometries into smaller parts.
    """

    _CATALOG_FILTER: ClassVar[dict[str, list[str]]] = {
        "include": ["id", "geometry", "properties.datetime", "properties.proj:bbox", "properties.proj:epsg"],
        "exclude": [],
    }

    def __init__(
        self,
        shape_list: Iterable[Polygon | MultiPolygon | _BaseGeometry],
        crs: CRS,
        time_interval: tuple[str, str],
        data_collection: DataCollection,
        tile_split_shape: int | tuple[int, int] = 1,
        config: SHConfig | None = None,
        **kwargs: Any,
    ):
        """
        :param shape_list: A list of geometrical shapes describing the area of interest
        :param crs: Coordinate reference system of the shapes in `shape_list`
        :param time_interval: Interval with start and end date of the form YYYY-MM-DDThh:mm:ss or YYYY-MM-DD
        :param data_collection: A satellite data collection
        :param tile_split_shape: Parameter that describes the shape in which the satellite tile bounding boxes will be
            split. It can be a tuple of the form `(n, m)` which means the tile bounding boxes will be
            split into `n` columns and `m` rows. It can also be a single integer `n` which is the same
            as `(n, n)`.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        :param kwargs: Parameters that are propagated to the base `AreaSplitter` class
        """
        self.time_interval = time_interval
        self.tile_split_shape = tile_split_shape
        self.data_collection = data_collection

        sh_config = config or SHConfig()
        if data_collection.service_url:
            sh_config = sh_config.copy()
            sh_config.sh_base_url = data_collection.service_url
        self.catalog = SentinelHubCatalog(config=sh_config)
        super().__init__(shape_list, crs, **kwargs)

    def _make_split(self) -> tuple[list[BBox], list[dict[str, object]]]:
        pass


class CustomGridSplitter(AreaSplitter):
    """Splitting class which can split according to given custom collection of bounding boxes"""

    def __init__(
        self,
        shape_list: Iterable[Polygon | MultiPolygon | _BaseGeometry],
        crs: CRS,
        bbox_grid: Iterable[BBox],
        bbox_split_shape: int | tuple[int, int] = 1,
        **kwargs: Any,
    ):
        """
        :param shape_list: A list of geometrical shapes describing the area of interest
        :param crs: Coordinate reference system of the shapes in `shape_list`
        :param bbox_grid: A collection of bounding boxes defining a grid of splitting. All of them have to be in the
            same CRS.
        :param bbox_split_shape: Parameter that describes the shape in which each of the bounding boxes in the given
            grid will be split. It can be a tuple of the form `(n, m)` which means the tile bounding boxes will be
            split into `n` columns and `m` rows. It can also be a single integer `n` which is the same as `(n, n)`.
        :param reduce_bbox_sizes: If `True` it will reduce the sizes of bounding boxes so that they will tightly fit
            the given geometry in `shape_list`.
        """
        self.bbox_grid = list(bbox_grid)
        self.bbox_split_shape = bbox_split_shape
        super().__init__(shape_list, crs, **kwargs)

    def _make_split(self) -> tuple[list[BBox], list[dict[str, object]]]:
        pass


class BaseUtmSplitter(AreaSplitter, metaclass=ABCMeta):
    """Base splitter that returns bboxes of fixed size aligned to UTM zones or UTM grid tiles as defined by the MGRS

    The generated bounding box grid will have coordinates in form of
    `(N * bbox_size_x + offset_x, M * bbox_size_y + offset_y)`
    """

    def __init__(
        self,
        shape_list: Iterable[Polygon | MultiPolygon | _BaseGeometry],
        crs: CRS,
        bbox_size: float | tuple[float, float],
        offset: tuple[float, float] | None = None,
    ):
        """
        :param shape_list: A list of geometrical shapes describing the area of interest
        :param crs: Coordinate reference system of the shapes in `shape_list`
        :param bbox_size: A size of generated bounding boxes in horizontal and vertical directions in meters. If a
            single value is given that will be interpreted as (value, value).
        :param offset: Bounding box offset in horizontal and vertical directions in meters.
        """
        self.bbox_size = _parse_to_pair(bbox_size, allowed_types=(int, float), param_name="bbox_size")

        self.offset = _parse_to_pair(offset or 0.0, allowed_types=(int, float), param_name="offset")

        self.utm_grid = self._get_utm_polygons()
        super().__init__(shape_list, crs)

    @abstractmethod
    def _get_utm_polygons(self) -> list[tuple[BaseGeometry, dict[str, Any]]]:
        """Find UTM grid zones overlapping with input area shape."""
        pass

    @staticmethod
    def _get_utm_from_props(utm_dict: dict[str, Any]) -> CRS:
        """Return the UTM CRS corresponding to the UTM described by the properties dictionary

        :param utm_dict: Dictionary reporting name of the UTM zone and MGRS grid
        :return: UTM coordinate reference system
        """
        pass

    def _align_bbox_to_size(self, bbox: BBox) -> BBox:
        """Align input bbox coordinates to be multiples of the bbox size

        :param bbox: Bounding box in UTM coordinates
        :return: BBox objects with coordinates multiples of the bbox size
        """
        pass

    def _make_split(self) -> tuple[list[BBox], list[dict[str, object]]]:
        """Split each UTM grid into equally sized bboxes in correct UTM zone"""
        pass

    def get_bbox_list(self, buffer: None | float | tuple[float, float] = None) -> list[BBox]:  # type: ignore[override]
        """Get list of bounding boxes.

        The CRS is fixed to the computed UTM CRS. This BBox splitter does not support reducing size of output
        bounding boxes

        :param buffer: A percentage of each BBox size increase. This will cause neighbouring bounding boxes to overlap.
        :return: List of bounding boxes
        """
        pass


class UtmGridSplitter(BaseUtmSplitter):
    """Splitter that returns bounding boxes of fixed size aligned to the UTM MGRS grid"""

    def _get_utm_polygons(self) -> list[tuple[BaseGeometry, dict[str, Any]]]:
        """Find UTM grid zones overlapping with input area shape

        :return: List of geometries and properties of UTM grid zones overlapping with input area shape
        """
        pass


class UtmZoneSplitter(BaseUtmSplitter):
    """Splitter that returns bounding boxes of fixed size aligned to the equator and the UTM zones."""

    LNG_MIN, LNG_MAX, LNG_UTM = -180, 180, 6
    LAT_MIN, LAT_MAX, LAT_EQ = -80, 84, 0

    def _get_utm_polygons(self) -> list[tuple[BaseGeometry, dict[str, Any]]]:
        """Find UTM zones overlapping with input area shape

        The returned geometry corresponds to a triangle ranging from the equator to the North/South Pole

        :return: List of geometries and properties of UTM zones overlapping with input area shape
        """
        pass


def _parse_to_pair(parameter: T | tuple[T, T], allowed_types: tuple[type, ...], param_name: str = "") -> tuple[T, T]:
    """Parses the parameters defining the splitting of the BBox."""
    pass
