import urllib.request, io
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

default_data_filename = "data.hdf5"
default_categories_filename = "categories.csv"

def download_data(url="https://zenodo.org/record/4723476/files/Guetschow-et-al-2021-PRIMAP-crf96_2021-v1.csv?download=1",
                  filename=default_data_filename):
    primap_res = urllib.request.urlopen(url)
    d = pd.read_csv(primap_res)
    source = d.source[0]
    scenario = d["scenario (PRIMAP)"][0]
    provenance = d.provenance[0]
    d.drop("source", inplace=True, axis=1)
    d.drop("scenario (PRIMAP)", inplace=True, axis=1)
    d.drop("provenance", inplace=True, axis=1)
    # d.entity is the kind of greenhouse gas
    # d.unit is always (k)t <entity> / yr", so we only need to check if its per t or kt
    d["is_kilo"] = d.unit.str.startswith("k")
    # category (IPCC1996) is the field from which the emission is sourced
    d.drop("unit", inplace=True, axis=1)
    d.rename(inplace=True, columns={
        "area (ISO3)": "country",
        "entity": "greenhouse_gas",
        "category (IPCC1996)": "category",
    })
    d.to_hdf(filename, "main")
    return d

def load_data(filename=default_data_filename):
    return pd.read_hdf(filename, "main")

def load_gases():
    return pd.read_csv("gases.txt", sep=";", skipinitialspace=True)

def download_categories(url="https://zenodo.org/record/4723476/files/PRIMAP-crf-IPCC2006-category-codes.csv?download=1",
                        filename=default_categories_filename):
    category_res = urllib.request.urlopen(url)
    categories = pd.read_csv(category_res)
    categories.rename(inplace=True, columns={
        "Category Code (IPCC2006)" : "IPCC_Code",
        "Category Name" : "Name",
        "Category Code (PRIMAP1)" : "PRIMAP1_Code",
    })
    categories.to_csv(filename)
    return categories

def load_categories(filename=default_categories_filename):
    return pd.read_csv(filename)

years = list(map(str, range(1986, 2019 + 1)))
