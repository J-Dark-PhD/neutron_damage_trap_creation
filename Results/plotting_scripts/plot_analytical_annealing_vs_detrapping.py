import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

results_folder = "../analytical_model_testing/"
T_range = np.genfromtxt(results_folder + "T_range.csv", delimiter=",")
trap_d1_detrapping_rates = np.genfromtxt(
    results_folder + "trap_d1_detrapping_rates.csv", delimiter=","
)
trap_d2_detrapping_rates = np.genfromtxt(
    results_folder + "trap_d2_detrapping_rates.csv", delimiter=","
)
trap_d3_detrapping_rates = np.genfromtxt(
    results_folder + "trap_d3_detrapping_rates.csv", delimiter=","
)
trap_d4_detrapping_rates = np.genfromtxt(
    results_folder + "trap_d4_detrapping_rates.csv", delimiter=","
)
annealing_rates = np.genfromtxt(results_folder + "annealing_rates.csv", delimiter=",")

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
plt.plot(T_range, trap_d1_detrapping_rates, color="blue", alpha=0.3)
plt.plot(T_range, trap_d2_detrapping_rates, color="blue", alpha=0.5)
plt.plot(T_range, trap_d3_detrapping_rates, color="blue", alpha=0.7)
plt.plot(
    T_range,
    trap_d4_detrapping_rates,
    color="blue",
    alpha=0.9,
    label="De-trapping",
)
plt.plot(T_range, annealing_rates, color="black", label="Annealing")

plt.annotate("1.15 eV", (1310, trap_d1_detrapping_rates[-1] * 1.1), color="black")
plt.annotate("1.35 eV", (1310, trap_d2_detrapping_rates[-1] * 0.6), color="black")
plt.annotate("1.65 eV", (1310, trap_d3_detrapping_rates[-1] * 0.7), color="black")
plt.annotate("1.85 eV", (1310, trap_d4_detrapping_rates[-1] * 0.5), color="black")

plt.yscale("log")
plt.legend()
plt.xlim(400, 1400)
plt.ylabel(r"Trapped tritium removal rate (s$^{-1}$)")
plt.xlabel(r"Temperature (K)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()
