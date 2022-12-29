import numpy as np, pandas as pd, matplotlib.pyplot as plt
import data, stations

def plot_temp_over_one_year(location, year):
    d = data.load_data(stations.find_id_by_name(location))
    d_year = d[d.index.year == year]
    plt.figure()
    plt.plot(d_year.index.day_of_year, d_year.TMK)
    plt.xlabel("time [day within year]")
    plt.ylabel("daily temperature (mean) [°C]")
    plt.title(location)

if __name__ == "__main__":
    plot_temp_over_one_year(location="göttingen", year=2021)
    plt.show()
