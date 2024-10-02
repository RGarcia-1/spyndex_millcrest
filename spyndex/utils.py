import json

import pkg_resources
import requests
from pathlib import Path


def load_json(js_file: str = "millcrest_spectral_indices.json") -> dict:
    """
    Loads the specified JSON file from the data folder.

    Parameters
    ----------
    js_file : str
        Json filename in the spyndex/data/ directory.
        Default is "millcrest_spectral_indices.json"

    Returns
    -------
    data : dict
        Contents of the json file as a dict.
    """
    spyndex_path = Path(pkg_resources.resource_filename("spyndex", "spyndex.py"))
    local_fn = spyndex_path.parent / f"data/{js_file}"

    with local_fn.open("r") as fid:
        data = json.load(fid)

    return data


def get_indices(online=False):
    """Retrieves the JSON of indices.

    Parameters
    ----------
    online : boolean
        Wheter to retrieve the most recent list of indices directly from the GitHub
        repository and not from the local copy.

    Returns
    -------
    dict
        Indices.
    """
    if online:
        indices = requests.get(
            "https://raw.githubusercontent.com/awesome-spectral-indices/awesome-spectral-indices/main/output/spectral-indices-dict.json"
        ).json()
    else:
        indices = load_json()

    return indices["SpectralIndices"]


def check_params(index: str, params: dict, indices: dict):
    """Checks if the parameters dictionary contains all required bands for the index
    computation.

    Parameters
    ----------
    index : str
        Index to check.
    params : dict
        Parameters dictionary to check.
    indices : dict
        Indices dictionary to check.

    Returns
    -------
    None
    """
    for band in indices[index]["bands"]:
        if band not in list(params.keys()):
            raise Exception(
                f"'{band}' is missing in the parameters for {index} computation!"
            )
