import pandas as pd, numpy as np

def timeseries_corr(d1, d2):
    """
    Pearson correlation coefficient between two timeseries with not exactly matching timestamps.
    timestamps which are not shared between the timeseries are ignored.
    """
    full_range = pd.date_range(min(d1.index[0], d2.index[0]), max(d1.index[-1], d2.index[-1]))
    series1 = d1.reindex(full_range)
    series2 = d2.reindex(full_range)
    both_avl = ~(series1.isna() | series2.isna())
    C = np.corrcoef(series1[both_avl], series2[both_avl])
    return C[0, 1] # C = [1 c; c 1]

def hav(theta):
    return np.sin(theta / 2)**2

def inv_hav(h):
    return 2*np.arcsin(np.sqrt(h))

earth_radius = 6371.0 # [km]

def geographic_distance(lat1, long1, lat2, long2):
    """
    geographic distance between point 1 = (lat1, long1) [deg] and point 2 = (lat2, long2) [deg] in km
    """
    lat1, long1, lat2, long2 = np.deg2rad(lat1), np.deg2rad(long1), np.deg2rad(lat2), np.deg2rad(long2)
    hav_theta = hav(lat1 - lat2) + np.cos(lat1) * np.cos(lat2) * hav(long1 - long2)
    theta = inv_hav(hav_theta)
    return theta * earth_radius
