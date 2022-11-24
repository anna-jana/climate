# daily weather data from german weather stations, provided
# by the german weather forcasting agency (deutscher wetterdienst)
# as open data:
# download, preprocesses store them on disk and load them back later
# data source (top level domain, see code for specific page): https://opendata.dwd.de

import io
import json
import os
import pathlib
import re
import urllib.request
import zipfile

import numpy as np
import pandas as pd

metadata_name = "metadata.json"
station_name_field = "station_name"
station_id_field = "station_id"

def preprocess_files(data_file, parameter_file):
    # even as this is german data, its using . as the decimal point
    data = pd.read_csv(data_file,
        sep=";", index_col="MESS_DATUM", parse_dates=["MESS_DATUM"], skipinitialspace=True,
        dtype={"QN_3": "Int64", "QN_4": "Int64", "RSKF": "Int64", "SHK_TAG": "Int64"},)
    data.pop("STATIONS_ID")
    data.pop("eor")
    # missing data is representated by -999 in the data set
    # this sadly converts all float types with missing values to obj types
    data.replace(-999, pd.NA, inplace=True)

    # parameter descriptions
    params = pd.read_csv(parameter_file,
            encoding="latin2", sep=";", skipinitialspace=True)
    params.drop(["Stations_ID", "Von_Datum", "Bis_Datum", "Stationsname", "eor",
                 "Unnamed: 12", "Besonderheiten", "Literaturhinweis"],
            axis="columns", inplace=True)
    params = params[~params.Parameter.duplicated(keep="first") & ~params.Parameter.isna()]
    params = params.set_index(params.Parameter).drop(["Parameter"], axis="columns")

    return data, params


def preprocess_and_save_single_station_zip(top_data_dir, zip_file):
    # figure out the name of the station name, data and parameter files
    # we dont care about the other files for this project (details on used instruments etc)
    data_filename = None
    station_name_filename = None
    parameter_filename = None
    for fname in zip_file.namelist():
        suffix = pathlib.Path(fname).suffix
        if fname.startswith("produkt"):
            assert data_filename is None
            data_filename = fname
        if fname.startswith("Metadaten_Stationsname") and suffix == ".txt":
            station_name_filename = fname
        if fname.startswith("Metadaten_Parameter") and suffix == ".txt":
            parameter_filename = fname

    # extract name and id of the weather station
    station_name_file = zip_file.open(station_name_filename)
    station_name_data = pd.read_csv(station_name_file,
            sep=";", encoding="latin2", skipinitialspace=True)
    station_name = station_name_data.Stationsname[0].strip()
    station_id = str(station_name_data.Stations_ID[0])
    print(f"{station_name =}, {station_id =} ...", end="", flush=True)

    # open data and parameter files
    zip_data_file = zip_file.open(data_filename)
    zip_parameter_file = zip_file.open(parameter_filename)

    # do some preprocessing
    data, parameter = preprocess_files(zip_data_file, zip_parameter_file)

    # create a direcotry for this specific station
    data_dir = os.path.join(top_data_dir, station_id)
    os.mkdir(data_dir)

    # write metadata
    metadata_filename = os.path.join(data_dir, metadata_name)
    metadata = {station_name_field: station_name, station_id_field: station_id}
    with open(metadata_filename, "w") as f:
        json.dump(metadata, f)

    # write the preprocessed data to disk
    disk_data_filename = os.path.join(data_dir, data_filename)
    disk_parameter_filename = os.path.join(data_dir, parameter_filename)
    data.to_csv(disk_data_filename)
    parameter.to_csv(disk_parameter_filename)

    print(" done")

default_top_data_dir = "dwd_climate_data_germnay"
stations_filename = "station_descriptions.txt"


def download_all_data(
        top_data_dir=default_top_data_dir,
        index_url="https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/",
        station_descriptions_filename="KL_Tageswerte_Beschreibung_Stationen.txt",
        ):
    # create top level directory containing all the different stations
    if os.path.exists(top_data_dir):
        raise RuntimeError("top level data directory already exists!")
    os.mkdir(top_data_dir)

    # download the content of the index page with all the different stations
    print("downloading index")
    index_res = urllib.request.urlopen(index_url)
    index_content_bytes = index_res.read()
    index_content = index_content_bytes.decode()

    # load the descriptions of all the stations including their geographical positions
    # and height above sealevel
    print("downloading station descriptions")
    descriptions_res = urllib.request.urlopen(urllib.request.urljoin(index_url, station_descriptions_filename))
    descriptions = pd.read_fwf(descriptions_res,
            colspecs=[(0, 6), (6, 15), (15, 34), (34, 43),
                      (43, 53), (53, 61), (61, 102), (102, 124)],
            encoding="latin2", skiprows=2, header=None,
            parse_dates=[1,2], infer_datetime_format=True,
            )
    descriptions.columns = ["Stations_id", "von_datum", "bis_datum",
            "Stationshoehe", "geoBreite", "geoLaenge",
            "Stationsname", "Bundesland"]
    descriptions.to_csv(os.path.join(top_data_dir, stations_filename))

    print("downlowding weather data for each station")
    # extract all links from the index page which link to zip files
    html_line = r'\<a href="(.+\.zip)"\>.+\.zip\</a\>'
    all_zip_link_matches = re.findall(html_line, index_content)

    for i, zip_name in enumerate(all_zip_link_matches):
        # download and open the zip file for the specific station url in memory
        zip_url = urllib.request.urljoin(index_url, zip_name)
        zip_res = urllib.request.urlopen(zip_url)
        zip_content_bytes = zip_res.read()
        zip_content_io = io.BytesIO(zip_content_bytes)
        zip_file = zipfile.ZipFile(zip_content_io)
        print(i + 1, "of", len(all_zip_link_matches), end=" ", flush=True)
        preprocess_and_save_single_station_zip(top_data_dir, zip_file)

