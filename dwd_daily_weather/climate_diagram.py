import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import data, util, stations

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

if __name__ == "__main__":
    plot_climate_diagram(data.load_data(stations.find_id_by_name("wasserkuppe")), "wasserkuppe")
    plt.show()
