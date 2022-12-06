import numpy as np, pandas as pd, matplotlib.pyplot as plt
import data, stations, util

for i, id in enumerate(stations.stations.Stations_id):
    print(f"{i + 1} of {stations.stations.Stations_id.size}")
    try:
        d = data.load_data(id)
    except KeyError:
        continue
    hist = d.NM.value_counts().sort_index()
    plt.plot(hist.index, hist.values / 8, color="tab:blue", alpha=0.2)
plt.xlabel("could coverage in %")
plt.ylabel("count")
plt.show()
