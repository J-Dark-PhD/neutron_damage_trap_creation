import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import cm
from matplotlib.colors import LogNorm
import numpy as np
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2dir = os.path.dirname(parentdir)
sys.path.insert(0, parent2dir)

from analytical_model import (
    inventory_variation_with_damage_and_temperature,
)

T_range = np.linspace(400, 1300, num=50)
dpa_range = np.geomspace(1e-5, 1e03, num=10)
T_range_contour = np.linspace(400, 1300, num=100)
dpa_range_contour = np.geomspace(1e-3, 1e03, num=100)

(
    inventories,
    inventories_no_damage,
    inventories_normalised,
    inventories_standard_temp,
    inventories_standard_temp_normalised,
    inventories_contour,
    inventories_normalised_contour,
) = inventory_variation_with_damage_and_temperature(
    T_range, dpa_range, T_range_contour, dpa_range_contour
)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


def plot_inventory_varying_damage_standard_temperature():
    plt.figure()
    plot_dpa_range = dpa_range_contour / (3600 * 24 * 365.25)
    plt.plot(dpa_range, inventories_standard_temp, color="black", label="761 K")
    # plt.plot(plot_dpa_range, inventories_standard_temp, color="black", label="761 K")
    plt.ylabel(r"T inventory (m$^{-2}$)")
    plt.xlabel(r"Damage rate (dpa/fpy)")
    # plt.xlabel(r"Damage rate (dpa/s)")
    # plt.xlim(plot_dpa_range[0], plot_dpa_range[-1])
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_normalised_inventory_varying_temperature_standard_dpa():
    plt.figure()
    plt.plot(
        dpa_range,
        inventories_standard_temp_normalised,
        color="black",
        label="761 K",
    )
    plt.ylabel(r"T inventory (m$^{-3}$)")
    plt.xlabel(r"Damage rate (dpa/fpy)")
    plt.xlim(0, 10)
    plt.ylim(1, 1e05)
    plt.yscale("log")
    plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_inventory_varying_temperature_and_damage():
    max_dpa_case = inventories_standard_temp[-1] / inventories_standard_temp[0]

    print("At standard temperature of 761 K")
    print(
        "{:.0f} dpa/fpy case = factor {:.0f} increase".format(
            dpa_range[-1], max_dpa_case
        )
    )

    plt.figure()
    for inv, dpa in zip(inventories, dpa_range):
        plt.plot(T_range, inv, label="{} dpa/fpy".format(dpa))
    plt.ylabel(r"T inventory (m$^{-3}$)")
    plt.xlabel(r"Temperature (K)")
    plt.xlim(400, 1300)
    plt.ylim(1e16, 1e24)
    plt.yscale("log")
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(
        [h[6], h[5], h[4], h[3], h[2], h[1], h[0]],
        [l[6], l[5], l[4], l[3], l[2], l[1], l[0]],
        loc="upper right",
    )
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_inventory_varying_temperature_and_damage_expanded():
    fpy = 3600 * 24 * 365
    plot_dpa_range = dpa_range / fpy
    norm = LogNorm(vmin=min(plot_dpa_range), vmax=max(plot_dpa_range))
    # colorbar = cm.viridis(np.linspace(0, 1, 200))
    # needed to avoidhaving white lines
    # colorbar = ListedColormap(colorbar[50:, :-1])
    colorbar = cm.viridis
    # https://stackoverflow.com/questions/51034408/how-to-make-the-color-of-one-end-of-colorbar-darker-in-matplotlib
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in plot_dpa_range]

    plt.figure()
    for inv, dpa, colour in zip(inventories, plot_dpa_range, colours):
        plt.plot(T_range, inv, label="{} dpa/fpy".format(dpa), color=colour)
    plt.ylabel(r"T inventory (m$^{-3}$)")
    plt.xlabel(r"Temperature (K)")
    plt.xlim(400, 1300)
    plt.ylim(1e16, 1e24)
    plt.yscale("log")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    cb = plt.colorbar(sm, label=r"Damage rate (dpa s$^{-1}$)")


def plot_normalised_inventory_varying_temperature_and_damage():
    print(
        "Max inventory difference at {:.0f} dpa/fpy = {:.0f}".format(
            dpa_range[-1], np.max(inventories_normalised)
        )
    )
    plt.figure()
    for inv, dpa in zip(inventories_normalised, dpa_range):
        plt.plot(T_range, inv, label="{} dpa/fpy".format(dpa))

    plt.ylabel(r"Normalised inventory")
    plt.xlabel(r"Temperature (K)")
    plt.xlim(400, 1300)
    plt.yscale("log")
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(
        [h[5], h[4], h[3], h[2], h[1], h[0]],
        [l[5], l[4], l[3], l[2], l[1], l[0]],
        loc="upper right",
    )
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_inventory_contour(dpa_range_contour):
    dpa_range_contour = np.array(dpa_range_contour / (24 * 3600 * 365.25))
    X, Y = np.meshgrid(T_range_contour, dpa_range_contour)

    fig, ax = plt.subplots()
    CS = ax.contourf(
        X,
        Y,
        inventories_contour,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.colorbar(CS, label=r"T Inventory (m$^{-2}$)", format="%.0e ")
    plt.yscale("log")
    plt.ylabel(r"Damage rate (dpa s$^{-1}$)")
    plt.xlabel(r"Temperature (K)")
    plt.tight_layout()

    # ##### normalised to 0 dpa ##### #

    fig, ax = plt.subplots()
    CS = ax.contourf(
        X,
        Y,
        inventories_normalised_contour,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.colorbar(
        CS,
        label=r"Normalised T Inventory (inv/inv$_{0 \ \mathrm{dpa}}$)",
        format="%.0e ",
    )
    plt.yscale("log")
    plt.ylabel(r"Damage rate (dpa s$^{-1}$)")
    plt.xlabel(r"Temperature (K)")
    plt.tight_layout()


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


plot_inventory_varying_damage_standard_temperature()
plot_normalised_inventory_varying_temperature_standard_dpa()
plot_inventory_varying_temperature_and_damage()
plot_inventory_varying_temperature_and_damage_expanded()
plot_normalised_inventory_varying_temperature_and_damage()
plot_inventory_contour(dpa_range_contour)
plot_inventory_variation_and_normalised(dpa_range_contour)

plt.show()
