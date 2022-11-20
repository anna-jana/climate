import numpy as np, pandas as pd, matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

d = pd.read_csv("dwd_climate_data_germnay/station_descriptions.txt", parse_dates=["von_datum", "bis_datum"])
d.drop(["Unnamed: 0"], axis=1, inplace=True)

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

plt.show()
