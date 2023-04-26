import matplotlib.pyplot as plt
import numpy as np

results_folder = "../analytical_model_testing/"
T_range = np.genfromtxt(results_folder + "T_range.csv", delimiter=",")
trap_1_filling_ratios = np.genfromtxt(
    results_folder + "trap_1_filling_ratios.csv", delimiter=","
)
trap_d1_filling_ratios = np.genfromtxt(
    results_folder + "trap_d1_filling_ratios.csv", delimiter=","
)
trap_d2_filling_ratios = np.genfromtxt(
    results_folder + "trap_d2_filling_ratios.csv", delimiter=","
)
trap_d3_filling_ratios = np.genfromtxt(
    results_folder + "trap_d3_filling_ratios.csv", delimiter=","
)
trap_d4_filling_ratios = np.genfromtxt(
    results_folder + "trap_d4_filling_ratios.csv", delimiter=","
)


plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
plt.plot(T_range, trap_1_filling_ratios, label="Trap 1 (1.00 eV)")
plt.plot(T_range, trap_d1_filling_ratios, label="Trap D1 (1.15 eV)")
plt.plot(T_range, trap_d2_filling_ratios, label="Trap D2 (1.35 eV)")
plt.plot(T_range, trap_d3_filling_ratios, label="Trap D3 (1.65 eV)")
plt.plot(T_range, trap_d4_filling_ratios, label="Trap D4 (1.85 eV)")
plt.ylabel(r"Filling ratio")
plt.xlabel(r"Temperature (K)")
plt.xlim(400, 1300)
plt.ylim(0, 1)
plt.legend()
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()
