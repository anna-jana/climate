# analyse weather/climate data from the german weather forcasting agency (deutscher wetter dienst, dwd)
import numpy as np, pandas as pd, matplotlib.pyplot as plt

pd.set_option("display.width", None)
plt.ion()

############################################## loading the data #############################################
# even as this is german data, its using . as the decimal point
data = pd.read_csv("wasserkuppe/produkt_klima_tag_19360101_20211231_05371.txt",
        sep=";", index_col="MESS_DATUM", parse_dates=["MESS_DATUM"], skipinitialspace=True,
        dtype={"QN_3": "Int64", "QN_4": "Int64", "RSKF": "Int64", "SHK_TAG": "Int64"},)
data.pop("STATIONS_ID")
data.pop("eor")
# missing data is representated by -999 in the data set
# this sadly converts all float types with missing values to obj types
data.replace(-999, pd.NA, inplace=True)

# parameter descriptions
params = pd.read_csv("wasserkuppe/Metadaten_Parameter_klima_tag_05371.txt",
        encoding="latin2", sep=";", skipinitialspace=True)
params.drop(["Stations_ID", "Von_Datum", "Bis_Datum", "Stationsname", "eor",
             "Unnamed: 12", "Besonderheiten", "Literaturhinweis"],
        axis="columns", inplace=True)
params = params[~params.Parameter.duplicated(keep="first") & ~params.Parameter.isna()]
params = params.set_index(params.Parameter).drop(["Parameter"], axis="columns")

############################################## basic analysis ###############################################
# transformations
mean_year = data.groupby(data.index.day_of_year).aggregate(np.mean)
years = data.groupby(data.index.year).aggregate([np.nanmin, np.nanmean, np.nanmax])

# plots
def mean_temp_within_year():
    plt.fill_between(mean_year.index, mean_year.TNK, mean_year.TXK, alpha=0.3)
    plt.plot(mean_year.index, mean_year.TMK)
    plt.xlabel("day of the year")
    plt.ylabel("T [°C]")

def mean_temp_over_years():
    plt.plot(years.index, years.TMK.nanmean)
    plt.xlabel("year")
    plt.ylabel("mean day temperature [°C]")

def max_temp_over_years():
    plt.plot(years.index, years.TXK.nanmax)
    plt.xlabel("year")
    plt.ylabel("max temp of the year [°C]")
