"""Module implementing geometry classes."""

from __future__ import annotations

import contextlib
import warnings
from abc import ABCMeta, abstractmethod
from math import ceil
from typing import Callable, Dict, Iterator, Tuple, TypeVar, Union

import shapely.geometry
import shapely.geometry.base
import shapely.ops
import shapely.wkt
from shapely.errors import GeometryTypeError
from shapely.geometry import MultiPolygon, Polygon
from typing_extensions import TypeAlias

from .constants import CRS
from .exceptions import SHDeprecationWarning
from .geo_utils import transform_point

Self = TypeVar("Self", bound="_BaseGeometry")
BBoxInputType: TypeAlias = Union[
    Tuple[float, float, float, float], Tuple[Tuple[float, float], Tuple[float, float]], Dict[str, float]
]


class _BaseGeometry(metaclass=ABCMeta):
    """Base geometry class"""

    def __init__(self, crs: CRS):
        """
        :param crs: Coordinate reference system of the geometry
        """
        self._crs = CRS(crs)

    @property
    def crs(self) -> CRS:
        """Returns the coordinate reference system (CRS)

        :return: Coordinate reference system Enum
        """
        pass

    @property
    @abstractmethod
    def geometry(self) -> Polygon | MultiPolygon:
        """An abstract property - every subclass must implement geometry property"""

    @property
    def geojson(self) -> dict:
        """Returns representation in a GeoJSON format. Use `json.dump` for writing it to file.

        :return: A dictionary in GeoJSON format
        """
        pass

    def get_geojson(self, with_crs: bool = True) -> dict:
        """Returns representation in a GeoJSON format. Use `json.dump` for writing it to file.

        :param with_crs: A flag indicating if GeoJSON dictionary should contain CRS part
        :return: A dictionary in GeoJSON format
        """
        pass

    def _crs_to_geojson(self) -> dict:
        """Helper method which generates part of GeoJSON format related to CRS"""
        pass

    @property
    def wkt(self) -> str:
        """Transforms geometry object into `Well-known text` format

        :return: string in WKT format
        """
        pass

    @abstractmethod
    def transform(self: Self, crs: CRS, always_xy: bool = True) -> Self:
        """Transforms geometry from current CRS to target CRS."""
        pass

    @abstractmethod
    def apply(self: Self, operation: Callable[[float, float], tuple[float, float]]) -> Self:
        """Applies a function to each vertex of a geometry object."""
        pass


class BBox(_BaseGeometry):
    """Class representing a bounding box in a given CRS.

    Throughout the sentinelhub package this class serves as the canonical representation of a bounding box. It can be
    initialized from multiple representations:

        1) `((min_x, min_y), (max_x, max_y))`
        2) `(min_x, min_y, max_x, max_y)`
        3) `{"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}`

    In the above
    Note that BBox coordinate system depends on `crs` parameter:

    - In case of `constants.CRS.WGS84` axis x represents longitude and axis y represents latitude.
    - In case of `constants.CRS.POP_WEB` axis x represents easting and axis y represents northing.
    - In case of `constants.CRS.UTM_*` axis x represents easting and axis y represents northing.
    """

    def __init__(self, bbox: BBoxInputType, crs: CRS):
        """
        :param bbox: A bbox in any valid representation
        :param crs: Coordinate reference system of the bounding box
        """
        x_fst, y_fst, x_snd, y_snd = self._to_tuple(bbox)
        self.min_x, self.max_x = min(x_fst, x_snd), max(x_fst, x_snd)
        self.min_y, self.max_y = min(y_fst, y_snd), max(y_fst, y_snd)

        super().__init__(crs)

    @classmethod
    def _to_tuple(cls, bbox: BBoxInputType) -> tuple[float, float, float, float]:
        """Converts the input bbox representation (see the constructor docstring for a list of valid representations)
        into a flat tuple. Also supports `list` objects in places where `tuple` is expected.

        :param bbox: A bbox in one of the forms listed in the class description.
        :return: A flat tuple `(min_x, min_y, max_x, max_y)`
        :raises: TypeError
        """
        pass

    @staticmethod
    def _tuple_from_list_or_tuple(
        bbox: tuple[float, float, float, float] | tuple[tuple[float, float], tuple[float, float]],
    ) -> tuple[float, float, float, float]:
        """Converts a list or tuple representation of a bbox into a flat tuple representation.

        :param bbox: a list or tuple with 4 coordinates that is either flat or nested
        :return: tuple (min_x, min_y, max_x, max_y)
        :raises: TypeError
        """
        pass

    @staticmethod
    def _tuple_from_str(bbox: str) -> tuple[float, float, float, float]:
        """Parses a string of numbers separated by any combination of commas and spaces

        :param bbox: e.g. str of the form `min_x ,min_y  max_x, max_y`
        :return: tuple (min_x,min_y,max_x,max_y)
        """
        pass

    @staticmethod
    def _tuple_from_dict(bbox: dict) -> tuple[float, float, float, float]:
        """Converts a dictionary representation of a bbox into a flat tuple representation

        :param bbox: a dict with keys "min_x, "min_y", "max_x", and "max_y"
        :return: tuple (min_x,min_y,max_x,max_y)
        :raises: KeyError
        """
        pass

    @staticmethod
    def _tuple_from_bbox(bbox: BBox) -> tuple[float, float, float, float]:
        """Converts a BBox instance into a tuple

        :param bbox: An instance of the BBox type
        :return: tuple (min_x, min_y, max_x, max_y)
        """
        pass

    def __iter__(self) -> Iterator[float]:
        """This method enables iteration over coordinates of bounding box"""
        return iter(self.lower_left + self.upper_right)

    def __repr__(self) -> str:
        """Class representation"""
        return f"{self.__class__.__name__}(({self.lower_left}, {self.upper_right}), crs={self.crs!r})"

    def __str__(self, reverse: bool = False) -> str:
        """Transforms bounding box into a string of coordinates

        :param reverse: `True` if x and y coordinates should be switched and `False` otherwise
        :return: String of coordinates
        """
        warnings.warn(
            "The string representation of `BBox` will change to match its `repr` representation.",
            category=SHDeprecationWarning,
            stacklevel=2,
        )
        if reverse:
            return f"{self.min_y},{self.min_x},{self.max_y},{self.max_x}"
        return f"{self.min_x},{self.min_y},{self.max_x},{self.max_y}"

    def __eq__(self, other: object) -> bool:
        """Method for comparing two bounding boxes

        :param other: Another bounding box object
        :return: `True` if bounding boxes have the same coordinates and the same CRS and `False otherwise
        """
        if isinstance(other, BBox):
            return list(self) == list(other) and self.crs is other.crs
        return False

    @property
    def lower_left(self) -> tuple[float, float]:
        """Returns the lower left vertex of the bounding box

        :return: min_x, min_y
        """
        pass

    @property
    def upper_right(self) -> tuple[float, float]:
        """Returns the upper right vertex of the bounding box

        :return: max_x, max_y
        """
        pass

    @property
    def middle(self) -> tuple[float, float]:
        """Returns the middle point of the bounding box

        :return: middle point
        """
        pass

    def reverse(self) -> BBox:
        """Returns a new BBox object where x and y coordinates are switched

        :return: New BBox object with switched coordinates
        """
        pass

    def transform(self, crs: CRS, always_xy: bool = True) -> BBox:
        """Transforms BBox from current CRS to target CRS

        This transformation will take lower left and upper right corners of the bounding box, transform these 2 points
        and define a new bounding box with them. The resulting bounding box might not completely cover the original
        bounding box but at least the transformation is reversible.

        :param crs: target CRS
        :param always_xy: Parameter that is passed to `pyproj.Transformer` object and defines axis order for
            transformation. The default value `True` is in most cases the correct one.
        :return: Bounding box in target CRS
        """
        pass

    def transform_bounds(self, crs: CRS, always_xy: bool = True) -> BBox:
        """Alternative way to transform BBox from current CRS to target CRS.

        This transformation will transform the bounding box geometry to another CRS as a geometric object, and then
        define a new bounding box from boundaries of that geometry. The resulting bounding box might be larger than
        original bounding box, but it will always completely cover it.

        :param crs: target CRS
        :param always_xy: Parameter that is passed to `pyproj.Transformer` object and defines axis order for
            transformation. The default value `True` is in most cases the correct one.
        :return: Bounding box in target CRS
        """
        pass

    def apply(self, operation: Callable[[float, float], tuple[float, float]]) -> BBox:
        """Applies a function to lower left and upper right pairs of coordinates of the bounding box to create a new
        bounding box."""
        pass

    def buffer(self, buffer: float | tuple[float, float], *, relative: bool = True) -> BBox:
        """Provides a new bounding box with a size that is changed either by a relative or an absolute buffer.

        :param buffer: The buffer can be provided either as a single number or a tuple of 2 numbers, one for buffer in
            horizontal direction and one for buffer in vertical direction. The buffer can also be negative as long as
            this doesn't reduce the bounding box into nothing.
        :param relative: If `True` the given buffer values will be interpreted as a percentage of distance between
            bounding box center point and its side edge (not to distance between opposite sides!). If `False` the given
            buffer will be interpreted as an absolute buffer measured in bounding box coordinate units.
        :return: A new bounding box of buffered size.
        """
        pass

    def get_polygon(self, reverse: bool = False) -> tuple[tuple[float, float], ...]:
        """Returns a tuple of coordinates of 5 points describing a polygon. Points are listed in clockwise order, first
        point is the same as the last.

        :param reverse: `True` if x and y coordinates should be switched and `False` otherwise
        :return: `((x_1, y_1), ... , (x_5, y_5))`
        """
        pass

    @property
    def geometry(self) -> shapely.geometry.Polygon:
        """Returns polygon geometry in shapely format

        :return: A polygon in shapely format
        """
        pass

    def get_partition(
        self,
        num_x: int | None = None,
        num_y: int | None = None,
        size_x: float | None = None,
        size_y: float | None = None,
    ) -> list[list[BBox]]:
        """Partitions bounding box into smaller bounding boxes of the same size.

        If `num_x` and `num_y` are specified, the total number of BBoxes is know but not the size. If `size_x` and
        `size_y` are provided, the BBox size is fixed but the number of BBoxes is not known in advance. In the latter
        case, the generated bounding boxes might cover an area larger than the parent BBox.

        :param num_x: Number of parts BBox will be horizontally divided into.
        :param num_y: Number of parts BBox will be vertically divided into.
        :param size_x: Physical dimension of BBox along easting coordinate
        :param size_y: Physical dimension of BBox along northing coordinate
        :return: Two-dimensional list of smaller bounding boxes. Their location is
        """
        pass

    def get_transform_vector(self, resx: float, resy: float) -> tuple[float, float, float, float, float, float]:
        """Given resolution it returns a transformation vector

        :param resx: Resolution in x direction
        :param resy: Resolution in y direction
        :return: A tuple with 6 numbers representing transformation vector
        """
        pass

    @staticmethod
    def _parse_resolution(res: str | int | float) -> float:
        """Helper method for parsing given resolution. It will also try to parse a string into float

        :return: A float value of resolution
        """
        pass


class Geometry(_BaseGeometry):
    """A class that combines shapely geometry with coordinate reference system. It currently supports polygons and
    multipolygons.

    It can be initialized with any of the following geometry representations:
    - `shapely.geometry.Polygon` or `shapely.geometry.MultiPolygon`
    - A GeoJSON dictionary with (multi)polygon coordinates
    - A WKT string with (multi)polygon coordinates
    """

    def __init__(self, geometry: Polygon | MultiPolygon | dict | str, crs: CRS):
        """
        :param geometry: A polygon or multipolygon in any valid representation
        :param crs: Coordinate reference system of the geometry
        """
        self._geometry = self._parse_geometry(geometry)

        super().__init__(crs)

    def __repr__(self) -> str:
        """Method for class representation"""
        return f"{self.__class__.__name__}({self.wkt}, crs={self.crs!r})"

    def __eq__(self, other: object) -> bool:
        """Method for comparing two Geometry classes

        :param other: Another Geometry object
        :return: `True` if geometry objects have the same geometry and CRS and `False` otherwise
        """
        if isinstance(other, Geometry):
            return self.geometry == other.geometry and self.crs is other.crs
        return False

    def reverse(self) -> Geometry:
        """Returns a new Geometry object where x and y coordinates are switched

        :return: New Geometry object with switched coordinates
        """
        pass

    def transform(self, crs: CRS, always_xy: bool = True) -> Geometry:
        """Transforms Geometry from current CRS to target CRS

        :param crs: target CRS
        :param always_xy: Parameter that is passed to `pyproj.Transformer` object and defines axis order for
            transformation. The default value `True` is in most cases the correct one.
        :return: Geometry in target CRS
        """
        pass

    def apply(self, operation: Callable[[float, float], tuple[float, float]]) -> Geometry:
        """Applies a function to each pair of vertex coordinates of the geometry to create a new geometry."""
        pass

    @classmethod
    def from_geojson(cls, geojson: dict, crs: CRS | None = None) -> Geometry:
        """Create Geometry object from geojson. It will parse crs from geojson (if info is available),
        otherwise it will be set to crs (WGS84 if parameter is empty)

        :param geojson: geojson geometry (single feature)
        :param crs: crs to be used if not available in geojson, CRS.WGS84 if not provided
        :return: Geometry object
        """
        pass

    @property
    def geometry(self) -> Polygon | MultiPolygon:
        """Returns shapely object representing geometry in this class

        :return: A polygon or a multipolygon in shapely format
        """
        pass

    @property
    def bbox(self) -> BBox:
        """Returns BBox object representing bounding box around the geometry

        :return: A bounding box, with same CRS
        """
        pass

    @staticmethod
    def _parse_geometry(geometry: Polygon | MultiPolygon | dict | str) -> Polygon | MultiPolygon:
        """Parses given geometry into shapely object

        :param geometry: A representation of the geometry
        :return: Shapely polygon or multipolygon
        :raises TypeError
        """
        pass
