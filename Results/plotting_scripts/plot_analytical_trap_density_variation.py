import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2dir = os.path.dirname(parentdir)
sys.path.insert(0, parent2dir)

from analytical_model import trap_density_variation_with_damage_and_temperature

T_range = np.linspace(400, 1300, num=1000)
dpa_range = np.geomspace(1e-5, 1e03, num=1000)
T_range_contour = np.linspace(400, 1300, num=100)
dpa_range_contour = np.geomspace(1e-3, 1e03, num=100)
(
    trap_d1_densities,
    trap_d2_densities,
    trap_d3_densities,
    trap_d4_densities,
    trap_densities_by_T,
    trap_d1_densities_by_T,
    trap_d2_densities_by_T,
    trap_d3_densities_by_T,
    trap_d4_densities_by_T,
    trap_d1_densities_by_dpa,
    trap_d2_densities_by_dpa,
    trap_d3_densities_by_dpa,
    trap_d4_densities_by_dpa,
    trap_d1_densities_contour,
    trap_d2_densities_contour,
    trap_d3_densities_contour,
    trap_d4_densities_contour,
    trap_d1_densities_contour_normalised,
    trap_d2_densities_contour_normalised,
    trap_d3_densities_contour_normalised,
    trap_d4_densities_contour_normalised,
) = trap_density_variation_with_damage_and_temperature(
    T_range, dpa_range, T_range_contour, dpa_range_contour
)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)


def plot_trap_density_standard_damage_varying_temperature():
    plt.figure()
    plt.plot(
        T_range, trap_d1_densities_by_T, label="Trap D1 (1.15 eV)", color=firebrick
    )
    plt.plot(
        T_range, trap_d2_densities_by_T, label="Trap D2 (1.35 eV)", color=pewter_blue
    )
    plt.plot(
        T_range, trap_d3_densities_by_T, label="Trap D3 (1.65 eV)", color=electric_blue
    )
    plt.plot(
        T_range, trap_d4_densities_by_T, label="Trap D4 (1.85 eV)", color=green_ryb
    )
    plt.ylabel(r"Trap concentraion (m$^{-3}$)")
    plt.xlabel(r"Temperature (T)")
    plt.xlim(400, 1300)
    plt.ylim(1e23, 1e26)
    plt.yscale("log")
    # plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_trap_density_standard_temperature_varying_damage():
    # fpy = 3600 * 24 * 365.25
    # alt_dpa_range_seconds = alt_dpa_range / fpy

    plt.figure()
    plt.plot(
        dpa_range,
        trap_d1_densities_by_dpa,
        label="Trap D1 (1.15 eV)",
        color=firebrick,
    )
    plt.plot(
        dpa_range,
        trap_d2_densities_by_dpa,
        label="Trap D2 (1.35 eV)",
        color=pewter_blue,
    )
    plt.plot(
        dpa_range,
        trap_d3_densities_by_dpa,
        label="Trap D3 (1.65 eV)",
        color=electric_blue,
    )
    plt.plot(
        dpa_range,
        trap_d4_densities_by_dpa,
        label="Trap D4 (1.85 eV)",
        color=green_ryb,
    )
    plt.ylabel(r"Trap concentraion (m$^{-3}$)")
    plt.xlabel(r"Damage rate (dpa/fpy)")
    # alt_alt_dpa_range = alt_dpa_range / fpy
    plt.xlim(dpa_range[0], dpa_range[-1])
    plt.ylim(1e23, 1e26)
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_trap_variation_paper():
    fig, axs = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=([12, 4.8]))
    # variation with temp
    axs[0].plot(
        T_range, trap_d1_densities_by_T, label="Trap D1 (1.15 eV)", color=firebrick
    )
    axs[0].plot(
        T_range, trap_d2_densities_by_T, label="Trap D2 (1.35 eV)", color=pewter_blue
    )
    axs[0].plot(
        T_range, trap_d3_densities_by_T, label="Trap D3 (1.65 eV)", color=electric_blue
    )
    axs[0].plot(
        T_range, trap_d4_densities_by_T, label="Trap D4 (1.85 eV)", color=green_ryb
    )
    axs[0].set_ylabel(r"Trap density (m$^{-3}$)")
    axs[0].set_xlabel(r"Temperature (K)")
    axs[0].set_xlim(400, 1300)
    axs[0].set_ylim(1e23, 1e26)
    axs[0].set_yscale("log")
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["right"].set_visible(False)

    # damage variation
    axs[1].plot(
        dpa_range,
        trap_d1_densities_by_dpa,
        label="Trap D1 (1.15 eV)",
        color=firebrick,
    )
    axs[1].plot(
        dpa_range,
        trap_d2_densities_by_dpa,
        label="Trap D2 (1.35 eV)",
        color=pewter_blue,
    )
    axs[1].plot(
        dpa_range,
        trap_d3_densities_by_dpa,
        label="Trap D3 (1.65 eV)",
        color=electric_blue,
    )
    axs[1].plot(
        dpa_range,
        trap_d4_densities_by_dpa,
        label="Trap D4 (1.85 eV)",
        color=green_ryb,
    )
    axs[1].set_xlabel(r"Damage rate (dpa/fpy)")
    axs[1].set_xlim(dpa_range[0], dpa_range[-1])
    axs[1].set_ylim(1e23, 1e26)
    axs[1].set_yscale("log")
    axs[1].set_xscale("log")
    plt.legend()
    axs[1].spines["top"].set_visible(False)
    axs[1].spines["right"].set_visible(False)

    # plt.subplots_adjust(wspace=0.4)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.15)

    plt.figure()
    plt.plot(
        dpa_range,
        trap_d1_densities_by_dpa,
        label=r"Trap D1",
        color=firebrick,
    )
    plt.plot(
        dpa_range,
        trap_d2_densities_by_dpa,
        label=r"Trap D2",
        color=pewter_blue,
    )
    plt.plot(
        dpa_range,
        trap_d3_densities_by_dpa,
        label=r"Trap D3",
        color=electric_blue,
    )
    plt.plot(
        dpa_range,
        trap_d4_densities_by_dpa,
        label=r"Trap D4",
        color=green_ryb,
    )
    plt.xlabel(r"Damage rate (dpa/fpy)")
    plt.ylabel(r"Trap density (m$^{-3}$)")
    plt.xlim(dpa_range[0], dpa_range[-1])
    plt.ylim(1e23, 1e26)
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
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
        trap_d4_densities_contour_normalised,
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
        trap_d1_densities_contour,
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
        trap_d2_densities_contour,
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
        trap_d3_densities_contour,
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
        trap_d4_densities_contour,
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
        trap_d1_densities_contour_normalised,
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
        trap_d2_densities_contour_normalised,
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
        trap_d3_densities_contour_normalised,
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
        trap_d4_densities_contour_normalised,
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


plot_trap_variation_paper()
plot_trap_density_standard_damage_varying_temperature()
plot_trap_density_standard_temperature_varying_damage()
plot_varying_trap_6_temp_and_damage(dpa_range_contour)
plot_varying_all_traps_temp_and_damage(dpa_range_contour)
plot_varying_all_traps_temp_and_damage_normalised(dpa_range_contour)

plt.show()
