import numpy as np, pandas as pd, matplotlib.pyplot as plt

pd.set_option("display.width", None)

# even as this is german data, its using . as the decimal point
data = pd.read_csv("produkt_klima_tag_19360101_20211231_05371.txt",
        sep=";", index_col="MESS_DATUM", parse_dates=["MESS_DATUM"], skipinitialspace=True,
        dtype={"QN_3": "Int64", "QN_4": "Int64", "RSKF": "Int64", "SHK_TAG": "Int64"},)
data.pop("STATIONS_ID")
data.pop("eor")
# missing data is representated by -999 in the data set
# this sadly converts all float types with missing values to obj types
data.replace(-999, pd.NA, inplace=True)

# parameter descriptions
params = pd.read_csv("Metadaten_Parameter_klima_tag_05371.txt",
        encoding="utf8", sep=",", skipinitialspace=True)



