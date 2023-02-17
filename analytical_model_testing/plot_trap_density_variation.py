import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
from analytical_model_testing import (
    green_ryb,
    firebrick,
    pewter_blue,
    blue_jeans,
    electric_blue,
    T_range,
    trap_1_densities_by_T,
    trap_2_densities_by_T,
    trap_3_densities_by_T,
    trap_4_densities_by_T,
    trap_5_densities_by_T,
    trap_6_densities_by_T,
    alt_dpa_range,
    trap_1_densities_standard_temp,
    trap_2_densities_standard_temp,
    trap_3_densities_standard_temp,
    trap_4_densities_standard_temp,
    trap_5_densities_standard_temp,
    trap_6_densities_standard_temp,
    total_trap_density,
    trap_density_values,
    dpa_range,
    dpa_range_contour,
    T_range_contour,
    trap_densities_contour_4_normalised,
    trap_densities_contour_1,
    trap_densities_contour_2,
    trap_densities_contour_3,
    trap_densities_contour_4,
    trap_densities_contour_1_normalised,
    trap_densities_contour_2_normalised,
    trap_densities_contour_3_normalised,
    trap_densities_contour_4_normalised,
)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

def plot_trap_density_variation_with_temperature_standard_damage():
    plt.figure()
    plt.plot(T_range, trap_1_densities_by_T, label="Trap 1 (0.87 eV)", color="black")
    plt.plot(T_range, trap_2_densities_by_T, label="Trap 2 (1.00 eV)", color="grey")
    plt.plot(T_range, trap_3_densities_by_T, label="Trap D1 (1.15 eV)", color=firebrick)
    plt.plot(
        T_range, trap_4_densities_by_T, label="Trap D2 (1.35 eV)", color=electric_blue
    )
    plt.plot(
        T_range, trap_5_densities_by_T, label="Trap D3 (1.65 eV)", color=pewter_blue
    )
    plt.plot(T_range, trap_6_densities_by_T, label="Trap D4 (1.85 eV)", color=green_ryb)
    plt.ylabel(r"Trap concentraion (m$^{-3}$)")
    plt.xlabel(r"Temperature (T)")
    plt.xlim(400, 1300)
    plt.ylim(1e24, 1e26)
    plt.yscale("log")
    # plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_trap_density_variation_with_damage_standard_temperature():
    fpy = 3600 * 24 * 365.25
    alt_dpa_range_seconds = alt_dpa_range / fpy

    plt.figure()
    plt.plot(
        alt_dpa_range_seconds,
        trap_1_densities_standard_temp,
        label="Trap 1 (0.87 eV)",
        color="black",
    )
    plt.plot(
        alt_dpa_range_seconds,
        trap_2_densities_standard_temp,
        label="Trap 2 (1.00 eV)",
        color="grey",
    )
    plt.plot(
        alt_dpa_range_seconds,
        trap_3_densities_standard_temp,
        label="Trap D1 (1.15 eV)",
        color=firebrick,
    )
    plt.plot(
        alt_dpa_range_seconds,
        trap_4_densities_standard_temp,
        label="Trap D2 (1.35 eV)",
        color=electric_blue,
    )
    plt.plot(
        alt_dpa_range_seconds,
        trap_5_densities_standard_temp,
        label="Trap D3 (1.65 eV)",
        color=pewter_blue,
    )
    plt.plot(
        alt_dpa_range_seconds,
        trap_6_densities_standard_temp,
        label="Trap D4 (1.85 eV)",
        color=green_ryb,
    )
    plt.ylabel(r"Trap concentraion (m$^{-3}$)")
    plt.xlabel(r"Damage rate (dpa/s)")
    alt_alt_dpa_range = alt_dpa_range / fpy
    plt.xlim(alt_alt_dpa_range[0], alt_alt_dpa_range[-1])
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_total_trap_density_variation_with_damage_standard_temperature():
    plt.figure()
    plt.plot(alt_dpa_range, total_trap_density, label="Total")
    plt.ylabel(r"Trap concentraion (m$^{-3}$)")
    plt.xlabel(r"Damage rate (dpa/fpy)")
    plt.xlim(alt_dpa_range[0], alt_dpa_range[-1])
    plt.xscale("log")
    plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_trap_6_density_varitation_with_temperature_and_damage():
    plt.figure()
    for trap_conc, dpa in zip(trap_density_values, dpa_range):
        plt.plot(T_range, trap_conc, label="{} dpa/fpy".format(dpa))
    plt.ylabel(r"Trap 6 (1.85 eV) concentraion (m$^{-3}$)")
    plt.xlabel(r"Temperature (T)")
    plt.xlim(400, 1300)
    plt.ylim(1e20, 1e26)
    plt.yscale("log")
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(
        [h[5], h[4], h[3], h[2], h[1]],
        [l[5], l[4], l[3], l[2], l[1]],
        loc="lower left",
    )
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_varying_trap_6_temp_and_damage(dpa_range_contour):

    dpa_range_contour = np.array(dpa_range_contour / (24 * 3600 * 365.25))
    X, Y = np.meshgrid(T_range_contour, dpa_range_contour)

    fig, ax = plt.subplots()
    CS = ax.contourf(
        X,
        Y,
        trap_densities_contour_4_normalised,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    # plt.colorbar(CS, label=r"Trap 6 (1.85 eV) concentration (m$^{-3}$)", format="%.0e ")
    plt.colorbar(
        CS,
        label=r"Trap 6 (1.85 eV) concentration ($\frac{n_{t}}{n_{max}}$)",
        format="%.0e ",
    )
    plt.yscale("log")
    plt.ylabel(r"Damage rate (dpa s$^{-1}$)")
    plt.xlabel(r"Temperature (K)")
    plt.tight_layout()


def plot_varying_all_traps_temp_and_damage(dpa_range_contour):

    dpa_range_contour = np.array(dpa_range_contour / (24 * 3600 * 365.25))
    X, Y = np.meshgrid(T_range_contour, dpa_range_contour)

    fig = plt.figure(figsize=(10, 8))

    # create one big plot to have common labels
    ax = fig.add_subplot(111)
    ax.spines["top"].set_color("none")
    ax.spines["bottom"].set_color("none")
    ax.spines["left"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.tick_params(labelcolor="w", top=False, bottom=False, left=False, right=False)
    ax.set_ylabel(r"Damage rate (dpa s$^{-1}$)")
    ax.yaxis.set_label_coords(-0.075, 0.5)
    ax.set_xlabel(r"Temperature (K)")
    ax.xaxis.set_label_coords(0.4, -0.075)

    # damaging trap 1
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.contourf(
        X,
        Y,
        trap_densities_contour_1,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.sca(ax1)
    plt.annotate("Trap 1 (1.15 eV)", (650, 7.5e-06), color="black")

    # damaging trap 2
    ax2 = fig.add_subplot(2, 2, 2)
    CS = ax2.contourf(
        X,
        Y,
        trap_densities_contour_2,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.sca(ax2)
    plt.annotate("Trap 2 (1.35 eV)", (650, 7.5e-06), color="black")

    # damaging trap 3
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.contourf(
        X,
        Y,
        trap_densities_contour_3,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.sca(ax3)
    plt.annotate("Trap 3 (1.65 eV)", (650, 7.5e-06), color="black")

    # damaging trap 4
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.contourf(
        X,
        Y,
        trap_densities_contour_4,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.sca(ax4)
    plt.annotate("Trap 4 (1.85 eV)", (650, 7.5e-06), color="black")

    for ax in [ax1, ax2, ax3, ax4]:
        plt.sca(ax)
        plt.yscale("log")
        # plt.ylim(1e-11, 1e-05)

    # remove the xticks for top plots and yticks for right plots
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax4.set_yticklabels([])

    plt.sca(ax)
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    plt.colorbar(
        CS,
        ax=[ax1, ax2, ax3, ax4],
        label=r"Trap concentration (m$^{-3}$)",
        format="%.0e",
    )


def plot_varying_all_traps_temp_and_damage_normalised(dpa_range_contour):

    dpa_range_contour = np.array(dpa_range_contour / (24 * 3600 * 365.25))
    X, Y = np.meshgrid(T_range_contour, dpa_range_contour)

    fig = plt.figure(figsize=(10, 8))

    # create one big plot to have common labels
    ax = fig.add_subplot(111)
    ax.spines["top"].set_color("none")
    ax.spines["bottom"].set_color("none")
    ax.spines["left"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.tick_params(labelcolor="w", top=False, bottom=False, left=False, right=False)
    ax.set_ylabel(r"Damage rate (dpa s$^{-1}$)")
    ax.yaxis.set_label_coords(-0.075, 0.5)
    ax.set_xlabel(r"Temperature (K)")
    ax.xaxis.set_label_coords(0.4, -0.075)

    # damaging trap 1
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.contourf(
        X,
        Y,
        trap_densities_contour_1_normalised,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.sca(ax1)
    plt.annotate("Trap 1 (1.15 eV)", (650, 7.5e-06), color="black")

    # damaging trap 2
    ax2 = fig.add_subplot(2, 2, 2)
    CS = ax2.contourf(
        X,
        Y,
        trap_densities_contour_2_normalised,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.sca(ax2)
    plt.annotate("Trap 2 (1.35 eV)", (650, 7.5e-06), color="black")

    # damaging trap 3
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.contourf(
        X,
        Y,
        trap_densities_contour_3_normalised,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.sca(ax3)
    plt.annotate("Trap 3 (1.65 eV)", (650, 7.5e-06), color="black")

    # damaging trap 4
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.contourf(
        X,
        Y,
        trap_densities_contour_4_normalised,
        levels=1000,
        cmap="viridis",
        locator=ticker.LogLocator(),
    )
    plt.sca(ax4)
    plt.annotate("Trap 4 (1.85 eV)", (650, 7.5e-06), color="black")

    for ax in [ax1, ax2, ax3, ax4]:
        plt.sca(ax)
        plt.yscale("log")

    # remove the xticks for top plots and yticks for right plots
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax4.set_yticklabels([])

    plt.sca(ax)
    plt.subplots_adjust(wspace=0.112, hspace=0.071)

    plt.colorbar(
        CS,
        ax=[ax1, ax2, ax3, ax4],
        label=r"$\frac{n_{t}}{n_{max}}$",
        format="%.0e",
    )


plot_trap_density_variation_with_temperature_standard_damage()
plot_trap_density_variation_with_damage_standard_temperature()
plot_total_trap_density_variation_with_damage_standard_temperature()
plot_trap_6_density_varitation_with_temperature_and_damage()
plot_varying_trap_6_temp_and_damage(dpa_range_contour)
plot_varying_all_traps_temp_and_damage(dpa_range_contour)
plot_varying_all_traps_temp_and_damage_normalised(dpa_range_contour)

plt.show()