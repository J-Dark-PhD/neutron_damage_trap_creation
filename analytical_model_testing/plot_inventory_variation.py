import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import LogNorm, ListedColormap
import numpy as np
from analytical_model_testing import (
    alt_dpa_range,
    inventories_standard_temp,
    inventories_standard_temp_normalised,
    dpa_range,
    dpa_range_contour,
    inventories,
    inventories_normalised,
    T_range,
    T_range_contour,
    inventories_contour,
    normalised_inventories_contour,
    inventories_alt,
    test_dpa_range,
    testing_T_range,
)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


def plot_inventory_varying_damage_standard_temperature():
    plt.figure()
    plot_dpa_range = alt_dpa_range / (3600 * 24 * 365.25)
    plt.plot(alt_dpa_range, inventories_standard_temp, color="black", label="761 K")
    # plt.plot(plot_dpa_range, inventories_standard_temp, color="black", label="761 K")
    plt.ylabel(r"T inventory (m$^{-3}$)")
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
        alt_dpa_range,
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
    plot_dpa_range = test_dpa_range / fpy
    norm = LogNorm(vmin=min(plot_dpa_range), vmax=max(plot_dpa_range))
    # colorbar = cm.viridis(np.linspace(0, 1, 200))
    # needed to avoidhaving white lines
    # colorbar = ListedColormap(colorbar[50:, :-1])
    colorbar = cm.viridis
    # https://stackoverflow.com/questions/51034408/how-to-make-the-color-of-one-end-of-colorbar-darker-in-matplotlib
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in plot_dpa_range]

    plt.figure()
    for inv, dpa, colour in zip(inventories_alt, plot_dpa_range, colours):
        plt.plot(testing_T_range, inv, label="{} dpa/fpy".format(dpa), color=colour)
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
    plt.colorbar(CS, label=r"T Inventory (m$^{-3}$)", format="%.0e ")
    plt.yscale("log")
    plt.ylabel(r"Damage rate (dpa s$^{-1}$)")
    plt.xlabel(r"Temperature (K)")
    plt.tight_layout()

    # ##### normalised to 0 dpa ##### #

    fig, ax = plt.subplots()
    CS = ax.contourf(
        X,
        Y,
        normalised_inventories_contour,
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


def plot_paper(dpa_range_contour):

    plot_dpa_range = test_dpa_range
    norm = LogNorm(vmin=min(plot_dpa_range), vmax=max(plot_dpa_range))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in plot_dpa_range]

    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, figsize=([13, 9.6]))
    # fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True)

    for inv, dpa, colour in zip(inventories_alt, plot_dpa_range, colours):
        axs[0, 0].plot(
            testing_T_range, inv, label="{} dpa/fpy".format(dpa), color=colour
        )
    axs[0, 0].set_ylabel(r"T inventory (m$^{-3}$)")
    axs[0, 0].set_xlim(400, 1300)
    axs[0, 0].set_ylim(1e16, 1e24)
    axs[0, 0].set_yscale("log")
    axs[0, 0].spines["top"].set_visible(False)
    axs[0, 0].spines["right"].set_visible(False)

    plt.colorbar(sm, label=r"Damage rate (dpa fpy$^{-1}$)", ax=axs[0, 0])

    dpa_range_contour = np.array(dpa_range_contour)
    X, Y = np.meshgrid(T_range_contour, dpa_range_contour)

    # ##### normalised to 0 dpa ##### #
    CS = axs[1, 0].contourf(
        X,
        Y,
        normalised_inventories_contour,
        norm=LogNorm(),
        levels=np.geomspace(
            np.min(normalised_inventories_contour),
            np.max(normalised_inventories_contour),
            num=1000,
        ),
        cmap="plasma",
    )
    for c in CS.collections:
        c.set_edgecolor("face")
    CS2 = axs[1, 0].contour(
        X,
        Y,
        normalised_inventories_contour,
        levels=[1e00, 1e01, 1e02, 1e03, 1e04],
        colors="black",
    )
    axs[1, 0].clabel(CS2, inline=True, fontsize=10, fmt="%.0e")

    plt.colorbar(
        CS,
        label=r"Normalised T retention (ret/ret$_{0 \ \mathrm{dpa}}$)",
        format="%.0e",
        ax=axs[1, 0],
    )

    axs[1, 0].set_yscale("log")
    axs[1, 0].set_ylabel(r"Damage rate (dpa fpy$^{-1}$)")
    axs[1, 0].set_xlabel(r"Temperature (K)")
    plt.tight_layout()


# plot_inventory_varying_damage_standard_temperature()
# plot_normalised_inventory_varying_temperature_standard_dpa()
# plot_inventory_varying_temperature_and_damage()
# plot_inventory_varying_temperature_and_damage_expanded()
# plot_normalised_inventory_varying_temperature_and_damage()
# plot_inventory_contour(dpa_range_contour)
plot_paper(dpa_range_contour)

plt.show()
