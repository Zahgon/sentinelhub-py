"""
Utility functions to read/write image data from/to file
"""

from __future__ import annotations

import csv
import json
import logging
import os
from typing import IO, Any, Callable, Literal
from xml.etree import ElementTree

import numpy as np
import tifffile as tiff
from PIL import Image

from .constants import MimeType
from .decoding import decode_image_with_pillow, decode_jp2_image, decode_tar, get_data_format

LOGGER = logging.getLogger(__name__)

CSV_DELIMITER = ";"


def read_data(filename: str, data_format: MimeType | None = None) -> Any:
    """Read image data from file

    This function reads input data from file. The format of the file
    can be specified in ``data_format``. If not specified, the format is
    guessed from the extension of the filename.

    :param filename: filename to read data from
    :param data_format: format of filename. Default is `None`
    :return: data read from filename
    :raises: exception if filename does not exist
    """
    pass


def _get_reader(data_format: MimeType) -> Callable[[str], Any]:
    """Provides a function for reading data in a given data format"""
    pass


def _open_file_and_read(reader: Callable[[IO], Any], mode: Literal["r", "rb"]) -> Callable[[str], Any]:
    def new_reader(path):
        pass

    pass


def _read_csv(filename: str, delimiter: str = CSV_DELIMITER) -> list:
    """Read data from CSV file

    :param filename: name of CSV file to be read
    :param delimiter: type of CSV delimiter. Default is ``;``
    :return: data stored in CSV file as list
    """
    pass


def write_data(  # noqa: C901
    filename: str, data: Any, data_format: MimeType | None = None, compress: bool = False, add: bool = False
) -> None:
    """Write image data to file

    Function to write image data to specified file. If file format is not provided
    explicitly, it is guessed from the filename extension. If format is TIFF, geo
    information and compression can be optionally added.

    :param filename: name of file to write data to
    :param data: image data to write to file
    :param data_format: format of output file. Default is `None`
    :param compress: Compress data. Default is `False`
    :param add: Append to existing file. Only supported for TXT. Default is `False`
    :raises: exception if numpy format is not supported or file cannot be written
    """
    pass


def _create_parent_folder(filename: str) -> None:
    pass
