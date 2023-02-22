import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import LogNorm, ListedColormap

dpa_values = np.geomspace(1e-03, 1e03, num=7)

ts = []
inventories = []

# for dpa in dpa_values:
#     results_folder = "../transient_testing/"
#     filename = results_folder + "{:.0e}_dpa/derived_quantities.csv".format(dpa)
#     data = np.genfromtxt(filename, delimiter=",", names=True)
#     ts.append(data["ts"])
#     inventories.append(data["Total_retention_volume_1"])

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


def plot_transient_inventories():
    plt.figure(figsize=(6.4, 6.4))
    for t, inventory, dpa in zip(ts, inventories, dpa_values):
        plt.plot(t, inventory, label="{:.0e} dpa/fpy".format(dpa))

    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(
        [h[6], h[5], h[4], h[3], h[2], h[1], h[0]],
        [l[6], l[5], l[4], l[3], l[2], l[1], l[0]],
        loc="lower right",
    )
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Time (s)")
    plt.ylabel("T Inventory (m$^{-2}$)")
    plt.ylim(bottom=1e15)
    plt.xlim(1e-01, 1e09)
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


def plot_comparison_transient_vs_analytical():
    plt.figure(figsize=(6.4, 6.4))

    plt.plot(
        ts[0],
        inventories[0],
        color="black",
        label="{:.0e} dpa/fpy".format(dpa_values[0]),
    )
    plt.plot(
        ts[2],
        inventories[2],
        color="green",
        label="{:.0e} dpa/fpy".format(dpa_values[2]),
    )
    plt.plot(
        ts[4], inventories[4], color="red", label="{:.0e} dpa/fpy".format(dpa_values[4])
    )

    plt.hlines(
        y=8.61e18,
        xmin=0,
        xmax=1e20,
        color="black",
        alpha=0.6,
        linestyles="dashed",
        label="Analytical steady-state",
    )
    plt.hlines(
        y=6.28e20, xmin=0, xmax=1e20, color="green", alpha=0.6, linestyles="dashed"
    )
    plt.hlines(
        y=3.65e22, xmin=0, xmax=1e20, color="red", alpha=0.6, linestyles="dashed"
    )
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(
        [h[3], h[2], h[1], h[0]],
        [l[3], l[2], l[1], l[0]],
        loc="lower right",
    )
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Time (s)")
    plt.ylabel("T Inventory (m$^{-2}$)")
    plt.ylim(bottom=1e16)
    plt.xlim(1e0, 1e09)
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


def plot_retention_profile_1e5s():

    data_0_001_dpa_file = "Results/profile_1e-03.csv"
    data_0_01_dpa_file = "Results/profile_1e-02.csv"
    data_0_1_dpa_file = "Results/profile_1e-01.csv"
    data_1_dpa_file = "Results/profile_1e00.csv"
    data_10_dpa_file = "Results/profile_1e01.csv"
    data_100_dpa_file = "Results/profile_1e02.csv"
    data_1000_dpa_file = "Results/profile_1e03.csv"

    data_0_001_dpa = np.genfromtxt(data_0_001_dpa_file, delimiter=",", names=True)
    data_0_01_dpa = np.genfromtxt(data_0_01_dpa_file, delimiter=",", names=True)
    data_0_1_dpa = np.genfromtxt(data_0_1_dpa_file, delimiter=",", names=True)
    data_1_dpa = np.genfromtxt(data_1_dpa_file, delimiter=",", names=True)
    data_10_dpa = np.genfromtxt(data_10_dpa_file, delimiter=",", names=True)
    data_100_dpa = np.genfromtxt(data_100_dpa_file, delimiter=",", names=True)
    data_1000_dpa = np.genfromtxt(data_1000_dpa_file, delimiter=",", names=True)

    y = data_1_dpa["retention"]
    x = data_1_dpa["arc_length"]

    inventories = [
        data_0_001_dpa["retention"],
        data_0_01_dpa["retention"],
        data_0_1_dpa["retention"],
        data_1_dpa["retention"],
        data_10_dpa["retention"],
        data_100_dpa["retention"],
        data_1000_dpa["retention"],
    ]
    x_values = [
        data_0_001_dpa["arc_length"],
        data_0_01_dpa["arc_length"],
        data_0_1_dpa["arc_length"],
        data_1_dpa["arc_length"],
        data_10_dpa["arc_length"],
        data_100_dpa["arc_length"],
        data_1000_dpa["arc_length"],
    ]

    plt.figure()
    for inv, x_value, dpa in zip(inventories, x_values, dpa_values):
        x_plot = x_value * 1000
        plt.plot(x_plot, inv, label="{:.0e} dpa/fpy".format(dpa))
    # plt.yscale("log")
    plt.legend()
    plt.xlabel(r"x (mm)")
    plt.ylabel(r"Retention (T m$^{-1}$) (t=1.5 days)")
    plt.xlim(0, 1)
    # plt.ylim(bottom=0)
    plt.yscale("log")
    plt.ylim(1e21, 1e26)
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(
        [h[6], h[5], h[4], h[3], h[2], h[1], h[0]],
        [l[6], l[5], l[4], l[3], l[2], l[1], l[0]],
        loc="upper right",
    )
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.tight_layout()


def plot_total_retention_1e5s_case():

    inventories = []
    x_values = []

    for dpa in dpa_values:
        results_folder = "Results/parametric_testing_1e5s/"
        filename = results_folder + "{:.0e}_dpa/derived_quantities.csv".format(dpa)
        data = np.genfromtxt(filename, delimiter=",", names=True)
        inventories.append(data["Total_retention_volume_1"][-1])
        fpy_to_s = 3600 * 24 * 365
        x_values.append(dpa / fpy_to_s)

    inventories = np.array(inventories)
    x_values = np.array(x_values)

    plt.figure()
    plt.plot(x_values, inventories, marker="x")
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel(r"Damage (dpa s$^{-1}$")
    plt.ylabel(r"Tritium inventory (m$^{-2}$)")
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


def plot_transient_inventories_varying_T_and_damage():

    dpa_values = np.geomspace(1e-03, 1e03, num=7)
    T_values = np.linspace(400, 1400, num=50)

    norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in dpa_values]

    plt.figure()

    # T_values = [400, 420, 441]
    # for dpa, colour in zip(dpa_values, colours):
    #     invs_per_dpa = []
    #     for T in T_values:
    #         try:
    #             results_folder = "../parametric_study/"
    #             data_file = (
    #                 results_folder
    #                 + "dpa={:.1e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
    #             )
    #             data = np.genfromtxt(data_file, delimiter=",", names=True)
    #             invs_per_dpa.append(data["Total_retention_volume_1"][-1])
    #         except:
    #             continue
    #     plt.plot(T_values, invs_per_dpa, color=colour)

    for T in T_values:
        for dpa, colour in zip(dpa_values, colours):
            try:
                results_folder = "../parametric_study/"
                data_file = (
                    results_folder
                    + "dpa={:.1e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
                )
                data = np.genfromtxt(data_file, delimiter=",", names=True)
                inv = data["Total_retention_volume_1"][-1]
                plt.scatter(T, inv, color=colour)
            except:
                continue

    plt.ylabel(r"T inventory (m$^{-3}$)")
    plt.xlabel(r"Temperature (K)")
    plt.ylim(1e16, 1e24)
    plt.xlim(400, 1300)
    plt.yscale("log")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    plt.colorbar(sm, label=r"Damage rate (dpa/fpy)")


# plot_transient_inventories()
# plot_comparison_transient_vs_analytical()
# plot_retention_profile_1e5s()
# plot_total_retention_1e5s_case()
plot_transient_inventories_varying_T_and_damage()

plt.show()
