# analyse weather/climate data from the german weather forcasting agency (deutscher wetter dienst, dwd)
# https://www.dwd.de/DE/leistungen/klimadatendeutschland/klarchivtagmonat.html?nn=16102

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, data_set):
        self.data_set = data_set
        data = self.data_set.data
        self.mean_year = data.groupby(data.index.day_of_year).aggregate(np.mean)
        self.years = data.groupby(data.index.year).aggregate([np.nanmin, np.nanmean, np.nanmax])

    def mean_temp_within_year(self):
        plt.fill_between(self.mean_year.index, self.mean_year.TNK, self.mean_year.TXK, alpha=0.3)
        plt.plot(self.mean_year.index, self.mean_year.TMK)
        plt.xlabel("day of the year")
        plt.ylabel("T [°C]")

    def mean_temp_over_years(self):
        plt.plot(self.years.index, self.years.TMK.nanmean)
        plt.xlabel("year")
        plt.ylabel("mean day temperature [°C]")

    def max_temp_over_years(self):
        plt.plot(self.years.index, self.years.TXK.nanmax)
        plt.xlabel("year")
        plt.ylabel("max temp of the year [°C]")
