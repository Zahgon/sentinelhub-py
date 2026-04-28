"""
Data request interface for downloading satellite data from AWS
"""

import functools
from abc import abstractmethod
from typing import Any, Generic, List, Optional, Tuple, TypeVar, Union
from typing_extensions import deprecated

from ..base import DataRequest
from ..data_collections import DataCollection
from ..exceptions import SHDeprecationWarning
from .client import AwsDownloadClient
from .data import REQUESTER_PAYS_PARAMS, AwsProduct, AwsTile
from .data_safe import SafeProduct, SafeTile

T = TypeVar("T")


class _BaseAwsDataRequest(DataRequest, Generic[T]):
    """The base class for Amazon Web Service request classes. Common parameters are defined here.

    Collects and provides data from AWS.

    More information about Sentinel-2 AWS registry: https://registry.opendata.aws/sentinel-2/
    """

    def __init__(
        self,
        *,
        bands: Union[None, str, List[str]] = None,
        metafiles: Union[None, str, List[str]] = None,
        safe_format: bool = False,
        **kwargs: Any,
    ):
        """
        :param bands: List of Sentinel-2 bands for request. If `None` all bands will be obtained
        :param metafiles: list of additional metafiles available on AWS
                          (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``)
        :param safe_format: flag that determines the structure of saved data. If `True` it will be saved in .SAFE format
                            defined by ESA. If `False` it will be saved in the same structure as the structure at AWS.
        :param data_folder: location of the directory where the fetched data will be saved.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.bands = bands
        self.metafiles = metafiles
        self.safe_format = safe_format

        self.aws_service: T

        client_class = functools.partial(AwsDownloadClient, boto_params=REQUESTER_PAYS_PARAMS)
        super().__init__(client_class, **kwargs)

    @abstractmethod
    def create_request(self) -> None:
        pass

    def get_aws_service(self) -> T:
        """
        :return: initialized AWS service class
        """
        pass


@deprecated(
    "AWS functionality will remain in the codebase for now, but won't be actively maintained.",
    category=SHDeprecationWarning,
)
class AwsProductRequest(_BaseAwsDataRequest[AwsProduct]):
    """AWS Service request class for an ESA product."""

    def __init__(self, product_id: str, *, tile_list: Optional[List[str]] = None, **kwargs: Any):
        """
        :param product_id: original ESA product identification string
            (e.g. ``'S2A_MSIL1C_20170414T003551_N0204_R016_T54HVH_20170414T003551'``)
        :param tile_list: list of tiles inside the product to be downloaded. If parameter is set to `None` all
            tiles inside the product will be downloaded.
        :param bands: List of Sentinel-2 bands for request. If `None` all bands will be obtained
        :param metafiles: list of additional metafiles available on AWS
            (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``)
        :param safe_format: flag that determines the structure of saved data. If `True` it will be saved in .SAFE format
            defined by ESA. If `False` it will be saved in the same structure as the structure at AWS.
        :param data_folder: location of the directory where the fetched data will be saved.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.product_id = product_id
        self.tile_list = tile_list

        super().__init__(**kwargs)

    def create_request(self) -> None:
        pass


@deprecated(
    "AWS functionality will remain in the codebase for now, but won't be actively maintained.",
    category=SHDeprecationWarning,
)
class AwsTileRequest(_BaseAwsDataRequest[AwsTile]):
    """AWS Service request class for an ESA tile."""

    def __init__(
        self,
        *,
        data_collection: DataCollection,
        tile: Optional[str] = None,
        time: Optional[str] = None,
        aws_index: Optional[int] = None,
        **kwargs: Any,
    ):
        """
        :param data_collection: A collection of requested AWS data. Supported collections are Sentinel-2 L1C and
            Sentinel-2 L2A.
        :param tile: tile name (e.g. ``'T10UEV'``)
        :param time: tile sensing time in ISO8601 format
        :param aws_index: there exist Sentinel-2 tiles with the same tile and time parameter. Therefore, each tile on
            AWS also has an index which is visible in their url path. If aws_index is set to `None` the class
            will try to find the index automatically. If there will be multiple choices it will choose the
            lowest index and inform the user.
        :param bands: List of Sentinel-2 bands for request. If `None` all bands will be obtained
        :param metafiles: list of additional metafiles available on AWS
            (e.g. ``['metadata', 'tileInfo', 'preview/B01', 'TCI']``)
        :param safe_format: flag that determines the structure of saved data. If `True` it will be saved in .SAFE
            format defined by ESA. If `False` it will be saved in the same structure as the structure at AWS.
        :param data_folder: location of the directory where the fetched data will be saved.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.data_collection = data_collection
        self.tile = tile
        self.time = time
        self.aws_index = aws_index

        super().__init__(**kwargs)

    def create_request(self) -> None:
        pass


def get_safe_format(
    product_id: Optional[str] = None,
    tile: Optional[Tuple[str, str]] = None,
    entire_product: bool = False,
    bands: Union[None, str, List[str]] = None,
    data_collection: Optional[DataCollection] = None,
) -> dict:
    """Returns .SAFE format structure in form of nested dictionaries. Either ``product_id`` or ``tile`` must be
    specified.

    :param product_id: original ESA product identification string. Default is `None`
    :param tile: tuple containing tile name and sensing time/date. Default is `None`
    :param entire_product: in case tile is specified this flag determines if it will be place inside a .SAFE structure
        of the product. Default is `False`
    :param bands: list of bands to download. If `None` all bands will be downloaded. Default is `None`
    :param data_collection: In case of tile request the collection of satellite data has to be specified.
    :return: Nested dictionaries representing .SAFE structure.
    """
    pass


def download_safe_format(
    product_id: Optional[str] = None,
    tile: Optional[Tuple[str, str]] = None,
    folder: str = ".",
    redownload: bool = False,
    entire_product: bool = False,
    bands: Optional[List[str]] = None,
    data_collection: Optional[DataCollection] = None,
) -> None:
    """Downloads .SAFE format structure in form of nested dictionaries. Either ``product_id`` or ``tile`` must
    be specified.

    :param product_id: original ESA product identification string. Default is `None`
    :param tile: tuple containing tile name and sensing time/date. Default is `None`
    :param folder: location of the directory where the fetched data will be saved. Default is ``'.'``
    :param redownload: if `True`, download again the requested data even though it's already saved to disk. If
        `False`, do not download if data is already available on disk. Default is `False`
    :param entire_product: in case tile is specified this flag determines if it will be place inside a .SAFE structure
        of the product. Default is `False`
    :param bands: list of bands to download. If `None` all bands will be downloaded. Default is `None`
    :param data_collection: In case of tile request the collection of satellite data has to be specified.
    :return: Nested dictionaries representing .SAFE structure.
    """
    pass
