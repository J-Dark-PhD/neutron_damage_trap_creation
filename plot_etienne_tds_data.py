import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)

tds_no_annealing = "tds_data/no_annealing.csv"
tds_800K = "tds_data/800K.csv"
tds_1200K = "tds_data/1200K.csv"

data_no_annealing = np.genfromtxt(tds_no_annealing, delimiter=",")
data_800K = np.genfromtxt(tds_800K, delimiter=",")
data_1200K = np.genfromtxt(tds_1200K, delimiter=",")

T_no_annealing = data_no_annealing[:, 0]
T_800K = data_800K[:, 0]
T_1200K = data_1200K[:, 0]

flux_no_annealing = data_no_annealing[:, 1]
flux_800K = data_800K[:, 1]
flux_1200K = data_1200K[:, 1]


plt.figure()
plt.scatter(
    T_no_annealing, flux_no_annealing, label="Exp. No Annealing", color=green_ryb
)
plt.scatter(T_800K, flux_800K, label="Exp. 800K", color=firebrick)
plt.scatter(T_1200K, flux_1200K, label="Exp. 1200K", color=pewter_blue)
plt.legend()
plt.ylabel(r"Desorption rate (D m$^{-2}$ s$^{-1}$)")
plt.xlabel(r"Temperature (K)")
plt.ylim(0, 7e17)
plt.xlim(500, 1200)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()
