import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize


def get_data(dpa_values_traps, T_values_traps, dpa_values_inv, T_values_inv):
    # ##### trap saturation evaluation ##### #

    k_B = 8.617333e-05
    fpy = 86400 * 365
    A_0 = 6.1838e-03
    E_A = 0.2792
    n_0 = 0

    t = np.geomspace(1e01, 1e09, int(1e04))

    trap_densities = []

    for T in T_values_traps:
        traps_per_T = []
        for dpa in dpa_values_traps:
            phi = dpa / fpy

            def numerical_trap_creation_model_trap_1(
                n, t, phi=phi, A_0=A_0, E_A=E_A, T=T
            ):
                K = 1.5e28
                n_max = 5.2e25
                dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n
                return dndt

            trap_1 = odeint(
                numerical_trap_creation_model_trap_1,
                n_0,
                t,
            )
            traps_per_T.append(trap_1)
        trap_densities.append(traps_per_T)

    normalised_traps = []
    for T_case in trap_densities:
        normalised_traps_per_T = []
        for dpa_case in T_case:
            norm_values = dpa_case / dpa_case[-1]
            normalised_traps_per_T.append(norm_values)
        normalised_traps.append(normalised_traps_per_T)

    saturation_time_traps = []
    for T_case in normalised_traps:
        char_times_per_T = []
        for dpa_case in T_case:
            char_time = np.where(dpa_case > 0.99)
            first = char_time[0][0]
            char_times_per_T.append(t[first])
        saturation_time_traps.append(char_times_per_T)

    np.savetxt("saturation_times_traps.txt", saturation_time_traps)

    inventories = []
    inventories_steady = []
    ts = []

    results_folder = "../parametric_studies/case_1e09s/"
    steady_results_folder = "../parametric_studies/case_steady/"

    for T in T_values_inv:
        invs_per_T = []
        ts_per_T = []
        steady_invs_per_T = []
        for dpa in dpa_values_inv:
            data_file = (
                results_folder
                + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
            )
            steady_data_file = (
                steady_results_folder
                + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
            )
            data = np.genfromtxt(data_file, delimiter=",", names=True)
            steady_data = np.genfromtxt(steady_data_file, delimiter=",", names=True)
            invs_per_T.append(data["Total_retention_volume_1"])
            steady_invs_per_T.append(steady_data["Total_retention_volume_1"])
            ts_per_T.append(data["ts"])
        inventories.append(invs_per_T)
        inventories_steady.append(steady_invs_per_T)
        ts.append(ts_per_T)

    normalised_inventories = []
    for T_case, T_case_steady in zip(inventories, inventories_steady):
        normalised_invs_per_T = []
        for dpa_case, dpa_case_steady in zip(T_case, T_case_steady):
            norm_values = dpa_case / dpa_case_steady
            # norm_values = dpa_case / dpa_case[-1]
            normalised_invs_per_T.append(norm_values)
        normalised_inventories.append(normalised_invs_per_T)

    characteristic_times = []
    for T_case, T_t in zip(normalised_inventories, ts):
        char_times_per_T = []
        for dpa_case, t in zip(T_case, T_t):
            char_time = np.where(dpa_case > 0.95)
            # char_time = np.where(dpa_case > 0.99)
            first = char_time[0][0]
            char_times_per_T.append(t[first])
        characteristic_times.append(char_times_per_T)

    np.savetxt("characteristic_times_invs.txt", characteristic_times)


dpa_values_traps = np.geomspace(1e-03, 1e04, num=50)
T_values_traps = np.linspace(1300, 400, num=20)

dpa_values_inv = np.geomspace(1e-03, 1e03, num=50)
T_values_inv = np.linspace(1300, 400, num=50)
T_values_inv = T_values_inv[:34]

# get_data(
#     dpa_values_traps=dpa_values_traps,
#     T_values_traps=T_values_traps,
#     dpa_values_inv=dpa_values_inv,
#     T_values_inv=T_values_inv,
# )

saturation_time_traps = np.loadtxt("../saturation_times_traps.txt")
characteristic_times = np.loadtxt("../characteristic_times_invs.txt")

# ##### Plotting ##### #

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

norm = Normalize(vmin=min(T_values_traps), vmax=max(T_values_traps))
colorbar = cm.inferno
sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

colours_traps = [colorbar(norm(T)) for T in T_values_traps]
colours_invs = [colorbar(norm(T)) for T in T_values_inv]

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=([6.4, 9.6]))

day = 3600 * 24
month = day * 31
year = day * 365.25

for T, sat_times, colour in zip(T_values_traps, saturation_time_traps, colours_traps):
    axs[0].plot(dpa_values_traps, sat_times, color=colour)

axs[0].set_xscale("log")
axs[0].set_yscale("log")
axs[0].set_ylabel(r"Trap density saturation time (s)")
axs[0].spines["top"].set_visible(False)
axs[0].spines["right"].set_visible(False)
axs[0].set_xlim(1e-03, 1e03)
axs[0].set_ylim(1e03, 1e07)

axs[0].vlines(5, 1e03, 1e09, color="black", alpha=0.5, linestyle="dashed")
axs[0].vlines(20, 1e03, 1e09, color="black", alpha=0.5, linestyle="dashed")
axs[0].annotate("DEMO", [6e-01, 7.5e06], color="black", alpha=0.5)
axs[0].annotate("ARC", [2.5e1, 7.5e06], color="black", alpha=0.5)

# axs[0].hlines(day, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
# axs[0].hlines(month, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")

# axs[0].annotate("1 day", [2e03, day * 1.1], color="black", alpha=0.3)
# axs[0].annotate("1 month", [2e03, month * 1.1], color="black", alpha=0.3)

# plt.colorbar(sm, label=r"Temperature (K)", ax=axs[0])

##########################


for T, char_times, colour in zip(T_values_inv, characteristic_times, colours_invs):
    axs[1].plot(dpa_values_inv, char_times, color=colour)

axs[1].set_xscale("log")
axs[1].set_yscale("log")
axs[1].spines["top"].set_visible(False)
axs[1].spines["right"].set_visible(False)
axs[1].set_ylabel(r"T retention saturation time (s)")
axs[1].set_xlabel(r"Damage rate (dpa/fpy)")

axs[1].set_xlim(1e-03, 1e03)
axs[1].set_ylim(1e03, 1e09)

# plt.colorbar(sm, label=r"Temperature (K)", ax=axs[1])

# axs[1].hlines(day, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
# axs[1].hlines(month, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
axs[1].hlines(year, 1e-03, 5e04, color="black", alpha=0.5, linestyle="dotted")
# axs[1].hlines(year * 10, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")

axs[1].vlines(5, 1e03, 1e09, color="black", alpha=0.5, linestyle="dashed")
axs[1].vlines(20, 1e03, 1e09, color="black", alpha=0.5, linestyle="dashed")

# axs[1].annotate("1 day", [2e03, day * 1.1], color="black", alpha=0.3)
# axs[1].annotate("1 month", [2e03, month * 1.1], color="black", alpha=0.3)
axs[1].annotate("1 FPY", [1.5e-03, year * 1.1], color="black", alpha=0.5)
# axs[1].annotate("10 years", [2e03, year * 10 * 1.1], color="black", alpha=0.3)

plt.tight_layout()

fig.colorbar(sm, label=r"Temperature (K)", ax=axs, aspect=40)

plt.show()
