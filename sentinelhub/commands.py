"""
Module that implements command line interface for the package
"""

from __future__ import annotations

import json
from typing import Any, Callable, TypeVar

import click

from .config import SHConfig
from .download import DownloadClient, DownloadRequest

FC = TypeVar("FC", bound=Callable[..., Any])


@click.command()
def main_help() -> None:
    """
    Welcome to sentinelhub Python library command line help.

    \b
    There are multiple modules with command line functionality:\n
       - sentinelhub.aws \n
       - sentinelhub.config \n
       - sentinelhub.download \n

    To check more about certain module command use: \n
      sentinelhub.<module name> --help
    """
    pass


def _config_options(func: FC) -> FC:
    """A helper function which joins `click.option` functions of each parameter from `SHConfig`."""
    pass


@click.command()
@click.option("--show", is_flag=True, default=False, help="Show current configuration")
@click.option("--profile", default=None, help="Selects profile to show/configure.")
@_config_options
def config(show: bool, profile: str | None, **params: Any) -> None:
    """Inspect and configure parameters in your local sentinelhub configuration file

    \b
    Example:
      sentinelhub.config --show
      sentinelhub.config --instance_id <new instance id>
      sentinelhub.config --max_download_attempts 5 --download_sleep_time 20 --download_timeout_seconds 120
    """
    pass


@click.command()
@click.argument("url")
@click.argument("filename", type=click.Path())
@click.option("-r", "--redownload", is_flag=True, default=False, help="Redownload existing files")
def download(url: str, filename: str, redownload: bool) -> None:
    """Download from custom created URL into custom created file path

    \b
    Example:
    sentinelhub.download https://roda.sentinel-hub.com/sentinel-s2-l1c/tiles/36/M/ZB/2022/3/17/0/metadata.xml \
./data/example.xml
    """
    pass
