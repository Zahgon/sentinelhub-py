"""
Module implementing utilities for collecting data, produced with Sentinel Hub Statistical Batch API, from an S3 bucket.
"""

from typing import List, Optional, Sequence, Union

from ..api.batch.statistical import BatchStatisticalRequest, BatchStatisticalRequestType, SentinelHubBatchStatistical
from ..base import DataRequest
from ..config import SHConfig
from ..constants import MimeType
from ..download.models import DownloadRequest
from .client import AwsDownloadClient


class AwsBatchStatisticalResults(DataRequest):
    """A utility class for downloading results of Batch Statistical API from an S3 bucket."""

    def __init__(
        self,
        batch_request: BatchStatisticalRequestType,
        *,
        feature_ids: Optional[Sequence[Union[str, int]]] = None,
        data_folder: Optional[str] = None,
        config: Optional[SHConfig] = None,
    ):
        """
        :param batch_request: Info about a batch request - either an instance of `BatchStatisticalRequest` or a
            batch ID or a raw payload of the batch response.
        :param feature_ids: A list of feature IDs of saved results on the bucket. If provided it will download only
            these results. If not provided it will collect the names of all JSON files from results folder on the
            bucket and download all of them. Note that it is recommended that you provide this parameter otherwise this
            class will have to make additional requests to the S3 bucket in order to list all features from the folder.
        :param data_folder: Directory to which the files should be saved.
        :param config: A config object that contains AWS credentials to access the S3 bucket with results.
        """
        self.batch_request = self._parse_batch_request(batch_request, config)
        self.feature_ids = feature_ids

        super().__init__(AwsDownloadClient, data_folder=data_folder, config=config)

    @staticmethod
    def _parse_batch_request(
        batch_request: BatchStatisticalRequestType, config: Optional[SHConfig]
    ) -> BatchStatisticalRequest:
        """In case a batch request is not defined with an instance of `BatchStatisticalRequest` it will make sure that
        such an instance is created."""
        pass

    def create_request(self) -> None:
        """Creates a list of download requests."""
        pass

    def _get_filenames(self, s3_path: str) -> List[str]:
        """Creates a list of JSON filenames from given feature ids or from given S3 path if feature ids are not
        provided. In case if it has to collect them from S3 path it makes sure not to collect any data from any
        subfolder in the path."""
        pass
