import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import csv

implantation_time = 72 * 3600
resting_time = 1 * 24 * 3600

T_sim = []
flux1, flux2 = [], []
total_flux = []
solute = []
ret = []
t = []
trap1 = []


data_sim = np.genfromtxt("Results/last.csv", delimiter=",", names=True)
t = data_sim["ts"]
solute = data_sim["Total_solute_volume_1"] / (12e-03 * 15e-03)

plt.plot(t, solute)
plt.scatter(t, solute)

# plt.xlim(300, 1000)
# plt.ylim(0, 1e16)
# plt.vlines(490, 0, 2e16, color="grey", linestyle="dashed")
# plt.vlines(540, 0, 2e16, color="grey", linestyle="dashed")
# plt.ylim(1e13, 1e18)
# plt.yscale("log")
plt.xlabel("T(K)")
plt.ylabel(r"Desorption flux (D/m$ ^{2}$/s)")
plt.title("TDS")
plt.legend()
plt.show()
