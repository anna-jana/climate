import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import data

class Analysis:
    def __init__(self, data):
        self.mean_year = data.groupby(data.index.day_of_year).aggregate(np.mean)
        self.years = data.groupby(data.index.year).aggregate([np.nanmin, np.nanmean, np.nanmax])

def plot_station_positions(d):
    m = Basemap(
        projection="lcc",
        resolution="i", # c: curde, l: low, i: intermediate (h: high, f: full but these are not installed
        lat_0=0.5*(d.geoBreite.min() + d.geoBreite.max()),
        lon_0=0.5*(d.geoLaenge.min() + d.geoLaenge.max()),
        width=1000_000,
        height=1000_000,
    )

    water_color = (0.3, 0.3, 0.7)
    m.drawcoastlines() # black lines for the coast
    m.drawmapboundary(fill_color=water_color) # the sea/ocean in blue
    m.fillcontinents(color=(0.7, 0.7, 0), lake_color=water_color) # the continents in brown (coral, whatever this is) and lakes in blue
    m.drawcountries() # boarders between nations (hate them)
    #m.drawrivers(color=water_color)
    parallels = np.arange(46, 58, 2)
    m.drawparallels(parallels, labels=[True]*len(parallels))
    meridians = np.arange(4, 18, 2)
    m.drawmeridians(meridians, labels=[True]*len(meridians))

    m.scatter(d.geoLaenge, d.geoBreite, color="black", marker="x", latlon=True)

    plt.title("Positions of DWD weather stations", pad=20)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

stations = data.load_stations()

def find_name_by_id(i):
    return stations.Stationsname[stations.Stations_id == i].iloc[0]

def find_id_by_name(name):
    return stations.Stations_id[
            stations.Stationsname.str.lower().str.contains(name.lower())
    ].iloc[0]

def plot_mean_trend(d, name=None):
    a = Analysis(d)
    plt.figure(layout="constrained")
    a.years.TMK.nanmean.plot()
    plt.xlabel("year")
    plt.ylabel("mean temperature in year [°C]")
    plt.title(name)

def plot_max_trend(d):
    a = Analysis(d)
    a.years.TXK.nanmax.plot()
    plt.xlabel("year")
    plt.ylabel("mean temperature in year [°C]")
    plt.title(name)

def plot_climate_diagram(d, name=None):
    by_months = d.groupby(d.index.month)
    min_  = by_months.aggregate(np.min)
    mean_ = by_months.aggregate(np.mean)
    max_  = by_months.aggregate(np.max)
    months = range(1, 12 + 1)

    plt.figure(layout="constrained")
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax1.fill_between(months, min_.TNK, max_.TXK, color="red", alpha=0.3)
    ax1.plot(months, mean_.TMK, color="red")
    ax1.set_ylabel("temperature [°C]")
    ax1.set_xlabel("month")
    ax1.set_xticks(months,
            ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December",],
            rotation=30)
    ax1.set_title(name)
    ax2.bar(months, mean_.RSK, alpha=0.7)
    ax2.set_ylabel("rainfall (height) [mm]")





