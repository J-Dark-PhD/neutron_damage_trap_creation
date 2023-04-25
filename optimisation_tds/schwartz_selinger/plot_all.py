import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import csv
import io
from matplotlib import cm
from matplotlib.colors import LogNorm

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)

implantation_time = 72 * 3600
resting_time = 0.5 * 24 * 3600
area = 12e-03 * 15e-03

tds_dpa_0 = "tds_data/0_dpa.csv"
tds_dpa_0_001 = "tds_data/0.001_dpa.csv"
tds_dpa_0_005 = "tds_data/0.005_dpa.csv"
tds_dpa_0_023 = "tds_data/0.023_dpa.csv"
tds_dpa_0_1 = "tds_data/0.1_dpa.csv"
tds_dpa_0_23 = "tds_data/0.23_dpa.csv"
tds_dpa_0_5 = "tds_data/0.5_dpa.csv"
tds_dpa_2_5 = "tds_data/2.5_dpa.csv"

data_0 = np.genfromtxt(tds_dpa_0, delimiter=",")
T_0 = data_0[:, 0]
flux_0 = data_0[:, 1] / area

data_0_001 = np.genfromtxt(tds_dpa_0_001, delimiter=",")
T_0_001 = data_0_001[:, 0]
flux_0_001 = data_0_001[:, 1] / area

data_0_005 = np.genfromtxt(tds_dpa_0_005, delimiter=",")
T_0_005 = data_0_005[:, 0]
flux_0_005 = data_0_005[:, 1] / area

data_0_023 = np.genfromtxt(tds_dpa_0_023, delimiter=",")
T_0_023 = data_0_023[:, 0]
flux_0_023 = data_0_023[:, 1] / area

data_0_1 = np.genfromtxt(tds_dpa_0_1, delimiter=",")
T_0_1 = data_0_1[:, 0]
flux_0_1 = data_0_1[:, 1] / area

data_0_23 = np.genfromtxt(tds_dpa_0_23, delimiter=",")
T_0_23 = data_0_23[:, 0]
flux_0_23 = data_0_23[:, 1] / area

data_0_5 = np.genfromtxt(tds_dpa_0_5, delimiter=",")
T_0_5 = data_0_5[:, 0]
flux_0_5 = data_0_5[:, 1] / area


data_2_5 = np.genfromtxt(tds_dpa_2_5, delimiter=",")
T_2_5 = data_2_5[:, 0]
flux_2_5 = data_2_5[:, 1] / area


def plot_TDS_data():

    plt.figure(figsize=(6.4, 5.5))
    plt.plot(T_2_5, flux_2_5, label=r"2.5 dpa", linewidth=3)
    plt.plot(T_0_5, flux_0_5, label=r"0.5 dpa", linewidth=3)
    plt.plot(T_0_23, flux_0_23, label=r"0.23 dpa", linewidth=3)
    plt.plot(T_0_1, flux_0_1, label=r"0.1 dpa", linewidth=3)
    plt.plot(T_0_023, flux_0_023, label=r"0.023 dpa", linewidth=3)
    plt.plot(T_0_005, flux_0_005, label=r"0.005 dpa", linewidth=3)
    plt.plot(T_0_001, flux_0_001, label=r"0.001 dpa", linewidth=3)
    plt.plot(T_0, flux_0, label=r"0 dpa", linewidth=3)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    # plt.savefig("tds_data.svg")


def plot_dpa_0():
    data_0 = np.genfromtxt(tds_dpa_0, delimiter=",")
    T_0 = data_0[:, 0]
    flux_0 = data_0[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []

    with open("Results/dpa_0/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0, flux_0, label="0 dpa")
    plt.scatter(T_0, flux_0, label=r"Exp", color="black")
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    # plt.plot(
    #     T_sim[1:],
    #     solute_contrib,
    #     linestyle="dashed",
    #     color="black",
    #     label=r"Solute",
    # )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0_dpa.svg")


def plot_dpa_0_001():
    data_0_001 = np.genfromtxt(tds_dpa_0_001, delimiter=",")
    T_0_001 = data_0_001[:, 0]
    flux_0_001 = data_0_001[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.001/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_001, flux_0_001, label=r"0.001 dpa")
    plt.scatter(T_0_001, flux_0_001, color="black", label=r"Exp")
    alpha = 0.05
    plt.scatter(T_0, flux_0, color="black", alpha=alpha)

    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.001 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.001_dpa.svg")


def plot_dpa_0_005():
    data_0_005 = np.genfromtxt(tds_dpa_0_005, delimiter=",")
    T_0_005 = data_0_005[:, 0]
    flux_0_005 = data_0_005[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.005/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_005, flux_0_005, label=r"0.005 dpa")
    plt.scatter(T_0_005, flux_0_005, color="black", label=r"Exp")
    alpha = 0.05
    plt.scatter(T_0_001, flux_0_001, color="black", alpha=alpha)
    plt.scatter(T_0, flux_0, color="black", alpha=alpha)
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.005 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.005_dpa.svg")


def plot_dpa_0_023():
    data_0_023 = np.genfromtxt(tds_dpa_0_023, delimiter=",")
    T_0_023 = data_0_023[:, 0]
    flux_0_023 = data_0_023[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.023/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))
    # plt.scatter(T_0_023, flux_0_023, label=r"0.023 dpa")
    plt.scatter(T_0_023, flux_0_023, label=r"Exp", color="black")
    alpha = 0.05
    plt.scatter(T_0_005, flux_0_005, color="black", alpha=alpha)
    plt.scatter(T_0_001, flux_0_001, color="black", alpha=alpha)
    plt.scatter(T_0, flux_0, color="black", alpha=alpha)
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.023 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.023_dpa.svg")


def plot_dpa_0_1():
    data_0_1 = np.genfromtxt(tds_dpa_0_1, delimiter=",")
    T_0_1 = data_0_1[:, 0]
    flux_0_1 = data_0_1[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.1/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_1, flux_0_1, label=r"0.1 dpa")
    plt.scatter(T_0_1, flux_0_1, label=r"Exp", color="black")
    alpha = 0.05
    plt.scatter(T_0_023, flux_0_023, color="black", alpha=alpha)
    plt.scatter(T_0_005, flux_0_005, color="black", alpha=alpha)
    plt.scatter(T_0_001, flux_0_001, color="black", alpha=alpha)
    plt.scatter(T_0, flux_0, color="black", alpha=alpha)
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.1 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.1_dpa.svg")


def plot_dpa_0_23():
    data_0_23 = np.genfromtxt(tds_dpa_0_23, delimiter=",")
    T_0_23 = data_0_23[:, 0]
    flux_0_23 = data_0_23[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.23/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_23, flux_0_23, label=r"0.23 dpa")
    plt.scatter(T_0_23, flux_0_23, label=r"Exp", color="black")
    alpha = 0.05
    plt.scatter(T_0_1, flux_0_1, color="black", alpha=alpha)
    plt.scatter(T_0_023, flux_0_023, color="black", alpha=alpha)
    plt.scatter(T_0_005, flux_0_005, color="black", alpha=alpha)
    plt.scatter(T_0_001, flux_0_001, color="black", alpha=alpha)
    plt.scatter(T_0, flux_0, color="black", alpha=alpha)
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.23 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.23_dpa.svg")


def plot_dpa_0_5():
    data_0_5 = np.genfromtxt(tds_dpa_0_5, delimiter=",")
    T_0_5 = data_0_5[:, 0]
    flux_0_5 = data_0_5[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.5/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_5, flux_0_5, label=r"0.5 dpa")
    plt.scatter(T_0_5, flux_0_5, label=r"Exp", color="black")
    alpha = 0.05
    plt.scatter(T_0_23, flux_0_23, color="black", alpha=alpha)
    plt.scatter(T_0_1, flux_0_1, color="black", alpha=alpha)
    plt.scatter(T_0_023, flux_0_023, color="black", alpha=alpha)
    plt.scatter(T_0_005, flux_0_005, color="black", alpha=alpha)
    plt.scatter(T_0_001, flux_0_001, color="black", alpha=alpha)
    plt.scatter(T_0, flux_0, color="black", alpha=alpha)
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.5 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.5_dpa.svg")


def plot_dpa_2_5():
    data_2_5 = np.genfromtxt(tds_dpa_2_5, delimiter=",")
    T_2_5 = data_2_5[:, 0]
    flux_2_5 = data_2_5[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_2.5/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))
    # plt.scatter(T_2_5, flux_2_5, label=r"2.5 dpa")
    plt.scatter(T_2_5, flux_2_5, color="black", label=r"Exp")
    alpha = 0.05
    plt.scatter(T_0_5, flux_0_5, color="black", alpha=alpha)
    plt.scatter(T_0_23, flux_0_23, color="black", alpha=alpha)
    plt.scatter(T_0_1, flux_0_1, color="black", alpha=alpha)
    plt.scatter(T_0_023, flux_0_023, color="black", alpha=alpha)
    plt.scatter(T_0_005, flux_0_005, color="black", alpha=alpha)
    plt.scatter(T_0_001, flux_0_001, color="black", alpha=alpha)
    plt.scatter(T_0, flux_0, color="black", alpha=alpha)
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("2.5 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_2.5_dpa.svg")


def plot_dpa_0():
    data_0 = np.genfromtxt(tds_dpa_0, delimiter=",")
    T_0 = data_0[:, 0]
    flux_0 = data_0[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []

    with open("Results/dpa_0/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0, flux_0, label="0 dpa")
    plt.scatter(T_0, flux_0, label=r"Exp", color="black")
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    # plt.plot(
    #     T_sim[1:],
    #     solute_contrib,
    #     linestyle="dashed",
    #     color="black",
    #     label=r"Solute",
    # )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0_dpa.svg")


def plot_dpa_0_001_solo():
    data_0_001 = np.genfromtxt(tds_dpa_0_001, delimiter=",")
    T_0_001 = data_0_001[:, 0]
    flux_0_001 = data_0_001[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.001/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_001, flux_0_001, label=r"0.001 dpa")
    plt.scatter(T_0_001, flux_0_001, color="black", label=r"Exp")

    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.001 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.001_dpa.svg")


def plot_dpa_0_005_solo():
    data_0_005 = np.genfromtxt(tds_dpa_0_005, delimiter=",")
    T_0_005 = data_0_005[:, 0]
    flux_0_005 = data_0_005[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.005/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_005, flux_0_005, label=r"0.005 dpa")
    plt.scatter(T_0_005, flux_0_005, color="black", label=r"Exp")

    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.005 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.005_dpa.svg")


def plot_dpa_0_023_solo():
    data_0_023 = np.genfromtxt(tds_dpa_0_023, delimiter=",")
    T_0_023 = data_0_023[:, 0]
    flux_0_023 = data_0_023[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.023/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))
    # plt.scatter(T_0_023, flux_0_023, label=r"0.023 dpa")
    plt.scatter(T_0_023, flux_0_023, label=r"Exp", color="black")

    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.023 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.023_dpa.svg")


def plot_dpa_0_1_solo():
    data_0_1 = np.genfromtxt(tds_dpa_0_1, delimiter=",")
    T_0_1 = data_0_1[:, 0]
    flux_0_1 = data_0_1[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.1/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_1, flux_0_1, label=r"0.1 dpa")
    plt.scatter(T_0_1, flux_0_1, label=r"Exp", color="black")

    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.1 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.1_dpa.svg")


def plot_dpa_0_23_solo():
    data_0_23 = np.genfromtxt(tds_dpa_0_23, delimiter=",")
    T_0_23 = data_0_23[:, 0]
    flux_0_23 = data_0_23[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.23/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_23, flux_0_23, label=r"0.23 dpa")
    plt.scatter(T_0_23, flux_0_23, label=r"Exp", color="black")

    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.23 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.23_dpa.svg")


def plot_dpa_0_5_solo():
    data_0_5 = np.genfromtxt(tds_dpa_0_5, delimiter=",")
    T_0_5 = data_0_5[:, 0]
    flux_0_5 = data_0_5[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.5/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    # plt.scatter(T_0_5, flux_0_5, label=r"0.5 dpa")
    plt.scatter(T_0_5, flux_0_5, label=r"Exp", color="black")

    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("0.5 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.5_dpa.svg")


def plot_dpa_2_5_solo():
    data_2_5 = np.genfromtxt(tds_dpa_2_5, delimiter=",")
    T_2_5 = data_2_5[:, 0]
    flux_2_5 = data_2_5[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_2.5/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))
    # plt.scatter(T_2_5, flux_2_5, label=r"2.5 dpa")
    plt.scatter(T_2_5, flux_2_5, color="black", label=r"Exp")

    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap 2",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap 3",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap 4",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap 5",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.2e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.title("2.5 dpa")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_2.5_dpa.svg")


def plot_dpa_0_1_detailed():
    data_0_1 = np.genfromtxt(tds_dpa_0_1, delimiter=",")
    T_0_1 = data_0_1[:, 0]
    flux_0_1 = data_0_1[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0.1/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))
                    trap2.append(float(row[7]))
                    trap3.append(float(row[8]))
                    trap4.append(float(row[9]))
                    trap5.append(float(row[10]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    trap_2_contrib = (np.diff(trap2) / np.diff(t)) * -1
    trap_3_contrib = (np.diff(trap3) / np.diff(t)) * -1
    trap_4_contrib = (np.diff(trap4) / np.diff(t)) * -1
    trap_5_contrib = (np.diff(trap5) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    plt.scatter(T_0_1, flux_0_1, label=r"Exp", color="black")
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1",
    )
    plt.plot(
        T_sim[1:],
        trap_2_contrib,
        linestyle="dashed",
        color=firebrick,
        label=r"Trap D1",
    )
    plt.plot(
        T_sim[1:],
        trap_3_contrib,
        linestyle="dashed",
        color=pewter_blue,
        label=r"Trap D2",
    )
    plt.plot(
        T_sim[1:],
        trap_4_contrib,
        linestyle="dashed",
        color=electric_blue,
        label=r"Trap D3",
    )
    plt.plot(
        T_sim[1:],
        trap_5_contrib,
        linestyle="dashed",
        color=green_ryb,
        label=r"Trap D4",
    )
    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_2_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_3_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_4_contrib, color="grey", alpha=0.1)
    plt.fill_between(T_sim[1:], 0, trap_5_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(0, 1.0e17)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.1_dpa_detailed.svg")


def plot_dpa_0_detailed():
    data_0_1 = np.genfromtxt(tds_dpa_0_1, delimiter=",")
    T_0_1 = data_0_1[:, 0]
    flux_0_1 = data_0_1[:, 1] / area

    T_sim = []
    flux1, flux2 = [], []
    solute = []
    ret = []
    t = []
    trap1 = []
    trap2 = []
    trap3 = []
    trap4 = []
    trap5 = []

    with open("Results/dpa_0/last.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        for row in plots:
            if "t(s)" not in row:
                if float(row[0]) >= implantation_time + resting_time * 0.75:
                    t.append(float(row[0]))
                    T_sim.append(float(row[1]))
                    flux1.append(float(row[2]))
                    flux2.append(float(row[3]))
                    solute.append(float(row[4]))
                    ret.append(float(row[5]))
                    trap1.append(float(row[6]))

    trap_1_contrib = (np.diff(trap1) / np.diff(t)) * -1
    solute_contrib = (np.diff(solute) / np.diff(t)) * -1

    plt.figure(figsize=(6.4, 5.5))

    plt.scatter(T_0, flux_0, label=r"Exp", color="black")
    plt.plot(
        T_sim,
        -np.asarray(flux1) - np.asarray(flux2),
        label="Simulation",
        color="orange",
        linewidth=2,
    )
    plt.plot(
        T_sim[1:],
        trap_1_contrib,
        linestyle="dashed",
        color="black",
        label=r"Trap 1 ($E_{t} = 1.00$ eV)",
    )
    plt.plot(
        T_sim[1:],
        solute_contrib,
        linestyle="dashed",
        color="purple",
        label=r"Mobile H (c$_{\mathrm{m}}$)",
    )

    plt.fill_between(T_sim[1:], 0, trap_1_contrib, color="grey", alpha=0.1)

    plt.xlim(300, 1000)
    plt.ylim(top=1.2e16)
    plt.xlabel("Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tds_fitting_0.1_dpa_detailed.svg")


def plot_with_previous():
    plot_dpa_0()
    plot_dpa_0_001()
    plot_dpa_0_005()
    plot_dpa_0_023()
    plot_dpa_0_1()
    plot_dpa_0_23()
    plot_dpa_0_5()
    plot_dpa_2_5()


def plot_alone():
    plot_dpa_0()
    plot_dpa_0_001_solo()
    plot_dpa_0_005_solo()
    plot_dpa_0_023_solo()
    plot_dpa_0_1_solo()
    plot_dpa_0_23_solo()
    plot_dpa_0_5_solo()
    plot_dpa_2_5_solo()


def plot_TDS_data_paper():

    area = 12e-03 * 15e-03

    dpa_values = [2.5, 0.5, 0.23, 0.1, 0.023, 0.005, 0.001, 0]

    tds_T_and_flux = []
    fitting_data = []

    for dpa in dpa_values:
        tds_data_file = "tds_data/{}_dpa.csv".format(dpa)
        tds_data = np.genfromtxt(tds_data_file, delimiter=",", dtype=float)
        tds_data_T = tds_data[:, 0]
        tds_data_flux = tds_data[:, 1] / area
        tds_T_and_flux.append([tds_data_T, tds_data_flux])

        fitting_file = "Results/dpa_{}/last.csv".format(dpa)
        T_sim = []
        flux_1 = []
        flux_2 = []
        with open(fitting_file, "r") as csvfile:
            plots = csv.reader(csvfile, delimiter=",")
            for row in plots:
                if "t(s)" not in row:
                    if float(row[0]) >= implantation_time + resting_time * 0.75:
                        T_sim.append(float(row[1]))
                        flux_1.append(float(row[2]))
                        flux_2.append(float(row[3]))
        flux = -np.asarray(flux_1) - np.asarray(flux_2)
        fitting_data.append([T_sim, flux])

    plot_dpa_values = dpa_values[:-1]
    norm = LogNorm(vmin=min(plot_dpa_values), vmax=max(plot_dpa_values))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in dpa_values]

    plt.figure(figsize=(6.4, 5.5))
    plt.plot(
        tds_T_and_flux[-1][0],
        tds_T_and_flux[-1][1],
        label=r"undamaged",
        linewidth=3,
        color="black",
    )

    tds_T_and_flux = tds_T_and_flux[:-1]
    for case, colour in zip(tds_T_and_flux, colours):
        T_values = case[0]
        flux_values = case[1]
        plt.plot(T_values, flux_values, color=colour, linewidth=3)

    for case in fitting_data[:-1]:
        T_values = case[0]
        flux_values = case[1]
        plt.plot(
            T_values,
            flux_values,
            color="grey",
            linewidth=2,
            linestyle="dashed",
            alpha=0.5,
        )
    plt.plot(
        fitting_data[-1][0],
        fitting_data[-1][1],
        color="grey",
        linewidth=2,
        linestyle="dashed",
        alpha=0.5,
        label="fittings",
    )

    plt.xlim(300, 1000)
    plt.ylim(0, 1e17)
    plt.xlabel(r"Temperature (K)")
    plt.ylabel(r"Desorption flux (D m$ ^{-2}$ s$ ^{-1}$)")
    plt.legend()
    # plt.subplots_adjust(wspace=0.112, hspace=0.071)
    # plt.colorbar(sm, label=r"Damage (dpa)")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    plt.colorbar(sm, label=r"Damage (dpa)")


# plot_alone()
# plot_with_previous()
plot_dpa_0_1_detailed()
# plot_dpa_0_detailed()
# plot_TDS_data()
plot_TDS_data_paper()

plt.show()
