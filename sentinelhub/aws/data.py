"""
Module for defining how satellite data will be collected from AWS and where it will be saved.
"""

import datetime as dt
import os
import warnings
from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional, Tuple, Union
from typing_extensions import deprecated

from ..api.opensearch import get_tile_info, get_tile_info_id
from ..config import SHConfig
from ..constants import MimeType
from ..data_collections import DataCollection
from ..download import DownloadRequest
from ..exceptions import AwsDownloadFailedException, SHUserWarning, SHDeprecationWarning
from ..time_utils import parse_time
from .client import AwsDownloadClient
from .constants import AwsConstants, EsaSafeType

MAX_SUPPORTED_BASELINES = {
    DataCollection.SENTINEL2_L1C: "04.00",
    DataCollection.SENTINEL2_L2A: "04.00",
}

REQUESTER_PAYS_PARAMS = {"RequestPayer": "requester"}


class AwsData(metaclass=ABCMeta):
    """A base class for collecting satellite data from AWS."""

    def __init__(
        self,
        parent_folder: str = "",
        bands: Union[None, str, List[str]] = None,
        metafiles: Union[None, str, List[str]] = None,
        config: Optional[SHConfig] = None,
    ):
        """
        :param parent_folder: Folder where the fetched data will be saved.
        :param bands: List of Sentinel-2 bands for request. If parameter is set to `None` all bands will be used.
        :param metafiles: List of additional metafiles available on AWS
                          (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``).
                          If parameter is set to `None` the list will be set automatically.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.parent_folder = parent_folder
        self.bands = self._parse_bands(bands)
        self.metafiles = self._parse_metafiles(metafiles)
        self.config = config or SHConfig()

        self.download_list: List[DownloadRequest] = []
        self.folder_list: List[str] = []

        self.base_url = self.get_base_url()
        self.base_http_url = self.get_base_url(force_http=True)

        # These need to be set by the child classes
        self.baseline: str
        self.safe_type: EsaSafeType
        self.data_collection: DataCollection
        self.date: dt.date
        self.product_id: str

    @abstractmethod
    def get_requests(self) -> Tuple[List[DownloadRequest], List[str]]:
        """Abstract class for joining together download requests"""
        pass

    def _parse_bands(self, band_input: Union[None, str, List[str]]) -> List[str]:
        """
        Parses class input and verifies band names.

        :param band_input: input parameter `bands`
        :return: verified list of bands
        """
        pass

    def _parse_metafiles(self, metafile_input: Union[None, str, List[str]]) -> List[str]:
        """Parses class input and verifies metadata file names.

        :param metafile_input: class input parameter `metafiles`
        :return: verified list of metadata files
        """
        pass

    def get_base_url(self, force_http: bool = False) -> str:
        """Creates base URL path

        :param force_http: `True` if HTTP base URL should be used and `False` otherwise
        :return: base url string
        """
        pass

    def get_safe_type(self) -> EsaSafeType:
        """Determines the type of ESA product.

        In 2016 ESA changed structure and naming of data. Therefore, the class must
        distinguish between old product type and compact (new) product type.

        :return: type of ESA product
        :raises: ValueError
        """
        pass

    def get_baseline(self) -> str:
        """Determines the baseline number (i.e. version) of ESA .SAFE product

        :return: baseline number
        :raises: ValueError
        """
        pass

    def _read_baseline_from_info(self) -> str:
        """Tries to find and return baseline number from either tileInfo or productInfo file.

        :return: Baseline ID
        :raises: ValueError
        """
        pass

    @staticmethod
    def url_to_tile(url: str) -> Tuple[str, str, int]:
        """Extracts tile name, date and AWS index from tile url on AWS.

        :param url: class input parameter 'metafiles'
        :return: Name of tile, date and AWS index which uniquely identifies tile on AWS
        """
        pass

    def sort_download_list(self) -> None:
        """Method for sorting the list of download requests. Band images have priority before metadata files. If bands
        images or metadata files are specified with a list they will be sorted in the same order as in the list.
        Otherwise, they will be sorted alphabetically (band B8A will be between B08 and B09).
        """
        def aws_sort_function(download_request):
            pass

        pass

    def structure_recursion(self, struct: dict, folder: str) -> None:
        """From nested dictionaries representing .SAFE structure it recursively extracts all the files that need to be
        downloaded and stores them into class attribute `download_list`.

        :param struct: nested dictionaries representing a part of .SAFE structure
        :param folder: name of folder where this structure will be saved
        """
        pass

    def _url_to_props(self, url: str) -> Tuple[str, str]:
        """Converts url back to name of product/tile and name of the file

        :param url: URL location of the data
        :return: Names of product or tile and name of a file
        """
        pass

    @staticmethod
    def add_file_extension(filename: str, data_format: Optional[MimeType] = None, remove_path: bool = False) -> str:
        """Joins filename and corresponding file extension if it has one.

        :param filename: Name of the file without extension
        :param data_format: format of file, if `None` it will be set automatically
        :param remove_path: `True` if the path in filename string should be removed
        :return: Name of the file with extension
        """
        pass

    def has_reports(self) -> bool:
        """Products created with baseline 2.06 and greater (and some products with baseline 2.05) should have quality
        report files

        :return: `True` if the product has report xml files and `False` otherwise
        """
        pass

    def is_early_compact_l2a(self) -> bool:
        """Check if product is early version of compact L2A product

        :return: `True` if product is early version of compact L2A product and `False` otherwise
        """
        pass


@deprecated(
    "AWS functionality will remain in the codebase for now, but won't be actively maintained.",
    category=SHDeprecationWarning,
)
class AwsProduct(AwsData):
    """Class for collecting Sentinel-2 products data from AWS."""

    def __init__(self, product_id: str, tile_list: Union[None, str, List[str]] = None, **kwargs: Any):
        """
        :param product_id: ESA ID of the product
        :param tile_list: list of tile names
        :param parent_folder: location of the directory where the fetched data will be saved.
        :param bands: List of Sentinel-2 bands for request. If parameter is set to `None` all bands will be used.
        :param metafiles: List of additional metafiles available on AWS
                          (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``).
                          If parameter is set to `None` the list will be set automatically.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.product_id = product_id.split(".")[0]
        self.tile_list = self.parse_tile_list(tile_list)

        self.data_collection = self.get_data_collection()
        self.safe_type = self.get_safe_type()

        super().__init__(**kwargs)

        self.date = self.get_date()
        self.product_url = self.get_product_url()

        client = AwsDownloadClient(config=self.config, boto_params=REQUESTER_PAYS_PARAMS)
        self.product_info = client.get_json_dict(self.get_url(AwsConstants.PRODUCT_INFO))
        self.baseline = self.get_baseline()

    @staticmethod
    def parse_tile_list(tile_input: Union[None, str, List[str]]) -> Optional[List[str]]:
        """Parses class input and verifies band names.

        :param tile_input: class input parameter `tile_list`
        :return: parsed list of tiles
        """
        pass

    def get_requests(self) -> Tuple[List[DownloadRequest], List[str]]:
        """Creates product structure and returns list of files for download.

        :return: List of download requests and list of empty folders that need to be created
        """
        pass

    def get_data_collection(self) -> DataCollection:
        """The method determines data collection from product ID.

        :return: Data collection of the product
        :raises: ValueError
        """
        pass

    def get_date(self) -> dt.date:
        """Collects sensing date of the product.

        :return: Sensing date
        """
        pass

    def get_url(self, filename: str, data_format: Optional[MimeType] = None) -> str:
        """Creates url of file location on AWS.

        :param filename: name of file
        :param data_format: format of file, if `None` it will be set automatically
        :return: url of file location
        """
        pass

    def get_product_url(self, force_http: bool = False) -> str:
        """Creates base url of product location on AWS.

        :param force_http: `True` if HTTP base URL should be used and `False` otherwise
        :return: url of product location
        """
        pass

    def get_tile_url(self, tile_info: dict) -> str:
        """Collects tile url from `productInfo.json` file.

        :param tile_info: information about tile from `productInfo.json`
        :return: url of tile location
        """
        pass

    def get_filepath(self, filename: str) -> str:
        """Creates file path for the file.

        :param filename: name of the file
        :return: filename with path on disk
        """
        pass


@deprecated(
    "AWS functionality will remain in the codebase for now, but won't be actively maintained.",
    category=SHDeprecationWarning,
)
class AwsTile(AwsData):
    """Class for collecting Sentinel-2 tiles data from AWS."""

    def __init__(
        self,
        tile_name: str,
        time: str,
        aws_index: Optional[int] = None,
        data_collection: DataCollection = DataCollection.SENTINEL2_L1C,
        **kwargs: Any,
    ):
        """
        :param tile: Tile name (e.g. 'T10UEV')
        :param time: Tile sensing time in ISO8601 format
        :param aws_index: There exist Sentinel-2 tiles with the same tile and time parameter. Therefore, each tile
            on AWS also has an index which is visible in their url path. If `aws_index` is set to `None` the
            class will try to find the index automatically. If there will be multiple choices it will choose
            the lowest index and inform the user.
        :param data_collection: A collection of requested AWS data. Supported collections are Sentinel-2 L1C and
            Sentinel-2 L2A, default is Sentinel-2 L1C data.
        :param parent_folder: folder where the fetched data will be saved.
        :param bands: List of Sentinel-2 bands for request. If parameter is set to `None` all bands will be used.
        :param metafiles: List of additional metafiles available on AWS
                          (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``).
                          If parameter is set to `None` the list will be set automatically.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.tile_name = self.parse_tile_name(tile_name)

        self.timestamp: dt.date = parse_time(time, ignoretz=True)
        self.date = self.timestamp.date() if isinstance(self.timestamp, dt.datetime) else self.timestamp

        self.aws_index = aws_index
        self.data_collection = data_collection

        super().__init__(**kwargs)
        self.tile_url = None

        self.aws_index = self.get_aws_index()
        self.tile_url = self.get_tile_url()
        self.tile_info = self.get_tile_info()
        if not self.tile_is_valid():
            raise ValueError("Cannot find data on AWS for specified tile, time and aws_index")

        self.product_id = self.get_product_id()
        self.safe_type = self.get_safe_type()
        self.baseline = self.get_baseline()

    @staticmethod
    def parse_tile_name(name: str) -> str:
        """
        Parses and verifies tile name.

        :param name: class input parameter `tile_name`
        :return: parsed tile name
        """
        pass

    def get_requests(self) -> Tuple[List[DownloadRequest], List[str]]:
        """
        Creates tile structure and returns list of files for download.

        :return: List of download requests and list of empty folders that need to be created
        """
        pass

    def get_aws_index(self) -> int:
        """
        Returns tile index on AWS. If `tile_index` was not set during class initialization it will be determined
        according to existing tiles on AWS.

        :return: Index of tile on AWS
        """
        pass

    @staticmethod
    def _parse_aws_index(tile_info: dict) -> int:
        """Parses an AWS index from tile info

        :param tile_info: dictionary with information about tile
        :return: Index of tile on AWS
        """
        pass

    def tile_is_valid(self) -> bool:
        """Checks if tile has tile info and valid timestamp

        :return: `True` if tile is valid and `False` otherwise
        """
        pass

    def get_tile_info(self) -> dict:
        """
        Collects basic info about tile from tileInfo.json.

        :return: dictionary with tile information
        """
        pass

    def get_url(self, filename: str) -> str:
        """
        Creates url of file location on AWS.

        :param filename: name of file
        :return: url of file location
        """
        pass

    def get_tile_url(self, force_http: bool = False) -> str:
        """
        Creates base url of tile location on AWS.

        :param force_http: `True` if HTTP base URL should be used and `False` otherwise
        :return: url of tile location
        """
        pass

    def get_qi_url(self, metafile: str) -> str:
        """Returns url of tile metadata products

        :param metafile: Name of metadata product at AWS
        :return: url location of metadata product at AWS
        """
        pass

    def get_band_qi_url(self, qi_type: str, band: str = "B00", data_format: MimeType = MimeType.GML) -> str:
        """
        :param qi_type: type of quality indicator
        :param band: band name
        :return: location of gml file on AWS
        """
        pass

    def get_preview_url(self, data_type: str = "L1C") -> str:
        """Returns url location of full resolution L1C preview"""
        pass

    def get_filepath(self, filename: str) -> str:
        """
        Creates file path for the file.

        :param filename: name of the file
        :return: filename with path on disk
        """
        pass

    def get_product_id(self) -> str:
        """
        Obtains ESA ID of product which contains the tile.

        :return: ESA ID of the product
        """
        pass

    def _band_exists(self, band_name: str) -> bool:
        pass

    @staticmethod
    def tile_id_to_tile(tile_id: str) -> Tuple[str, str, int]:
        """
        :param tile_id: original tile identification string provided by ESA (e.g.
                        'S2A_OPER_MSI_L1C_TL_SGS__20160109T230542_A002870_T10UEV_N02.01')
        :return: tile name, sensing date and AWS index
        """
        pass
