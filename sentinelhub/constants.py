"""
Module defining constants and enumerate types used in the package
"""

from __future__ import annotations

import functools
import mimetypes
import re
import warnings
from enum import Enum, EnumMeta
from typing import Callable, ClassVar

import numpy as np
import pyproj
import utm
from aenum import extend_enum

from ._version import __version__
from .exceptions import SHUserWarning


class ServiceUrl:
    """Most commonly used Sentinel Hub service URLs"""

    MAIN = "https://services.sentinel-hub.com"
    USWEST = "https://services-uswest2.sentinel-hub.com"
    CREODIAS = "https://creodias.sentinel-hub.com"
    MUNDI = "https://shservices.mundiwebservices.com"
    CODE_DE = "https://code-de.sentinel-hub.com"


class ServiceType(Enum):
    """Enum constant class for type of service

    Supported types are WMS, WCS, WFS, AWS, IMAGE
    """

    WMS = "wms"
    WCS = "wcs"
    WFS = "wfs"
    AWS = "aws"
    IMAGE = "image"
    PROCESSING_API = "processing"


class ResamplingType(Enum):
    """Enum constant class for type of resampling."""

    NEAREST = "NEAREST"
    BILINEAR = "BILINEAR"
    BICUBIC = "BICUBIC"

    @classmethod
    def _missing_(cls, value: object) -> ResamplingType:
        # This triggers if value is not found, before raising an error (see Enum docs). Makes class case-insensitive.
        pass


class MosaickingOrder(Enum):
    """Enum constant class for type of mosaicking order."""

    MOST_RECENT = "mostRecent"
    LEAST_RECENT = "leastRecent"
    LEAST_CC = "leastCC"


class CRSMeta(EnumMeta):
    """Metaclass used for building CRS Enum class"""

    _UNSUPPORTED_CRS = pyproj.CRS(4326)

    def __new__(mcs, cls, bases, classdict):  # type: ignore[no-untyped-def] # noqa: N804
        """This is executed at the beginning of runtime when CRS class is created"""
        for direction, direction_value in [("N", "6"), ("S", "7")]:
            for zone in range(1, 61):
                classdict[f"UTM_{zone}{direction}"] = f"32{direction_value}{zone:02}"

        return super().__new__(mcs, cls, bases, classdict)

    def __call__(cls, crs_value, *args, **kwargs):  # type: ignore[no-untyped-def]
        """This is executed whenever CRS('something') is called"""
        # pylint: disable=signature-differs
        crs_value = cls._parse_crs(crs_value)

        if isinstance(crs_value, str) and not cls.has_value(crs_value) and crs_value.isdigit() and len(crs_value) >= 4:
            crs_name = f"EPSG_{crs_value}"
            extend_enum(cls, crs_name, crs_value)

        return super().__call__(crs_value, *args, **kwargs)

    @staticmethod
    def _parse_crs(value: object) -> object:  # noqa: C901
        """Method for parsing different inputs representing the same CRS enum. Examples:

        - 4326
        - 'EPSG:3857'
        - {'init': 32633}
        - geojson['crs']['properties']['name'] string (urn:ogc:def:crs:...)
        - pyproj.CRS(32743)
        """
        pass


class CRS(Enum, metaclass=CRSMeta):
    """Coordinate Reference System enumerate class

    Available CRS constants are WGS84, POP_WEB (i.e. Popular Web Mercator) and constants in form UTM_<zone><direction>,
    where zone is an integer from [1, 60] and direction is either N or S (i.e. northern or southern hemisphere)
    """

    WGS84 = "4326"
    POP_WEB = "3857"
    #: UTM enum members are defined in CRSMeta.__new__

    def __str__(self) -> str:
        """Method for casting CRS enum into string"""
        return self.ogc_string()

    def __repr__(self) -> str:
        """Method for retrieving CRS enum representation"""
        return f"CRS('{self.value}')"

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Tests whether CRS contains a constant defined with string `value`.

        :param value: The string representation of the enum constant.
        :return: `True` if there exists a constant with string value `value`, `False` otherwise
        """
        pass

    @property
    def epsg(self) -> int:
        """EPSG code property

        :return: EPSG code of given CRS
        """
        pass

    def ogc_string(self) -> str:
        """Returns a string of the form authority:id representing the CRS.

        :param self: An enum constant representing a coordinate reference system.
        :return: A string representation of the CRS.
        """
        pass

    @property
    def opengis_string(self) -> str:
        """Returns a URL to OGC webpage where the CRS is defined

        :return: A URL with CRS definition
        """
        pass

    def is_utm(self) -> bool:
        """Checks if crs is one of the 64 possible UTM coordinate reference systems.

        :param self: An enum constant representing a coordinate reference system.
        :return: `True` if crs is UTM and `False` otherwise
        """
        pass

    @functools.lru_cache(maxsize=128)
    def projection(self) -> pyproj.Proj:
        """Returns a projection in form of pyproj class.

        For better time performance this method will cache `128` most recent results. Cache can be released with
        `CRS.projection.cache_clear()`.

        :return: pyproj projection class
        """
        pass

    @functools.lru_cache(maxsize=128)
    def pyproj_crs(self) -> pyproj.CRS:
        """Returns a pyproj CRS class.

        For better time performance this method will cache `128` most recent results. Cache can be released with
        `CRS.pyproj_crs.cache_clear()`.

        :return: pyproj CRS class
        """
        pass

    @functools.lru_cache(maxsize=512)
    def get_transform_function(self, other: CRS, always_xy: bool = True) -> Callable[..., tuple]:
        """Returns a function for transforming geometrical objects from one CRS to another. The function will support
        transformations between any objects that pyproj supports.

        For better time performance this method will cache results. Cache can be released with
        `CRS.get_transform_function.cache_clear()`.

        :param self: Initial CRS
        :param other: Target CRS
        :param always_xy: Parameter that is passed to `pyproj.Transformer` object and defines axis order for
            transformation. The default value `True` is in most cases the correct one.
        :return: A projection function obtained from pyproj package
        """
        pass

    @staticmethod
    def get_utm_from_wgs84(lng: float, lat: float) -> CRS:
        """Convert from WGS84 to UTM coordinate system

        :param lng: Longitude
        :param lat: Latitude
        :return: UTM coordinates
        """
        pass

    def _get_pyproj_projection_def(self) -> str:
        """Returns a pyproj crs definition

        For WGS 84 it ensures lng-lat order
        """
        pass


class MimeType(Enum):
    """Enum class to represent supported file formats

    Supported file formats are TIFF 8-bit, TIFF 16-bit, TIFF 32-bit float, PNG, JPEG, JPEG2000, JSON, CSV, ZIP, HDF5,
    XML, GML, RAW
    """

    TIFF = "tiff"
    PNG = "png"
    JPG = "jpg"
    JP2 = "jp2"
    JSON = "json"
    CSV = "csv"
    ZIP = "zip"
    HDF = "hdf"
    XML = "xml"
    GML = "gml"
    TXT = "txt"
    TAR = "tar"
    RAW = "raw"
    SAFE = "safe"
    PICKLE = "pkl"
    NPY = "npy"
    GPKG = "gpkg"
    GEOJSON = "geojson"
    GZIP = "gz"

    @property
    def extension(self) -> str:
        """Returns file extension of the MimeType object

        :returns: A file extension string
        """
        pass

    @staticmethod
    def from_string(mime_type_str: str) -> MimeType:
        """Parses mime type from a file extension string

        :param mime_type_str: A file extension string
        :return: A mime type enum
        """
        pass

    def is_image_format(self) -> bool:
        """Checks whether file format is an image format

        Example: ``MimeType.PNG.is_image_format()`` or ``MimeType.is_image_format(MimeType.PNG)``

        :param self: File format
        :return: `True` if file is in image format, `False` otherwise
        """
        pass

    def is_api_format(self) -> bool:
        """Checks if mime type is supported by Sentinel Hub API

        :return: True if API supports this format and False otherwise
        """
        pass

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Tests whether MimeType contains a constant defined with string ``value``

        :param value: The string representation of the enum constant
        :return: `True` if there exists a constant with string value ``value``, `False` otherwise
        """
        pass

    def get_string(self) -> str:
        """Get file format as string

        :return: String describing the file format
        """
        pass

    def matches_extension(self, path: str) -> bool:
        """Checks if mime type enum is used as the last file extension in given file path.

        :param path: Path that might have an extension at the end.
        :return: A boolean value indicating if the file path ends with the expected extension.
        """
        pass

    def get_expected_max_value(self) -> float | int:
        """Returns max value of image `MimeType` format and raises an error if it is not an image format

        :return: A maximum value of specified image format
        :raises: ValueError
        """
        pass


class RequestType(Enum):
    """Enum constant class for GET/POST request type."""

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    PATCH = "PATCH"


class SHConstants:
    """Common constants used in various requests."""

    LATEST = "latest"
    HEADERS: ClassVar[dict[str, str]] = {"User-Agent": f"sentinelhub-py/v{__version__}"}
