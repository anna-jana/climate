import os
import json
import dataclasses
import glob

import numpy as np
import pandas as pd

import download

@dataclasses.dataclass
class StationDataSet:
    id: "any"
    name: "any"
    data: "any"

def load_dir(path):
    # load the metadata
    metadata_fname = os.path.join(path, download.metadata_name)
    with open(metadata_fname, "r") as f:
        metadata = json.load(f)
        id = metadata[download.station_id_field]
        name = metadata[download.station_name_field]
    # load data file
    p = os.path.join(path, "produkt*")
    data_files = list(glob.glob(p))
    assert len(data_files) == 1
    data_filename = data_files[0]
    data = pd.read_csv(data_filename, parse_dates=["MESS_DATUM"], skipinitialspace=True, index_col="MESS_DATUM")
    return StationDataSet(id=id, name=name, data=data)


def load_all_dirs(top_data_dir=download.default_top_data_dir, load_subdirs=None):
    data = {}
    if load_subdirs is None:
        load_subdirs = os.listdir(top_data_dir)
    for name in load_subdirs:
        subdir = os.path.join(top_data_dir, name)
        if os.path.isdir(subdir):
            d = load_dir(subdir)
            data[d.id] = d
            print(d.id)
    return data

