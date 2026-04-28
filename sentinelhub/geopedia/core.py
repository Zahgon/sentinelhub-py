"""
The core module for Geopedia interactions
"""

from __future__ import annotations

import datetime
import hashlib
from typing import TYPE_CHECKING, Any, Iterable, Iterator, Literal, overload

from shapely.geometry import shape as geo_shape
from shapely.geometry.base import BaseGeometry

from ..api.ogc import OgcImageService, OgcRequest
from ..base import FeatureIterator
from ..config import SHConfig
from ..constants import CRS, MimeType
from ..download import DownloadClient, DownloadRequest
from ..geometry import BBox
from ..types import JsonDict

if TYPE_CHECKING:
    from .request import GeopediaImageRequest


class GeopediaService:
    """The class for Geopedia OGC services"""

    def __init__(self, config: SHConfig | None = None):
        """
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.config = config or SHConfig()
        self._base_url = self.config.geopedia_rest_url


@overload
def _parse_geopedia_layer(layer: int | str, return_wms_name: Literal[False] = False) -> int: ...


@overload
def _parse_geopedia_layer(layer: int | str, return_wms_name: Literal[True]) -> str: ...


def _parse_geopedia_layer(layer: int | str, return_wms_name: bool = False) -> int | str:
    """Helper function for parsing Geopedia layer name. If WMS name is required and wrong form is given it will
    return a string with 'ttl' at the beginning. (WMS name can also start with something else, e.g. only 't'
    instead 'ttl', therefore anything else is also allowed.) Otherwise, it will parse it into a number.
    """
    pass


class GeopediaSession(GeopediaService):
    """For retrieving data from Geopedia vector and raster layers it is required to make a session. This class handles
    starting and renewing of session and login (optional). It provides session headers required by Geopedia REST
    requests. Session duration is hardcoded to 1 hour with class attribute SESSION_DURATION. After that this
    class will automatically renew the session and login.
    """

    SESSION_DURATION = datetime.timedelta(hours=1)
    UNAUTHENTICATED_USER_ID = "NO_USER"

    _global_session_info = None
    _global_session_start = None

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        password_md5: str | None = None,
        is_global: bool = False,
        **kwargs: Any,
    ):
        """
        :param username: Optional parameter in case of login with Geopedia credentials
        :param password: Optional parameter in case of login with Geopedia credentials
        :param password_md5: Password can optionally also be provided as already encoded md5 hexadecimal string
        :param is_global: If `True` this session will be shared among all instances of this class, otherwise it will be
            used only with the single instance. Default is `False`.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        super().__init__(**kwargs)

        if password and password_md5:
            raise ValueError("At most one of the parameters 'password' and 'password_md5' can be specified, not both")

        self.username = username
        self.password = password_md5 if password is None else hashlib.md5(password.encode()).hexdigest()
        self.is_global = is_global

        if bool(self.username) != bool(self.password):
            raise ValueError(
                "Either both username and password have to be specified or neither of them, only one found"
            )

        self._session_info: dict | None = None
        self._session_start: datetime.datetime | None = None

        self.provide_session()

    @property
    def session_info(self) -> dict:
        """All information that Geopedia provides about the current session

        :return: A dictionary with session info
        """
        pass

    @property
    def session_id(self) -> str:
        """A public property of this class which provides a Geopedia session ID

        :return: A session ID string
        """
        pass

    @property
    def session_headers(self) -> dict:
        """Headers which have to be used when accessing any data from Geopedia with this session

        :return: A dictionary containing session headers
        """
        pass

    @property
    def user_info(self) -> dict:
        """Information that this session has about user

        :return: A dictionary with user info
        """
        pass

    @property
    def user_id(self) -> str:
        """Geopedia user ID. If no login was done during session this will return `'NO_USER'`.

        :return: User ID string
        """
        pass

    def restart(self) -> GeopediaSession:
        """Method that restarts Geopedia Session

        :return: It returns the object itself, with new session
        """
        pass

    def provide_session(self, start_new: bool = False) -> dict:
        """Makes sure that session is still valid and provides session info

        :param start_new: If `True` it will always create a new session. Otherwise, it will create a new
            session only if no session exists or the previous session timed out.
        :return: Current session info
        """
        pass

    def _start_new_session(self) -> None:
        """Starts a new session and calculates when the new session will end. If username and password are provided
        it will also make login.
        """
        pass

    def _make_login(self, session_info: dict) -> None:
        """Private method that makes login"""
        pass

    @staticmethod
    def _parse_session_id(session_info: dict) -> str:
        """Method for parsing session ID from session info"""
        pass

    @staticmethod
    def _parse_user_id(session_info: dict) -> str:
        """Method for parsing user ID from session info"""
        pass


class GeopediaWmsService(GeopediaService, OgcImageService):
    """Geopedia OGC services class for providing image data. Most of the methods are inherited from
    `sentinelhub.ogc.OgcImageService` class.
    """

    def __init__(self, **kwargs: Any):
        """
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        super().__init__(**kwargs)

        self._base_url = self.config.geopedia_wms_url

    def get_request(self, request: OgcRequest) -> list[DownloadRequest]:
        """Get a list of DownloadRequests for all data that are under the given field in the table of a Geopedia layer.

        :return: list of items which have to be downloaded
        """
        pass

    def get_dates(self, _: OgcRequest) -> list[datetime.datetime | None]:
        """Geopedia does not support date queries

        :param request: OGC-type request
        :return: Undefined date
        """
        pass

    def get_wfs_iterator(self) -> Any:
        """This method is inherited from OgcImageService but is not implemented."""
        pass


class GeopediaImageService(GeopediaService):
    """Service class that provides images from a Geopedia vector layer."""

    def __init__(self, **kwargs: Any):
        """
        :param base_url: Base url of Geopedia REST services. If `None`, the url
                     specified in the configuration file is taken.
        """
        super().__init__(**kwargs)

        self.gpd_iterator: GeopediaFeatureIterator | None = None

    def get_request(self, request: GeopediaImageRequest) -> list[DownloadRequest]:
        """Get a list of DownloadRequests for all data that are under the given field in the table of a Geopedia layer.

        :return: list of items which have to be downloaded
        """
        pass

    def _get_items(self, request: GeopediaImageRequest) -> list:
        """Collects data from Geopedia layer and returns list of features"""
        pass

    @staticmethod
    def _get_url(item: dict) -> str | None:
        pass

    @staticmethod
    def _get_filename(request: GeopediaImageRequest, item: dict) -> str | None:
        """Creates a filename"""
        pass

    def get_gpd_iterator(self) -> GeopediaFeatureIterator | None:
        """Returns iterator over info about data used for the `GeopediaVectorRequest`

        :return: Iterator of dictionaries containing info about data used in the request.
        """
        pass


class GeopediaFeatureIterator(FeatureIterator[JsonDict]):
    """Iterator for Geopedia Vector Service"""

    FILTER_EXPRESSION = "filterExpression"
    MAX_FEATURES_PER_REQUEST = 1000

    def __init__(
        self,
        layer: str | int,
        bbox: BBox | None = None,
        query_filter: str | None = None,
        offset: int = 0,
        gpd_session: GeopediaSession | None = None,
        config: SHConfig | None = None,
    ):
        """
        :param layer: Geopedia layer which contains requested data
        :param bbox: Bounding box of the requested image. Its coordinates must be in the CRS.POP_WEB (EPSG:3857)
            coordinate system.
        :param query_filter: Query string used for filtering returned features.
        :param offset: Offset of resulting features
        :param gpd_session: Optional parameter for specifying a custom Geopedia session, which can also contain login
            credentials. This can be used for accessing private Geopedia layers. By default, it is set to `None` and a
            basic Geopedia session without credentials will be created.
        :param config: A custom instance of config class to override parameters from the saved configuration.
        """
        self.layer = _parse_geopedia_layer(layer)
        self.config = config or SHConfig()
        self.gpd_session = gpd_session if gpd_session else GeopediaSession(is_global=True)

        client = DownloadClient(config=self.config)
        url = f"{self.config.geopedia_rest_url}/data/v2/search/tables/{self.layer}/features"
        params = self._build_request_params(bbox, query_filter)

        super().__init__(client, url, params)
        self.next = f"{url}?offset={offset}&limit={self.MAX_FEATURES_PER_REQUEST}"

        self.layer_size: int | None = None

    def _build_request_params(self, bbox: BBox | None, query_filter: str | None) -> dict:
        """Builds payload parameters for requests to Geopedia"""
        pass

    def __len__(self) -> int:
        """Length of iterator is number of features which can be obtained from Geopedia with applied filters"""
        return self.get_size()

    def _fetch_features(self) -> Iterable[JsonDict]:
        """Retrieves a new page of features from Geopedia"""
        pass

    def get_geometry_iterator(self) -> Iterator[BaseGeometry]:
        """Iterator over Geopedia feature geometries"""
        pass

    def get_field_iterator(self, field: str) -> Iterator[Any]:
        """Iterator over the specified field of Geopedia features"""
        pass

    def get_size(self) -> int:
        """Provides number of features which can be obtained. It has to fetch at least one feature from
        Geopedia services to get this information.

        :return: Size of Geopedia layer with applied filters
        """
        pass
