import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import data, util

# mean_year = data.groupby(data.index.day_of_year).aggregate(np.mean)

stations = data.load_stations()

def plot_station_positions():
    m = Basemap(
        projection="lcc",
        resolution="i", # c: curde, l: low, i: intermediate (h: high, f: full but these are not installed
        lat_0=0.5*(stations.geoBreite.min() + stations.geoBreite.max()),
        lon_0=0.5*(stations.geoLaenge.min() + stations.geoLaenge.max()),
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
    m.scatter(stations.geoLaenge, stations.geoBreite, color="black", marker="x", latlon=True)
    plt.title("Positions of DWD weather stations", pad=20)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

def find_name_by_id(i):
    return stations.Stationsname[stations.Stations_id == i].iloc[0]

def find_id_by_name(name, nth=0):
    return stations.Stations_id[
            stations.Stationsname.str.lower().str.contains(name.lower())
    ].iloc[nth]

def search_by_name(name):
    return stations.Stationsname[
            stations.Stationsname.str.lower().str.contains(name.lower())
    ]

if __name__ == "__main__":
    plot_station_positions()
    plt.show()
