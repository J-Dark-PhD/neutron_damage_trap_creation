import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import csv

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)

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

# plt.scatter(T_0, flux_0, label="0 dpa", color="black")
# plt.scatter(T_0_001, flux_0_001, label="0.001 dpa")
# plt.scatter(T_0_005, flux_0_005, label="0.005 dpa")
# plt.scatter(T_0_023, flux_0_023, label="Exp. 0.023 dpa", color="black")
# plt.scatter(T_0_1, flux_0_1, label="0.1 dpa")
# plt.scatter(T_0_23, flux_0_23, label="0.23 dpa")
plt.scatter(T_0_5, flux_0_5, label="0.5 dpa")
# plt.scatter(T_2_5, flux_2_5, label="2.5 dpa")

T_sim = []
flux1, flux2 = [], []
total_flux = []
solute = []
ret = []
t = []
trap1 = []
trap2 = []
trap3 = []
trap4 = []
trap5 = []

# t_standard = []
# T_sim_standard = []
# flux1_standard, flux2_standard = [], []

# with open("Results/dpa_0.023/last.csv", "r") as csvfile:
#     plots = csv.reader(csvfile, delimiter=",")
#     for row in plots:
#         if "t(s)" not in row:
#             if float(row[0]) >= implantation_time + resting_time * 0.75:
#                 t_standard.append(float(row[0]))
#                 T_sim_standard.append(float(row[1]))
#                 flux1_standard.append(float(row[2]))
#                 flux2_standard.append(float(row[3]))


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
                trap3.append(float(row[8]))
                trap4.append(float(row[9]))
                trap5.append(float(row[10]))


trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1

solute_contrib = (np.diff(solute) / np.diff(t)) * -1

plt.plot(
    T_sim[1:],
    trap_1_contrib,
    linestyle="dashed",
    color=green_ryb,
    label=r"Trap 1 ($E_{t} = 1.00 eV$)",
)
plt.plot(
    T_sim[1:],
    trap_2_contrib,
    linestyle="dashed",
    color=firebrick,
    label=r"Trap 2 ($E_{t} = 1.15 eV$)",
)
# plt.plot(
#     T_sim[1:],
#     trap_3_contrib,
#     linestyle="dashed",
#     color=pewter_blue,
#     label=r"Trap 3 ($E_{t} = 1.30 eV$)",
# )
# plt.plot(
#     T_sim[1:],
#     trap_4_contrib,
#     linestyle="dashed",
#     color=blue_jeans,
#     label=r"Trap 4 ($E_{t} = 1.50 eV$)",
# )
# plt.plot(
#     T_sim[1:],
#     trap_5_contrib,
#     linestyle="dashed",
#     color=electric_blue,
#     label=r"Trap 5 ($E_{t} = 1.85 eV$)",
# )
plt.plot(
    T_sim[1:],
    trap_3_contrib,
    linestyle="dashed",
    color=blue_jeans,
    label=r"Trap 3 ($E_{t} = 1.40 eV$)",
)
plt.plot(
    T_sim[1:],
    trap_4_contrib,
    linestyle="dashed",
    color=electric_blue,
    label=r"Trap 4 ($E_{t} = 1.65 eV$)",
)
plt.plot(
    T_sim[1:],
    trap_5_contrib,
    linestyle="dashed",
    color=electric_blue,
    label=r"Trap 5 ($E_{t} = 1.85 eV$)",
)
plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

plt.plot(
    T_sim,
    -np.asarray(flux1) - np.asarray(flux2),
    label="Simulation",
    color="orange",
    linewidth=2,
)

# plt.plot(
#     T_sim_standard,
#     -np.asarray(flux1_standard) - np.asarray(flux2_standard),
#     label="Simulation standard",
#     color=pewter_blue,
#     linewidth=2,
# )

plt.xlim(300, 1000)
# plt.ylim(0, 5e16)
plt.ylim(bottom=0)
plt.xlabel("Temperature (K)")
plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
# plt.title("TDS")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.legend()
plt.tight_layout()

plt.show()
