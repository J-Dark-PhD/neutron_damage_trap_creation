import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import LogNorm


plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

area = 12e-03 * 15e-03

tds_dpa_0 = "tds_data/0_dpa.csv"
tds_dpa_0_001 = "tds_data/0.001_dpa.csv"
tds_dpa_0_005 = "tds_data/0.005_dpa.csv"
tds_dpa_0_023 = "tds_data/0.023_dpa.csv"
tds_dpa_0_1 = "tds_data/0.1_dpa.csv"
tds_dpa_0_23 = "tds_data/0.23_dpa.csv"
tds_dpa_0_5 = "tds_data/0.5_dpa.csv"
tds_dpa_2_5 = "tds_data/2.5_dpa.csv"

data_0 = np.genfromtxt(tds_dpa_0, delimiter=",", dtype=float)
T_0 = data_0[:, 0]
flux_0 = data_0[:, 1] / area

data_0_001 = np.genfromtxt(tds_dpa_0_001, delimiter=",", dtype=float)
T_0_001 = data_0_001[:, 0]
flux_0_001 = data_0_001[:, 1] / area

data_0_005 = np.genfromtxt(tds_dpa_0_005, delimiter=",", dtype=float)
T_0_005 = data_0_005[:, 0]
flux_0_005 = data_0_005[:, 1] / area

data_0_023 = np.genfromtxt(tds_dpa_0_023, delimiter=",", dtype=float)
T_0_023 = data_0_023[:, 0]
flux_0_023 = data_0_023[:, 1] / area

data_0_1 = np.genfromtxt(tds_dpa_0_1, delimiter=",", dtype=float)
T_0_1 = data_0_1[:, 0]
flux_0_1 = data_0_1[:, 1] / area

data_0_23 = np.genfromtxt(tds_dpa_0_23, delimiter=",", dtype=float)
T_0_23 = data_0_23[:, 0]
flux_0_23 = data_0_23[:, 1] / area

data_0_5 = np.genfromtxt(tds_dpa_0_5, delimiter=",", dtype=float)
T_0_5 = data_0_5[:, 0]
flux_0_5 = data_0_5[:, 1] / area


data_2_5 = np.genfromtxt(tds_dpa_2_5, delimiter=",", dtype=float)
T_2_5 = data_2_5[:, 0]
flux_2_5 = data_2_5[:, 1] / area

dpa_values = [0.001, 0.005, 0.023, 0.1, 0.23, 0.5, 2.5]
norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
colorbar = cm.viridis
sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

colours = [colorbar(norm(dpa)) for dpa in dpa_values]

T_data = [T_0_001, T_0_005, T_0_023, T_0_1, T_0_23, T_0_5, T_2_5]
flux_data = [
    flux_0_001,
    flux_0_005,
    flux_0_023,
    flux_0_1,
    flux_0_23,
    flux_0_5,
    flux_2_5,
]

T_data = np.flip(T_data, 0)
flux_data = np.flip(flux_data, 0)
dpa_values = np.flip(dpa_values, 0)
colours = np.flip(colours, 0)


def plot_TDS_data():

    plt.figure(figsize=(6.4, 5.5))
    for T_value, flux_value, colour in zip(T_data, flux_data, colours):
        plt.plot(T_value, flux_value, color=colour, linewidth=3)

    plt.plot(T_0, flux_0, label=r"0 dpa", linewidth=3, color="black")

    plt.xlim(300, 1000)
    plt.ylim(0, 1e17)
    plt.xlabel(r"Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.legend()
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    plt.colorbar(sm, label=r"Damage (dpa)")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


plot_TDS_data()

plt.show()
