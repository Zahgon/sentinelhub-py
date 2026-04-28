"""
Module defining evalscript generation utilities
"""

from __future__ import annotations

import numpy as np

from .data_collections import DataCollection
from .data_collections_bands import Band, Unit

DTYPE_TO_SAMPLE_TYPE: dict[type, str] = {
    bool: "UINT8",
    np.uint8: "UINT8",
    np.uint16: "UINT16",
    np.float32: "FLOAT32",
}

EVALSCRIPT_TEMPLATE = """
//VERSION=3

function setup() {{
    return {{
        input: [{{
            bands: [{input_names}],
            units: [{input_units}]
        }}],
        output: [{output_spec}]
    }}
}}

function updateOutputMetadata(scenes, inputMetadata, outputMetadata) {{
    outputMetadata.userData = {{
        "norm_factor":  inputMetadata.normalizationFactor
    }}
}}

function evaluatePixel(sample) {{
    return {{ {return_spec} }};
}}
"""


def parse_data_collection_bands(data_collection: DataCollection, bands: list[str]) -> list[Band]:
    """Checks that all requested bands are available and returns the band information for further processing

    :param data_collection: A collection of requested satellite data.
    :param bands: A list of band or meta band names to use in the evalscript.
    """
    pass


def generate_evalscript(
    data_collection: DataCollection,
    bands: list[str] | None = None,
    meta_bands: list[str] | None = None,
    merged_bands_output: str | None = None,
    prioritize_dn: bool = True,
) -> str:
    """Generate an evalscript based on the provided specifications. This utility supports generating only evalscripts
    with the mosaicking option set to `SIMPLE`.

    :param data_collection: A collection of requested satellite data.
    :param bands: A list of band names to use in the evalscript. Defaults to using all bands provided by the collection.
    :param meta_bands: A list of meta band names to use in the evalscript. By default no meta bands are added.
    :param merged_bands_output: If provided, bands will be concatenated into a single multi-band tiff with this name.
    :param prioritize_dn: Use DN units if possible. Default is True. If DN units are not available, the default units
        for each specific band are used. DN units will be used regardless of the flag if they are the only possible
        choice.
    """
    pass
