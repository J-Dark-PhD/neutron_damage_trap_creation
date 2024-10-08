import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# from analytical_model_testing import (
#     dpa_range_contour,
#     T_range_contour,
#     normalised_inventories_contour,
#     inventories,
#     dpa_range,
#     T_range,
#     inventories_no_damage,
# )
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2dir = os.path.dirname(parentdir)
sys.path.insert(0, parent2dir)

from analytical_model import (
    T_range,
    T_range_contour,
    dpa_range,
    dpa_range_contour,
    analytical_model,
    fpy,
)

inventories = []
inventories_no_damage = []
inventories_contour = []
inventories_no_damage_contour = []
inventories_normalised_contour = []

for dpa in dpa_range:
    phi = dpa / fpy
    (
        H_retention_standard_temp,
        trap_densities_standard_temp,
        trap_filling_ratios_standard_temp,
    ) = analytical_model(phi=phi, T=700)
    inventory_per_dpa = []
    inventories_no_damage = []
    for T in T_range:
        (
            H_retention,
            trap_densities,
            trap_fdrssstg4wsfilling_ratios,
        ) = analytical_model(phi=phi, T=T)
        (
            H_retention_no_damage,
            trap_densities_no_damage,
            trap_filling_ratios_no_damage,
        ) = analytical_model(phi=phi, T=T)
        inventory_per_dpa.append(H_retention)
        inventories_no_damage.append(H_retention_no_damage)
    inventories.append(inventory_per_dpa)

for dpa in dpa_range_contour:
    phi = dpa / fpy
    inventory_contour_per_dpa = []
    inventories_no_damage_contour = []
    for T in T_range_contour:
        (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
            phi=phi, T=T
        )
        (
            H_retention_no_damage,
            trap_densities_no_damage,
            trap_filling_ratios_no_damage,
        ) = analytical_model(phi=0, T=T)
        inventory_contour_per_dpa.append(H_retention)
        inventories_no_damage_contour.append(H_retention_no_damage)
    inventories_contour.append(inventory_contour_per_dpa)

for inv in inventories_standard_temp:
    normalised_values = np.array(inv) / np.array(inventories_standard_temp[0])
    inventories_standard_temp_normalised.append(normalised_values)

for case in inventories_contour:
    inventory = case / np.array(inventories_no_damage_contour)
    inventories_normalised_contour.append(inventory)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


def plot_inventory_variation_and_normalised(dpa_range_contour):
    plot_dpa_range = dpa_range
    norm = LogNorm(vmin=min(plot_dpa_range), vmax=max(plot_dpa_range))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in plot_dpa_range]

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=([6.4, 9.6]))

    for inv, colour in zip(inventories, colours):
        axs[0].plot(T_range, inv, color=colour)

    axs[0].plot(T_range, inventories_no_damage, label=r"undamaged", color="black")
    axs[0].set_ylabel(r"T inventory (m$^{-2}$)")
    axs[0].set_xlim(400, 1300)
    axs[0].set_ylim(1e16, 1e24)
    axs[0].set_yscale("log")
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["right"].set_visible(False)
    axs[0].legend()

    plt.colorbar(sm, label=r"Damage rate (dpa fpy$^{-1}$)", ax=axs[0])

    dpa_range_contour = np.array(dpa_range_contour)
    X, Y = np.meshgrid(T_range_contour, dpa_range_contour)

    # ##### normalised to 0 dpa ##### #
    CS = axs[1].contourf(
        X,
        Y,
        inventories_normalised_contour,
        norm=LogNorm(),
        levels=np.geomspace(
            np.min(inventories_normalised_contour),
            np.max(inventories_normalised_contour),
            num=1000,
        ),
        cmap="plasma",
    )
    for c in CS.collections:
        c.set_edgecolor("face")
    CS2 = axs[1].contour(
        X,
        Y,
        inventories_normalised_contour,
        levels=[1e00, 1e01, 1e02, 1e03, 1e04, 1e05],
        colors="black",
    )
    axs[1].clabel(CS2, inline=True, fontsize=10, fmt="%.0e")

    plt.colorbar(
        CS,
        label=r"Normalised T inventory (inv/inv$_{0 \ \mathrm{dpa}}$)",
        format="%.0e",
        ax=axs[1],
    )

    axs[1].set_yscale("log")
    axs[1].set_ylabel(r"Damage rate (dpa fpy$^{-1}$)")
    axs[1].set_xlabel(r"Temperature (K)")

    plt.tight_layout()


def plot_inventories_transient_and_distribution():
    dpa_values = np.geomspace(1e-05, 1e03, num=10)

    norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in dpa_values]

    results_folder = "../parametric_studies/case_1fpy/"
    # standard case
    standard_file = results_folder + "dpa=0/T=700/derived_quantities.csv"
    data = np.genfromtxt(standard_file, delimiter=",", names=True)
    inv_per_dpa = data["Total_retention_volume_1"]
    times = data["ts"]

    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=([6.4, 9.6]))
    axs[0].plot(times, inv_per_dpa, color="black", label=r"undamaged")

    for dpa, colour in zip(dpa_values, colours):
        data_file = results_folder + "dpa={:.2e}/T=700/derived_quantities.csv".format(
            dpa
        )
        data = np.genfromtxt(data_file, delimiter=",", names=True)
        inv_per_dpa = data["Total_retention_volume_1"]
        times = data["ts"]
        axs[0].plot(times, inv_per_dpa, color=colour)

    day = 3600 * 24
    axs[0].vlines(day, 1e15, 1e23, color="black", alpha=0.5, linestyle="dashed")
    axs[0].annotate("24h", [day * 1.2, 1e16], color="black", alpha=0.5)

    axs[0].set_ylabel(r"T inventory (m$^{-2}$)")
    axs[0].set_xlabel(r"Time (s)")
    axs[0].set_ylim(1e15, 1e23)
    axs[0].set_xlim(left=1e-01)
    axs[0].set_yscale("log")
    axs[0].set_xscale("log")
    axs[0].legend()
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["right"].set_visible(False)

    # ##### retention profile ##### #
    dpa_values = np.geomspace(1e-05, 1e03, num=9)
    norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
    sm = plt.cm.ScalarMappable(cmap=cm.viridis, norm=norm)
    colours = [colorbar(norm(dpa)) for dpa in dpa_values]

    results_folder = "../parametric_studies/profile_dist_24h/T=700K/profiles/"
    data_file = results_folder + "case_dpa=1e-01.csv"
    x_data = np.genfromtxt(data_file, delimiter=",", names=True)
    x_values = x_data["arc_length"]
    x_plot = x_values * 1000

    inventories = []
    for dpa in dpa_values:
        data_file = results_folder + "case_dpa={:.0e}.csv".format(dpa)
        data = np.genfromtxt(data_file, delimiter=",", names=True)
        inv = data["retention"]
        inventories.append(inv)

    for inv, dpa, colour in zip(inventories, dpa_values, colours):
        axs[1].plot(x_plot, inv, color=colour)
    axs[1].set_xlabel(r"x (mm)")
    axs[1].set_ylabel(r"T retention (T m$^{-3}$)")
    axs[1].set_xlim(0, 2)
    axs[1].set_yscale("log")
    axs[1].set_ylim(1e21, 1e26)
    axs[1].spines["right"].set_visible(False)
    axs[1].spines["top"].set_visible(False)

    plt.tight_layout()

    fig.colorbar(sm, label=r"Damage rate (dpa/fpy)", ax=axs, aspect=40)


# plot_inventory_variation_and_normalised(dpa_range_contour)
plot_inventories_transient_and_distribution()

plt.show()
