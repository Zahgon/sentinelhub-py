"""
Module for creating .SAFE structure with data collected from AWS
"""

import warnings
from typing import Any, List, Optional, Tuple

from ..constants import MimeType
from ..data_collections import DataCollection
from ..download.models import DownloadRequest
from ..exceptions import SHRuntimeWarning
from .client import AwsDownloadClient
from .constants import AwsConstants, EsaSafeType
from .data import REQUESTER_PAYS_PARAMS, AwsProduct, AwsTile


class SafeProduct(AwsProduct):
    """Class implementing transformation of Sentinel-2 satellite products from AWS into .SAFE structure"""

    def get_requests(self) -> Tuple[List[DownloadRequest], List[str]]:
        """Creates product structure and returns list of files for download

        :return: list of download requests
        """
        pass

    def get_safe_struct(self) -> dict:
        """Describes a structure inside tile folder of ESA product .SAFE structure

        :return: nested dictionaries representing .SAFE structure
        """
        pass

    def _get_datastrip_substruct(self) -> dict:
        """Builds a datastrip subfolder structure of .SAFE format."""
        pass

    def _get_granule_substruct(self) -> dict:
        """Builds a granule subfolder structure of .SAFE format."""
        pass

    def get_main_folder(self) -> str:
        """
        :return: name of main folder
        """
        pass

    def get_datastrip_list(self) -> List[Tuple[str, str]]:
        """
        :return: list of datastrips folder names and urls from `productInfo.json` file
        """
        pass

    def get_datastrip_name(self, datastrip: str) -> str:
        """
        :param datastrip: name of datastrip
        :return: name of datastrip folder
        """
        pass

    def get_datastrip_metadata_name(self, datastrip_folder: str) -> str:
        """
        :param datastrip_folder: name of datastrip folder
        :return: name of datastrip metadata file
        """
        pass

    def get_product_metadata_name(self) -> str:
        """
        :return: name of product metadata file
        """
        pass

    def get_report_name(self) -> str:
        """
        :return: name of the report file of L2A products
        """
        pass

    def get_report_time(self) -> str:
        """Returns time when the L2A processing started and reports was created.
        :return: String in a form YYYYMMDDTHHMMSS
        """
        pass


class SafeTile(AwsTile):
    """Class implementing transformation of Sentinel-2 satellite tiles from AWS into .SAFE structure"""

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialization parameters are inherited from parent class"""
        super().__init__(*args, **kwargs)

        self.tile_id = self.get_tile_id()

    def get_requests(self) -> Tuple[List[DownloadRequest], List[str]]:
        """Creates tile structure and returns list of files for download.

        :return: list of download requests for
        """
        pass

    def get_safe_struct(self) -> dict:
        """Describes a structure inside tile folder of ESA product .SAFE structure.

        :return: nested dictionaries representing .SAFE structure
        """
        pass

    def _get_aux_substruct(self) -> dict:
        """Builds an auxiliary data subfolder structure of .SAFE format.

        Note: Old products also have DEM and MSI in aux folder which are not reconstructed here.
        """
        pass

    def _get_image_substruct(self) -> dict:
        """Builds the part of structure of .SAFE format that contains satellite imagery."""
        pass

    def _get_qi_substruct(self) -> dict:
        """Builds a quality-indicators data subfolder structure of .SAFE format."""
        pass

    def _get_reports_substruct(self) -> dict:
        """Builds a substructure of .SAFE format with reports."""
        pass

    def get_tile_id(self) -> str:
        """Creates ESA tile ID

        :return: ESA tile ID
        """
        pass

    def get_sensing_time(self) -> str:
        """
        :return: Exact tile sensing time
        """
        pass

    def get_datastrip_time(self) -> str:
        """
        :return: Exact datastrip time
        """
        pass

    def get_datatake_time(self) -> str:
        """
        :return: Exact time of datatake
        """
        pass

    def get_main_folder(self) -> str:
        """
        :return: name of tile folder
        """
        pass

    def get_tile_metadata_name(self) -> str:
        """
        :return: name of tile metadata file
        """
        pass

    def get_aux_data_name(self) -> str:
        """
        :return: name of auxiliary data file
        """
        pass

    def get_img_name(self, band: str, resolution: Optional[str] = None) -> str:
        """
        :param band: band name
        :param resolution: Specifies the resolution in case of Sentinel-2 L2A products
        :return: name of band image file
        """
        pass

    def get_qi_name(self, qi_type: str, band: str = "B00", data_format: MimeType = MimeType.GML) -> str:
        """
        :param qi_type: type of quality indicator
        :param band: band name
        :param data_format: format of the file
        :return: name of gml file
        """
        pass

    def get_preview_name(self) -> str:
        """Returns .SAFE name of full resolution L1C preview
        :return: name of preview file
        """
        pass


def _edit_name(name: str, code: str, add_code: Optional[str] = None, delete_end: bool = False) -> str:
    """Helping function for creating file names in .SAFE format

    :param name: initial string
    :param code:
    :param add_code:
    :param delete_end:
    :return: edited string
    """
    pass
