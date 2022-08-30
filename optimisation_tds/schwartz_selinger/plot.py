import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import csv

implantation_time = 72 * 3600
resting_time = 0.5 * 24 * 3600

tds_data_folder = "../../data/tds_data/"

tds_dpa_0 = "tds_data/0_dpa.csv"
tds_dpa_0_001 = "tds_data/0.001_dpa.csv"
tds_dpa_0_005 = "tds_data/0.005_dpa.csv"
tds_dpa_0_023 = "tds_data/0.023_dpa.csv"
tds_dpa_0_1 = "tds_data/0.1_dpa.csv"
tds_dpa_0_23 = "tds_data/0.23_dpa.csv"
tds_dpa_0_5 = "tds_data/0.5_dpa.csv"
tds_dpa_2_5 = "tds_data/2.5_dpa.csv"

data_0 = np.genfromtxt(tds_dpa_0, delimiter=",")
data_0_001 = np.genfromtxt(tds_dpa_0_001, delimiter=",")
data_0_005 = np.genfromtxt(tds_dpa_0_005, delimiter=",")
data_0_023 = np.genfromtxt(tds_dpa_0_023, delimiter=",")
data_0_1 = np.genfromtxt(tds_dpa_0_1, delimiter=",")
data_0_23 = np.genfromtxt(tds_dpa_0_23, delimiter=",")
data_0_5 = np.genfromtxt(tds_dpa_0_5, delimiter=",")
data_2_5 = np.genfromtxt(tds_dpa_2_5, delimiter=",")

T_0 = data_0[:, 0]
T_0_001 = data_0_001[:, 0]
T_0_005 = data_0_005[:, 0]
T_0_023 = data_0_023[:, 0]
T_0_1 = data_0_1[:, 0]
T_0_23 = data_0_23[:, 0]
T_0_5 = data_0_5[:, 0]
T_2_5 = data_2_5[:, 0]

area = 12e-03 * 15e-03

flux_0 = data_0[:, 1] / area
flux_0_001 = data_0_001[:, 1] / area
flux_0_005 = data_0_005[:, 1] / area
flux_0_023 = data_0_023[:, 1] / area
flux_0_1 = data_0_1[:, 1] / area
flux_0_23 = data_0_23[:, 1] / area
flux_0_5 = data_0_5[:, 1] / area
flux_2_5 = data_2_5[:, 1] / area

# plt.scatter(T_0, flux_0, label="0 dpa")
# plt.scatter(T_0_001, flux_0_001, label="0.001 dpa")
# plt.scatter(T_0_005, flux_0_005, label="0.005 dpa")
plt.scatter(T_0_023, flux_0_023, label="0.023 dpa")
# plt.scatter(T_0_1, flux_0_1, label="0.1 dpa")
# plt.scatter(T_0_23, flux_0_23, label="0.23 dpa", color="black")
# plt.scatter(T_0_5, flux_0_5, label="0.5 dpa", color="black")
# plt.scatter(T_2_5, flux_2_5, label="2.5 dpa", color="black")

# plt.axvspan(
#     460,
#     530,
#     color="tab:blue",
#     alpha=0.5,
# )
# plt.axvspan(
#     750,
#     800,
#     color="tab:blue",
#     alpha=0.5,
# )

T_sim = []
flux1, flux2 = [], []
total_flux = []
solute = []
ret = []
t = []
trap1 = []
trap2 = []
# trap3 = []


with open("Results/last.csv", "r") as csvfile:
    plots = csv.reader(csvfile, delimiter=",")
    for row in plots:
        if "t(s)" not in row:
            if float(row[0]) >= implantation_time + resting_time * 0.75:
                t.append(float(row[0]))
                T_sim.append(float(row[1]))
                flux1.append(float(row[2]))
                flux2.append(float(row[3]))
                solute.append(float(row[4]))
                ret.append(float(row[5]))
                trap1.append(float(row[6]))
                trap2.append(float(row[7]))


fields = [ret, solute, trap1, trap2]
derivatives = [[] for i in range(len(fields))]

legends = ["Total", "Solute", "Trap 1", "Trap 2"]
for i in range(len(ret) - 1):
    for j in range(0, len(derivatives)):
        derivatives[j].append(-(fields[j][i + 1] - fields[j][i]) / (t[i + 1] - t[i]))

plt.plot(T_sim, -np.asarray(flux1) - np.asarray(flux2))
# plt.plot(T_sim, -np.asarray(flux2), label="flux2")
T_sim.pop(0)
for i in range(0, len(derivatives)):
    if i != 0:
        style = "dashed"
        width = 0.8
        plt.fill_between(T_sim, 0, derivatives[i], facecolor="grey", alpha=0.1)
    else:
        style = "-"
        width = 1.7
    if i != 1:
        plt.plot(
            T_sim,
            derivatives[i],
            linewidth=width,
            linestyle=style,
            label=legends[i],
            alpha=1,
        )

# plt.xlim(300, 1000)
# plt.ylim(0, 1e16)
plt.ylim(bottom=0)
# plt.vlines(490, 0, 2e16, color="grey", linestyle="dashed")
# plt.vlines(540, 0, 2e16, color="grey", linestyle="dashed")
# plt.ylim(1e13, 1e18)
# plt.yscale("log")
plt.xlabel("T(K)")
plt.ylabel(r"Desorption flux (D/m$ ^{2}$/s)")
plt.title("TDS")
plt.legend()
plt.show()
