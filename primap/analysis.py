import numpy as np, pandas as pd, matplotlib.pyplot as plt
import data

plt.ion()

d = data.load_data()

def plot_emissions(country_code="DEU", gas="CO2", fig=None):
    by_gas_and_country = d[(d.country == country_code) & (d.greenhouse_gas == gas)]
    is_kilo = by_gas_and_country.is_kilo[by_gas_and_country.index[0]]
    del by_gas_and_country["country"]
    del by_gas_and_country["greenhouse_gas"]
    del by_gas_and_country["category"]
    del by_gas_and_country["is_kilo"]
    time_series = by_gas_and_country.sum()
    time_series = time_series[time_series != 0.0]

    if fig is None:
        plt.figure(layout="constrained")
    plt.plot(time_series.index, time_series / 1e6)
    plt.xlabel("year")
    plt.ylabel(f"emission [million {'k' if is_kilo else ''} t / yr]")
    plt.xticks(rotation=60)
    plt.title(f"{country_code} {gas} emissions")


def global_emissions(gas="CO2"):
    by_gas = d[d.greenhouse_gas == gas]
    print(by_gas)
    is_kilo = by_gas.is_kilo[by_gas.index[0]]
    del by_gas["country"]
    del by_gas["greenhouse_gas"]
    del by_gas["category"]
    del by_gas["is_kilo"]
    time_series = by_gas.sum()
    time_series = time_series[4:]

    plt.figure(layout="constrained")
    plt.plot(time_series.index, time_series / 1e6)
    plt.xlabel("year")
    plt.ylabel(f"emission [million {'k' if is_kilo else ''} t / yr]")
    plt.xticks(rotation=60)
    plt.title(f"global {gas} emissions")
