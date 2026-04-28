"""
Module implementing some common utility functions
"""

# ruff: noqa: FA100
# do not use `from __future__ import annotations`, it clashes with `dataclass_json`
from enum import Enum
from typing import Any, Dict, Optional, Type, TypedDict

from dataclasses_json import LetterCase
from dataclasses_json import config as dataclass_config

from sentinelhub.types import JsonDict

from ..geometry import Geometry
from ..time_utils import parse_time, serialize_time

datetime_config = dataclass_config(
    encoder=lambda time: serialize_time(time, use_tz=True) if time else None,
    decoder=lambda time: parse_time(time, force_datetime=True) if time else None,
    letter_case=LetterCase.CAMEL,
)

geometry_config = dataclass_config(
    encoder=Geometry.get_geojson,
    decoder=lambda geojson: Geometry.from_geojson(geojson) if geojson else None,
    exclude=lambda geojson: geojson is None,
    letter_case=LetterCase.CAMEL,
)


def enum_config(enum_class: Type[Enum]) -> Dict[str, dict]:
    """Given an Enum class it provide an object for serialization/deserialization"""
    pass


def _update_other_args(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> None:
    """Function for a recursive update of `dict1` with `dict2`. The function loops over the keys in `dict2` and
    only the non-dict like values are assigned to the specified keys.
    """
    pass


def remove_undefined(payload: dict) -> dict:
    """Takes a dictionary and removes keys without value"""
    pass


class AccessSpecification(TypedDict):
    """Specification of a S3 input or output."""

    s3: JsonDict


def s3_specification(
    url: str,
    access_key: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    iam_role_arn: Optional[str] = None,
    region: Optional[str] = None,
) -> AccessSpecification:
    """A helper method to build a dictionary used for specifying S3 paths. Consult the
    `access documentation <https://docs.sentinel-hub.com/api/latest/api/batch-statistical/#aws-bucket-access>`__
    for more information.

    In general either use `iam_role_arn` or `access_key` plus `secret_access_key`.

    :param url: A URL pointing to an S3 bucket or an object in an S3 bucket.
    :param access_key: AWS access key that allows programmatic access to the S3 bucket specified in the `url` field.
    :param secret_access_key: AWS secret access key which must correspond to the AWS access key.
    :param iam_role_arn: IAM role ARN, which allows programmatic access to the S3 bucket specified in the `url` field
        using the recommended assume IAM role flow.
    :param region: The region where the S3 bucket is located. If omitted, the region of the Sentinel Hub deployment
        that the request is submitted to is assumed.
    :return: A dictionary of S3 specifications used by the Batch Statistical API
    """
    pass
