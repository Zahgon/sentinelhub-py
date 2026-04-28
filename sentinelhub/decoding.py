"""
Module for data decoding
"""

from __future__ import annotations

import json
import struct
import tarfile
import warnings
from io import BytesIO
from json import JSONDecodeError
from typing import IO, Any
from xml.etree import ElementTree

import numpy as np
import tifffile as tiff
from PIL import Image
from requests import Response

from .constants import MimeType
from .exceptions import ImageDecodingError


def decode_data(response_content: bytes, data_type: MimeType) -> Any:
    """Interprets downloaded data and returns it.

    :param response_content: downloaded data (i.e. json, png, tiff, xml, zip, ... file)
    :param data_type: expected downloaded data type
    :return: downloaded data
    :raises: ValueError
    """
    pass


def decode_image(data: bytes, image_type: MimeType) -> np.ndarray:
    """Decodes the image provided in various formats, i.e. png, 16-bit float tiff, 32-bit float tiff, jp2
    and returns it as a numpy array

    :param data: image in its original format
    :param image_type: expected image format
    :return: image as numpy array
    :raises: ImageDecodingError
    """
    pass


def decode_image_with_pillow(stream: IO | str) -> np.ndarray:
    """Decodes an image using `Pillow` package and handles potential warnings.

    :param stream: A binary stream format or a filename.
    :return: A numpy array representing an image of shape (height, width) or (height, width, channels).
    """
    pass


def decode_jp2_image(stream: IO) -> np.ndarray:
    """Tries to decode a JPEG2000 image using the `Pillow` package.

    :param stream: A binary stream format.
    :return: A numpy array representing an image of shape (height, width) or (height, width, channels).
    """
    pass


def decode_tar(data: bytes | BytesIO) -> dict[str, object]:
    """A decoder to convert response bytes into a dictionary of {filename: value}

    :param data: Data to decode
    :return: A dictionary of decoded files from a tar file
    """
    pass


def decode_sentinelhub_err_msg(response: Response) -> str:
    """Decodes error message from Sentinel Hub service

    :param response: Sentinel Hub service response
    :return: An error message
    """
    pass


def get_jp2_bit_depth(stream: IO) -> int:
    """Reads a bit encoding depth of jpeg2000 file in binary stream format

    :param stream: binary stream format
    :return: bit depth
    """
    pass


def fix_jp2_image(image: np.ndarray, bit_depth: int) -> np.ndarray:
    """Because Pillow library incorrectly reads JPEG 2000 images with 15-bit encoding this function corrects the
    values in image.

    :param image: image read by opencv library
    :param bit_depth: A bit depth of jp2 image encoding
    :return: corrected image
    """
    pass


def get_data_format(filename: str) -> MimeType:
    """Util function to guess format from filename extension

    :param filename: name of file
    :return: file extension
    """
    pass
