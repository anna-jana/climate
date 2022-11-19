# analyse weather/climate data from the german weather forcasting agency (deutscher wetter dienst, dwd)
# https://www.dwd.de/DE/leistungen/klimadatendeutschland/klarchivtagmonat.html?nn=16102
import numpy as np, pandas as pd, matplotlib.pyplot as plt

pd.set_option("display.width", None)
plt.ion()

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
