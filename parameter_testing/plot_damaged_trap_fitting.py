import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import LogNorm, ListedColormap
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve
from scipy.interpolate import interp1d


from neutron_trap_creation_models import (
    neutron_trap_creation_numerical,
    trap1,
    trap2,
    trap3,
    trap4,
    dpa_list,
    dpa_values,
    A_0_optimised,
    E_A_optimised,
)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)

data_dmg = np.genfromtxt("damage_dpa_t_selinger.csv", delimiter=",", names=True)
x_data = np.array(data_dmg["x"])
dpa_data = np.array(data_dmg["dpa"])
dpa_data = dpa_data / dpa_data.max()
interp_func = interp1d(x_data, dpa_data, fill_value="extrapolate")
x = np.linspace(0, x_data.max(), 1000)

t_damage = 86400
t = np.linspace(0, t_damage, t_damage)
A_0 = A_0_optimised
E_A = E_A_optimised
T = 370
n_0 = 0

trap1_K = 6.0e26
trap1_n_max = 4.5e25
trap2_K = 3.5e26
trap2_n_max = 3.1e25
trap3_K = 2.9e26
trap3_n_max = 2.4e25
trap4_K = 8.0e26
trap4_n_max = 5.8e25

phi = 2.5 / t_damage
K = 5e21
n_max = 3.1e25

damaged_trap1_densities = []
damaged_trap2_densities = []
damaged_trap3_densities = []
damaged_trap4_densities = []

dpa_list = np.linspace(0, 3, num=100)
for dpa in dpa_list:
    phi = dpa / t_damage
    # trap 1
    trap1_extra_args = (phi, trap1_K, trap1_n_max, A_0, E_A, T)
    n_trap1_damaged = odeint(
        neutron_trap_creation_numerical, n_0, t, args=trap1_extra_args
    )
    damaged_trap1_densities.append(float(n_trap1_damaged[-1]))
    # trap 2
    trap2_extra_args = (phi, trap2_K, trap2_n_max, A_0, E_A, T)
    n_trap2_damaged = odeint(
        neutron_trap_creation_numerical, n_0, t, args=trap2_extra_args
    )
    damaged_trap2_densities.append(float(n_trap2_damaged[-1]))
    # trap 3
    trap3_extra_args = (phi, trap3_K, trap3_n_max, A_0, E_A, T)
    n_trap3_damaged = odeint(
        neutron_trap_creation_numerical, n_0, t, args=trap3_extra_args
    )
    damaged_trap3_densities.append(float(n_trap3_damaged[-1]))
    # trap 4
    trap4_extra_args = (phi, trap4_K, trap4_n_max, A_0, E_A, T)
    n_trap4_damaged = odeint(
        neutron_trap_creation_numerical, n_0, t, args=trap4_extra_args
    )
    damaged_trap4_densities.append(float(n_trap4_damaged[-1]))

trap1_err = np.array(trap1) * 0.1
trap2_err = np.array(trap2) * 0.1
trap3_err = np.array(trap3) * 0.1
trap4_err = np.array(trap4) * 0.1


def plot_all_in_one():
    plt.figure(figsize=(8, 8))

    # trap 1
    err_bar_1 = plt.errorbar(
        dpa_values,
        trap1,
        yerr=trap1_err,
        fmt=".",
        capsize=5,
        color=firebrick,
        label=r"Trap 2 ($E_{t} = 1.15$ eV)",
    )
    plot_1 = plt.plot(
        dpa_list,
        damaged_trap1_densities,
        color=firebrick,
        label=r"Trap 2 fitting ($K = 6.0 \cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  4.5\cdot 10^{25}$ m$^{-3}$)",
    )

    # trap 2
    err_bar_2 = plt.errorbar(
        dpa_values,
        trap2,
        yerr=trap2_err,
        fmt=".",
        color=electric_blue,
        capsize=5,
        label=r"Trap 3 ($E_{t} = 1.30$ eV)",
    )
    plot_2 = plt.plot(
        dpa_list,
        damaged_trap2_densities,
        color=electric_blue,
        label=r"Trap 3 fitting ($K = 3.5 \cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  3.5\cdot 10^{25}$ m$^{-3}$)",
    )

    # trap 3
    err_bar_3 = plt.errorbar(
        dpa_values,
        trap3,
        yerr=trap3_err,
        fmt=".",
        capsize=5,
        color=pewter_blue,
        label=r"Trap 4 ($E_{t} = 1.50$ eV)",
    )
    plot_3 = plt.plot(
        dpa_list,
        damaged_trap3_densities,
        color=pewter_blue,
        label=r"Trap 4 fitting ($K = 2.9\cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  2.4\cdot 10^{25}$ m$^{-3}$)",
    )

    # trap 4
    err_bar_4 = plt.errorbar(
        dpa_values,
        trap4,
        yerr=trap4_err,
        fmt=".",
        capsize=5,
        color=green_ryb,
        label=r"Trap 5 ($E_{t} = 1.85$ eV)",
    )
    plot_4 = plt.plot(
        dpa_list,
        damaged_trap4_densities,
        color=green_ryb,
        label=r"Trap 5 fitting ($K = 8.0\cdot 10^{21}$ s$^{-1}$, $n_{max, \phi} =  5.8\cdot 10^{25}$ m$^{-3}$) ",
    )

    # plt.xscale("log")
    plt.ylim(bottom=0)
    plt.xlim(0, 3)
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")
    plt.xlabel(r"Damage (dpa)")

    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(
        [h[7], h[3], h[4], h[0], h[5], h[1], h[6], h[2]],
        [l[7], l[3], l[4], l[0], l[5], l[1], l[6], l[2]],
        loc="lower right",
    )

    # plt.legend(loc="lower right")
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.tight_layout()


def plot_all(i=8):

    fig, axs = plt.subplots(2, 2, sharex=True, sharey="row", figsize=(12, 9))

    # trap 2
    plt.sca(axs[0, 0])
    err_bar_1 = plt.errorbar(
        dpa_values[:i],
        trap1[:i],
        yerr=trap1_err[:i],
        fmt=".",
        capsize=5,
        color=firebrick,
        label=r"Trap 2 ($E_{t} = 1.15$ eV)",
    )
    plt.legend(loc="lower right")
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")

    # Trap 3
    plt.sca(axs[0, 1])
    err_bar_2 = plt.errorbar(
        dpa_values[:i],
        trap2[:i],
        yerr=trap2_err[:i],
        fmt=".",
        color=electric_blue,
        capsize=5,
        label=r"Trap 3 ($E_{t} = 1.30$ eV)",
    )
    plt.legend(loc="lower right")

    # trap 4
    plt.sca(axs[1, 0])
    err_bar_3 = plt.errorbar(
        dpa_values[:i],
        trap3[:i],
        yerr=trap3_err[:i],
        fmt=".",
        capsize=5,
        color=pewter_blue,
        label=r"Trap 4 ($E_{t} = 1.50$ eV)",
    )
    plt.legend(loc="lower right")
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")
    plt.xlabel(r"Damage (dpa)")

    # trap 5
    plt.sca(axs[1, 1])
    err_bar_4 = plt.errorbar(
        dpa_values[:i],
        trap4[:i],
        yerr=trap4_err[:i],
        fmt=".",
        capsize=5,
        color=green_ryb,
        label=r"Trap 5 ($E_{t} = 1.85$ eV)",
    )
    plt.legend(loc="lower right")
    plt.xlabel(r"Damage (dpa)")

    for ax in [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]:
        plt.sca(ax)
        plt.ylim(0, 7e25)
        plt.xlim(0, 3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.subplots_adjust(wspace=0.112, hspace=0.2)
    plt.tight_layout()


def plot_all_presentation(i=8):

    plt.figure(figsize=(6.4, 6.4))

    # trap 5
    err_bar_4 = plt.errorbar(
        dpa_values[:i],
        trap4[:i],
        yerr=trap4_err[:i],
        fmt=".",
        capsize=5,
        color=green_ryb,
    )
    points_4 = plt.scatter(
        dpa_values[:i], trap4[:i], color=green_ryb, s=10, label="Trap 5"
    )

    # trap 2
    err_bar_1 = plt.errorbar(
        dpa_values[:i],
        trap1[:i],
        yerr=trap1_err[:i],
        fmt=".",
        capsize=5,
        color=firebrick,
    )
    points_4 = plt.scatter(
        dpa_values[:i], trap1[:i], color=firebrick, s=10, label="Trap 2"
    )

    # Trap 3
    err_bar_2 = plt.errorbar(
        dpa_values[:i],
        trap2[:i],
        yerr=trap2_err[:i],
        fmt=".",
        color=pewter_blue,
        capsize=5,
    )
    points_4 = plt.scatter(
        dpa_values[:i], trap2[:i], color=pewter_blue, s=10, label="Trap 3"
    )

    # trap 4
    err_bar_3 = plt.errorbar(
        dpa_values[:i],
        trap3[:i],
        yerr=trap3_err[:i],
        fmt=".",
        capsize=5,
        color=electric_blue,
    )
    points_3 = plt.scatter(
        dpa_values[:i], trap3[:i], color=electric_blue, s=10, label="Trap 4"
    )

    # # trap 5
    # err_bar_4 = plt.errorbar(
    #     dpa_values[:i],
    #     trap4[:i],
    #     yerr=trap4_err[:i],
    #     fmt=".",
    #     capsize=5,
    #     color=green_ryb,
    # )
    # points_4 = plt.scatter(
    #     dpa_values[:i], trap4[:i], color=green_ryb, s=10, label="Trap 5"
    # )

    plt.legend(loc="lower right")

    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")
    plt.xlabel(r"Damage (dpa)")
    plt.ylim(0, 7e25)
    plt.xlim(0, 3.5)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.savefig("figure_{}.svg".format(i))


def plot_all_with_fitting():

    fig, axs = plt.subplots(2, 2, sharex=True, sharey="row", figsize=(12, 9))

    # trap 2
    plt.sca(axs[0, 0])
    err_bar_1 = plt.errorbar(
        dpa_values,
        trap1,
        yerr=trap1_err,
        fmt=".",
        capsize=5,
        color=firebrick,
        label=r"Trap 2 ($E_{t} = 1.15$ eV)",
    )
    plot_1 = plt.plot(
        dpa_list,
        damaged_trap1_densities,
        color=firebrick,
        label=r"Trap 2 fitting ($K = 6.0 \cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  4.5\cdot 10^{25}$ m$^{-3}$)",
    )
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend([h[1], h[0]], [l[1], l[0]], loc="lower right")
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")

    # Trap 3
    plt.sca(axs[0, 1])
    err_bar_2 = plt.errorbar(
        dpa_values,
        trap2,
        yerr=trap2_err,
        fmt=".",
        color=electric_blue,
        capsize=5,
        label=r"Trap 3 ($E_{t} = 1.30$ eV)",
    )
    plot_2 = plt.plot(
        dpa_list,
        damaged_trap2_densities,
        color=electric_blue,
        label=r"Trap 3 fitting ($K = 3.5 \cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  3.5\cdot 10^{25}$ m$^{-3}$)",
    )
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend([h[1], h[0]], [l[1], l[0]], loc="lower right")

    # trap 4
    plt.sca(axs[1, 0])
    err_bar_3 = plt.errorbar(
        dpa_values,
        trap3,
        yerr=trap3_err,
        fmt=".",
        capsize=5,
        color=pewter_blue,
        label=r"Trap 4 ($E_{t} = 1.50$ eV)",
    )
    plot_3 = plt.plot(
        dpa_list,
        damaged_trap3_densities,
        color=pewter_blue,
        label=r"Trap 4 fitting ($K = 2.9\cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  2.4\cdot 10^{25}$ m$^{-3}$)",
    )
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend([h[1], h[0]], [l[1], l[0]], loc="lower right")
    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")
    plt.xlabel(r"Damage (dpa)")

    # trap 5
    plt.sca(axs[1, 1])
    err_bar_4 = plt.errorbar(
        dpa_values,
        trap4,
        yerr=trap4_err,
        fmt=".",
        capsize=5,
        color=green_ryb,
        label=r"Trap 5 ($E_{t} = 1.85$ eV)",
    )
    plot_4 = plt.plot(
        dpa_list,
        damaged_trap4_densities,
        color=green_ryb,
        label=r"Trap 5 fitting ($K = 8.0\cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  5.8\cdot 10^{25}$ m$^{-3}$) ",
    )
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend([h[1], h[0]], [l[1], l[0]], loc="lower right")
    plt.xlabel(r"Damage (dpa)")

    for ax in [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]:
        plt.sca(ax)
        plt.ylim(0, 7e25)
        plt.xlim(0, 3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.subplots_adjust(wspace=0.112, hspace=0.2)

    plt.tight_layout()


def plot_all_with_fitting_presentation():

    plt.figure(figsize=(6.4, 6.4))

    # trap 2
    err_bar_1 = plt.errorbar(
        dpa_values,
        trap1,
        yerr=trap1_err,
        fmt=".",
        capsize=5,
        color=firebrick,
    )
    points_1 = plt.scatter(
        dpa_values,
        trap1,
        color=firebrick,
        s=10,
    )
    plot_1 = plt.plot(
        dpa_list,
        damaged_trap1_densities,
        color=firebrick,
    )

    # Trap 3
    err_bar_2 = plt.errorbar(
        dpa_values,
        trap2,
        yerr=trap2_err,
        fmt=".",
        color=pewter_blue,
        capsize=5,
    )
    points_1 = plt.scatter(
        dpa_values,
        trap2,
        color=pewter_blue,
        s=10,
    )
    plot_2 = plt.plot(
        dpa_list,
        damaged_trap2_densities,
        color=pewter_blue,
    )

    # trap 4
    err_bar_3 = plt.errorbar(
        dpa_values,
        trap3,
        yerr=trap3_err,
        fmt=".",
        capsize=5,
        color=electric_blue,
    )
    points_1 = plt.scatter(
        dpa_values,
        trap3,
        color=electric_blue,
        s=10,
    )
    plot_3 = plt.plot(
        dpa_list,
        damaged_trap3_densities,
        color=electric_blue,
    )

    # trap 5
    err_bar_4 = plt.errorbar(
        dpa_values,
        trap4,
        yerr=trap4_err,
        fmt=".",
        capsize=5,
        color=green_ryb,
    )
    points_1 = plt.scatter(
        dpa_values,
        trap4,
        color=green_ryb,
        s=10,
    )
    plot_4 = plt.plot(
        dpa_list,
        damaged_trap4_densities,
        color=green_ryb,
    )
    plt.hlines(8e25, 0, 1, color="black", label="Fittings")
    x_annotation = 3.15
    plt.annotate(
        "Trap 5", (x_annotation, damaged_trap4_densities[-1] * 0.98), color=green_ryb
    )
    plt.annotate(
        "Trap 2", (x_annotation, damaged_trap1_densities[-1] * 0.98), color=firebrick
    )
    plt.annotate(
        "Trap 3", (x_annotation, damaged_trap2_densities[-1] * 0.96), color=pewter_blue
    )
    plt.annotate(
        "Trap 4",
        (x_annotation, damaged_trap3_densities[-1] * 0.96),
        color=electric_blue,
    )

    plt.legend(loc="lower right")

    plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")
    plt.xlabel(r"Damage (dpa)")
    plt.ylim(0, 7e25)
    plt.xlim(0, 3.5)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


values = [8, 7, 6, 5, 4, 3, 2, 1]

# for i in values:
# plot_all(i)
# plot_all_presentation(i)

plot_all_in_one()
# plot_all_with_fitting()
# plot_all_with_fitting_presentation()

plt.show()
