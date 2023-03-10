import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib import ticker
from matplotlib.colors import LogNorm, Normalize

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

    dpa_values = np.geomspace(1e-03, 1e03, num=50)
    T_values = np.linspace(400, 1300, num=50)
    T_values_alt = np.linspace(1300, 400, num=50)
    print(T_values)
    print(T_values_alt)

    norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in dpa_values]

    plt.figure()

    T_values = T_values
    for dpa, colour in zip(dpa_values, colours):
        invs_per_dpa = []
        for T in T_values:
            results_folder = "../parametric_study/"
            data_file = (
                results_folder
                + "dpa={:.0e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
            )
            data = np.genfromtxt(data_file, delimiter=",", names=True)
            invs_per_dpa.append(data["Total_retention_volume_1"][-1])
        plt.plot(T_values, invs_per_dpa, color=colour)

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


def plot_characteristic_time_evolution():

    dpa_values = np.geomspace(1e-03, 1e03, num=50)
    T_values = np.linspace(1300, 400, num=50)
    T_values = T_values[:34]

    inventories = []
    inventories_steady = []
    ts = []

    results_folder = "../parametric_studies/case_1e09s/"
    steady_results_folder = "../parametric_studies/case_steady/"

    for T in T_values:
        invs_per_T = []
        ts_per_T = []
        steady_invs_per_T = []
        for dpa in dpa_values:
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

        # plt.plot(T_values, invs_per_dpa, color=colour)

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

    norm = Normalize(vmin=min(T_values), vmax=max(T_values))
    colorbar = cm.inferno
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(T)) for T in T_values]

    plt.figure(figsize=[8, 4.8])

    day = 3600 * 24
    month = day * 31
    year = day * 365.25
    # plt.hlines(day, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
    # plt.hlines(month, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
    # plt.hlines(year, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
    # plt.hlines(year * 10, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")

    # dpa_values = dpa_valuses / year
    for T, char_times, colour in zip(T_values, characteristic_times, colours):
        plt.plot(dpa_values, char_times, color=colour)

    plt.xscale("log")
    plt.yscale("log")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.ylabel(r"$\tau_{c}$ (s)")
    plt.xlabel(r"Damage rate (dpa/fpy)")
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    plt.colorbar(sm, label=r"Temperature (K)")
    plt.xlim(1e-03, 1.5e04)
    plt.ylim(1e03, 1e09)

    plt.hlines(day, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
    plt.hlines(month, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
    plt.hlines(year, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
    plt.hlines(year * 10, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")

    plt.annotate("1 day", [2e03, day * 1.1], color="black", alpha=0.3)
    plt.annotate("1 month", [2e03, month * 1.1], color="black", alpha=0.3)
    plt.annotate("1 year", [2e03, year * 1.1], color="black", alpha=0.3)
    plt.annotate("10 years", [2e03, year * 10 * 1.1], color="black", alpha=0.3)

    # print(characteristic_times)


def plot_transient_inventories_1fpy():

    dpa_values = np.geomspace(1e-05, 1e03, num=9)
    T_values = np.linspace(1300, 400, num=50)[:37]

    norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in dpa_values]

    plt.figure()

    T_values = T_values
    for dpa, colour in zip(dpa_values, colours):
        invs_per_dpa = []
        for T in T_values:
            results_folder = "../parametric_studies/case_1fpy/"
            data_file = (
                results_folder
                + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
            )
            data = np.genfromtxt(data_file, delimiter=",", names=True)
            invs_per_dpa.append(data["Total_retention_volume_1"][-1])
        plt.plot(T_values, invs_per_dpa, color=colour)

    plt.ylabel(r"T inventory (m$^{-3}$)")
    plt.xlabel(r"Temperature (K)")
    # plt.ylim(1e16, 1e24)
    plt.xlim(400, 1300)
    plt.yscale("log")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    plt.colorbar(sm, label=r"Damage rate (dpa/fpy)")


def plot_retention_profile_1e5s_alt():

    dpa_values = np.geomspace(1e-03, 1e03, num=10)
    # dpa_values = np.geomspace(1e03, 1e-03, num=10)
    results_folder = "../parametric_studies/case_1e05s/T=700K/profiles/"
    data_file = results_folder + "dpa=1.00e-01.csv"
    x_data = np.genfromtxt(data_file, delimiter=",", names=True)
    x_values = x_data["arc_length"]
    x_plot = x_values * 1000

    inventories = []
    for dpa in dpa_values:
        data_file = results_folder + "dpa={:.2e}.csv".format(dpa)
        data = np.genfromtxt(data_file, delimiter=",", names=True)
        inv = data["retention"]
        inventories.append(inv)

    fpy = 3600 * 24 * 365.25
    dpa_values = dpa_values / fpy

    norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in dpa_values]

    plt.figure()
    for inv, dpa, colour in zip(inventories, dpa_values, colours):
        plt.plot(x_plot, inv, color=colour)
    plt.xlabel(r"x (mm)")
    plt.ylabel(r"Retention (T m$^{-1}$)")
    plt.xlim(0, 1)
    plt.yscale("log")
    plt.ylim(1e21, 1e26)
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    plt.colorbar(sm, label=r"Damage rate (dpa s$^{-1}$)")
    plt.tight_layout()


def plot_transient_inventories_varying_T_and_damage_24h():

    dpa_values = np.geomspace(1e-05, 1e03, num=50)
    T_values = np.linspace(400, 1300, num=50)

    T_values = T_values

    fpy = 3600 * 24 * 365.25
    dpa_plot_values = dpa_values / fpy
    norm = LogNorm(vmin=min(dpa_plot_values), vmax=max(dpa_plot_values))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours = [colorbar(norm(dpa)) for dpa in dpa_plot_values]

    results_folder = "../parametric_studies/case_24h/"

    reference_inventories = []
    for T in T_values:
        no_damage_results_file = (
            results_folder + "dpa=0/T={:.0f}/derived_quantities.csv".format(T)
        )
        no_damage_data = np.genfromtxt(
            no_damage_results_file, delimiter=",", names=True
        )
        reference_inventories.append(no_damage_data["Total_retention_volume_1"][-1])

    plt.figure()

    T_values = T_values
    for dpa, colour in zip(dpa_values, colours):
        invs_per_dpa = []
        for T in T_values:
            data_file = (
                results_folder
                + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
            )
            data = np.genfromtxt(data_file, delimiter=",", names=True)
            invs_per_dpa.append(data["Total_retention_volume_1"][-1])
        plt.plot(T_values, invs_per_dpa, color=colour)

    plt.plot(T_values, reference_inventories, color="black")

    plt.ylabel(r"T inventory (m$^{-3}$)")
    plt.xlabel(r"Temperature (K)")
    plt.ylim(1e16, 1e23)
    plt.xlim(400, 1300)
    plt.yscale("log")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.112, hspace=0.071)
    plt.colorbar(sm, label=r"Damage rate (dpa s$^{-1}$)")


def plot_relative_inventory_24h():
    dpa_values = np.geomspace(1e-05, 1e03, num=50)
    T_values = np.linspace(400, 1300, num=50)

    T_values = T_values

    results_folder = "../parametric_studies/case_24h/"

    inventories = []
    for dpa in dpa_values:
        invs_per_dpa = []
        for T in T_values:
            data_file = (
                results_folder
                + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
            )
            data = np.genfromtxt(data_file, delimiter=",", names=True)
            invs_per_dpa.append(data["Total_retention_volume_1"][-1])
        inventories.append(invs_per_dpa)

    reference_inventories = []
    for T in T_values:
        no_damage_results_file = (
            results_folder + "dpa=0/T={:.0f}/derived_quantities.csv".format(T)
        )
        no_damage_data = np.genfromtxt(
            no_damage_results_file, delimiter=",", names=True
        )
        reference_inventories.append(no_damage_data["Total_retention_volume_1"][-1])

    reference_inventories = reference_inventories

    normalised_inventories = []
    inventories = np.array(inventories)
    for inv in inventories:
        normalised_inv = inv / np.array(reference_inventories)
        normalised_inventories.append(normalised_inv)

    fpy = 3600 * 24 * 365.25
    plot_dpa_values = dpa_values / fpy
    X, Y = np.meshgrid(T_values, plot_dpa_values)

    fig, ax = plt.subplots()
    CS = ax.contourf(
        X,
        Y,
        normalised_inventories,
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


# plot_transient_inventories()
# plot_comparison_transient_vs_analytical()
# plot_retention_profile_1e5s()
# plot_total_retention_1e5s_case()
# plot_transient_inventories_varying_T_and_damage()
# plot_characteristic_time_evolution()
# plot_transient_inventories_1fpy()
plot_retention_profile_1e5s_alt()
# plot_transient_inventories_varying_T_and_damage_24h()
# plot_relative_inventory_24h()

plt.show()
