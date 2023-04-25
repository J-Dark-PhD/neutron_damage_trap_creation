from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint

from neutron_trap_creation_models import (
    neutron_trap_creation_numerical,
    t_annealing,
    A_0_optimised,
    E_A_optimised,
    atom_density_W,
    temperatures,
    trap_1,
    trap_2,
    trap_3,
    T_list,
)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)

##############################################
# ############# All 3 data sets ############ #
##############################################

t = np.linspace(0, t_annealing, t_annealing)
phi = 0
K = 1
n_max = 1
A_0 = A_0_optimised
E_A = E_A_optimised

n_0_trap1 = trap_1[0] * atom_density_W * 1e-02
n_0_trap2 = trap_2[0] * atom_density_W * 1e-02
n_0_trap3 = trap_3[0] * atom_density_W * 1e-02

annealed_trap_1_densities = []
annealed_trap_2_densities = []
annealed_trap_3_densities = []

for T in T_list:
    extra_args = (phi, K, n_max, A_0, E_A, T)
    # trap 1
    n_traps_annleaing_trap_1 = odeint(
        neutron_trap_creation_numerical, n_0_trap1, t, args=extra_args
    )
    end_value_trap_1 = float(n_traps_annleaing_trap_1[-1])
    annealed_trap_1_densities.append(end_value_trap_1)

    # trap 2
    n_traps_annleaing_trap_2 = odeint(
        neutron_trap_creation_numerical, n_0_trap2, t, args=extra_args
    )
    end_value_trap_2 = float(n_traps_annleaing_trap_2[-1])
    annealed_trap_2_densities.append(end_value_trap_2)

    # trap 3
    n_traps_annleaing_trap_3 = odeint(
        neutron_trap_creation_numerical, n_0_trap3, t, args=extra_args
    )
    end_value_trap_3 = float(n_traps_annleaing_trap_3[-1])
    annealed_trap_3_densities.append(end_value_trap_3)

trap_1 = (np.array(trap_1) / 100) * 6.3e28
trap_2 = (np.array(trap_2) / 100) * 6.3e28
trap_3 = (np.array(trap_3) / 100) * 6.3e28

trap_1_err = np.array(trap_1) * 0.1
trap_2_err = np.array(trap_2) * 0.1
trap_3_err = np.array(trap_3) * 0.1
# annealed_trap_1_densities = (np.array(annealed_trap_1_densities) / 6.3e28) * 100
# annealed_trap_2_densities = (np.array(annealed_trap_2_densities) / 6.3e28) * 100
# annealed_trap_3_densities = (np.array(annealed_trap_3_densities) / 6.3e28) * 100

# ##### Seperate plots ##### #


def plot_1():
    plt.figure()
    err_bar_1 = plt.errorbar(
        temperatures,
        trap_1,
        yerr=trap_1_err,
        fmt=".",
        capsize=5,
        color=green_ryb,
    )
    plot_1 = plt.plot(
        T_list,
        annealed_trap_1_densities,
        color=green_ryb,
        label=r"Trap 3 ($E_{t} = 1.65$ eV)",
    )
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
    plt.xlabel(r"Annealing temperature (K)")
    plt.ylim(bottom=0)
    plt.xlim(0, 1400)
    plt.legend(loc="lower left")
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


def plot_2():
    plt.figure()
    err_bar_2 = plt.errorbar(
        temperatures,
        trap_2,
        yerr=trap_2_err,
        fmt=".",
        capsize=5,
        color=firebrick,
    )
    plot_2 = plt.plot(
        T_list,
        annealed_trap_2_densities,
        color=firebrick,
        label=r"Trap 4 ($E_{t} = 1.85$ eV)",
    )
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
    plt.xlabel(r"Annealing temperature (K)")
    plt.ylim(bottom=0)
    plt.xlim(0, 1400)
    plt.legend(loc="lower left")
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


def plot_3():
    plt.figure()
    err_bar_3 = plt.errorbar(
        temperatures,
        trap_3,
        yerr=trap_3_err,
        fmt=".",
        capsize=5,
        color=blue_jeans,
    )
    plot_3 = plt.plot(
        T_list,
        annealed_trap_3_densities,
        color=blue_jeans,
        label=r"Trap 5 ($E_{t} = 2.06$ eV)",
    )
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
    plt.xlabel(r"Annealing temperature (K)")
    plt.ylim(bottom=0)
    plt.xlim(0, 1400)
    plt.legend(loc="lower left")
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


def plot_all_in_one():
    plt.figure()
    err_bar_4 = plt.errorbar(
        temperatures,
        trap_1,
        yerr=trap_1_err,
        fmt=".",
        capsize=5,
        color=green_ryb,
        label=r"Trap 3 ($E_{t} = 1.65$ eV)",
    )
    plot_4 = plt.plot(
        T_list,
        annealed_trap_1_densities,
        color=green_ryb,
        label=r"Trap 3 fitting ($A_{0} = 0.28$ eV, $E_{A} = 6.18 \cdot 10^{-3}$ s$^{-1}$)",
    )

    err_bar_5 = plt.errorbar(
        temperatures,
        trap_2,
        yerr=trap_2_err,
        fmt=".",
        capsize=5,
        color=firebrick,
        label=r"Trap 4 ($E_{t} = 1.85$ eV)",
    )
    plot_5 = plt.plot(
        T_list,
        annealed_trap_2_densities,
        color=firebrick,
        label=r"Trap 4 fitting ($A_{0} = 0.28$ eV, $E_{A} = 6.18 \cdot 10^{-3}$ s$^{-1}$)",
    )

    err_bar_6 = plt.errorbar(
        temperatures,
        trap_3,
        yerr=trap_3_err,
        fmt=".",
        capsize=5,
        color=blue_jeans,
        label=r"Trap 5 ($E_{t} = 2.06$ eV)",
    )
    plot_6 = plt.plot(
        T_list,
        annealed_trap_3_densities,
        color=blue_jeans,
        label=r"Trap 5 fitting ($A_{0} = 0.28$ eV, $E_{A} = 6.18 \cdot 10^{-3}$ s$^{-1}$)",
    )

    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
    plt.xlabel(r"Annealing temperature (K)")
    # plt.ylim(0, 0.4)
    plt.xlim(0, 1400)
    plt.legend(loc="upper right")
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


def plot_all_with_fitting():

    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(5, 10))

    # trap 2
    plt.sca(axs[0])
    err_bar_4 = plt.errorbar(
        temperatures,
        trap_1,
        yerr=trap_1_err,
        fmt=".",
        capsize=5,
        color=green_ryb,
    )
    plot_4 = plt.plot(
        T_list,
        annealed_trap_1_densities,
        color=green_ryb,
        label=r"Trap 3 ($E_{t} = 1.65$ eV)",
    )
    plt.legend(loc="lower left")
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")

    # Trap 3
    plt.sca(axs[1])
    err_bar_5 = plt.errorbar(
        temperatures,
        trap_2,
        yerr=trap_2_err,
        fmt=".",
        capsize=5,
        color=firebrick,
    )
    plot_5 = plt.plot(
        T_list,
        annealed_trap_2_densities,
        color=firebrick,
        label=r"Trap 4 ($E_{t} = 1.85$ eV)",
    )
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(loc="lower left")
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")

    # trap 4
    plt.sca(axs[2])
    err_bar_6 = plt.errorbar(
        temperatures,
        trap_3,
        yerr=trap_3_err,
        fmt=".",
        capsize=5,
        color=blue_jeans,
    )
    plot_6 = plt.plot(
        T_list,
        annealed_trap_3_densities,
        color=blue_jeans,
        label=r"Trap 5 ($E_{t} = 2.06$ eV)",
    )
    plt.legend(loc="lower left")
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")
    plt.xlabel(r"Annealing temperature (K)")

    for ax in [axs[0], axs[1], axs[2]]:
        plt.sca(ax)
        # plt.ylim(0, 7e25)
        # plt.xlim(0, 3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.subplots_adjust(wspace=0.112, hspace=0.2)

    plt.tight_layout()


def plot_all_with_fitting_wo_t4():

    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(5, 7.5))

    # trap 1
    plt.sca(axs[0])
    values_4 = plt.scatter(
        temperatures,
        trap_1,
        marker="x",
        color=green_ryb,
        # label=r"Trap A3 ($E_{t} = 1.65$ eV)",
    )
    plot_4 = plt.plot(
        T_list,
        annealed_trap_1_densities,
        color=green_ryb,
        label=r"Trap 3",
    )

    # trap 2
    plt.sca(axs[1])
    values_5 = plt.scatter(
        temperatures,
        trap_2,
        marker="x",
        color=firebrick,
        # label=r"Trap A4 ($E_{t} = 1.85$ eV)"
    )
    plot_5 = plt.plot(
        T_list,
        annealed_trap_2_densities,
        color=firebrick,
        label=r"Trap 4",
    )
    h, l = plt.gca().get_legend_handles_labels()
    plt.xlabel(r"Annealing temperature (K)")

    for ax in [axs[0], axs[1]]:
        plt.sca(ax)
        plt.ylim(bottom=0)
        plt.xlim(0, 1400)
        plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")
        plt.legend(loc="lower left")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.subplots_adjust(wspace=0.112, hspace=0.2)

    plt.tight_layout()


# plot_1()
# plot_2()
# plot_3()
# plot_all_in_one()
# plot_all_with_fitting()
plot_all_with_fitting_wo_t4()

plt.show()
