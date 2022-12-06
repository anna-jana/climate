import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import data, util, stations

def plot_trends(d, name=""):
    years = d.groupby(d.index.year).aggregate([np.nanmin, np.nanmean, np.nanmax])
    fig, axs = plt.subplots(1, 3, layout="constrained")
    years.TMK.nanmin.plot(ax=axs[0])
    axs[0].set_xlabel("year")
    axs[0].set_ylabel("temperature [°C]")
    axs[0].set_title("min")
    years.TMK.nanmean.plot(ax=axs[1])
    axs[1].set_xlabel("year")
    axs[1].set_title("mean")
    years.TMK.nanmax.plot(ax=axs[2])
    axs[2].set_xlabel("year")
    axs[2].set_title("max")
    fig.suptitle(name)

if __name__ == "__main__":
    plot_trends(data.load_data(stations.find_id_by_name("wasserkuppe")), "wasserkuppe")
    plt.show()
