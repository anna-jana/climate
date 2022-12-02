import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import data, util, stations

def correlations_vs_distance(col, nsamples=1000):
    np.random.seed(42)
    result = []
    while len(result) < nsamples:
        print(f"{len(result) + 1} of {nsamples}")
        i = np.random.randint(stations.stations.index.size)
        j = np.random.randint(stations.stations.index.size)
        id1 = stations.stations.Stations_id[i]
        id2 = stations.stations.Stations_id[j]
        try:
            d1 = data.load_data(id1)
            d2 = data.load_data(id2)
        except KeyError:
            continue
        c = util.timeseries_corr(d1[col], d2[col])
        if not np.isfinite(c):
            continue
        d = util.geographic_distance(
                stations.stations.geoBreite[i], stations.stations.geoLaenge[i],
                stations.stations.geoBreite[j], stations.stations.geoLaenge[j],
        )
        result.append(dict(station1=id1, station2=id2, distance=d, correlation=c))
    return pd.DataFrame(result)

def plot_correlations_vs_distance(res, name):
    plt.plot(res.distance, res.correlation, ".")
    plt.xlabel("distance [km]")
    plt.ylabel("correlation [1]")
    plt.title(name)

fname_temp = "corr_TMK.pkl"
fname_rain = "corr_RSK.pkl"
fname_humidity = "corr_UPM.pkl"
fname_steampressure = "corr_VPM.pkl"

def compute():
    res = correlations_vs_distance("TMK") # mean temp
    res.to_pickle(fname_temp)
    res = correlations_vs_distance("RSK") # total rainfall
    res.to_pickle(fname_rain)
    res = correlations_vs_distance("UPM") # mean humidity
    res.to_pickle(fname_humidity)
    res = correlations_vs_distance("VPM") # mean steampressure
    res.to_pickle(fname_steampressure)

def plot():
    plt.figure(layout="constrained")

    plt.subplot(2,2,1)
    res = pd.read_pickle(fname_temp)
    plot_correlations_vs_distance(res, "mean daily temperature")

    plt.subplot(2,2,2)
    res = pd.read_pickle(fname_rain)
    plot_correlations_vs_distance(res, "daily total rainfall")

    plt.subplot(2,2,3)
    res = pd.read_pickle(fname_rain)
    res = pd.read_pickle(fname_humidity)
    plot_correlations_vs_distance(res, "mean daily humidity")

    plt.subplot(2,2,4)
    res = pd.read_pickle(fname_steampressure)
    plot_correlations_vs_distance(res, "mean daily steam-pressure")

    plt.show()
