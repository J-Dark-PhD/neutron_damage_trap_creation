import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib import ticker
from matplotlib.colors import LogNorm, Normalize


def retrive_data_and_save(dpa_values, dpa_values_paper, T_values, T_values_paper):

    results_folder = "../parametric_studies/case_24h/"

    # inventories = []
    # for dpa in dpa_values:
    #     invs_per_dpa = []
    #     for T in T_values:
    #         data_file = (
    #             results_folder
    #             + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
    #         )
    #         data = np.genfromtxt(data_file, delimiter=",", names=True)
    #         invs_per_dpa.append(data["Total_retention_volume_1"][-1])
    #     inventories.append(invs_per_dpa)

    # reference_inventories = []
    # for T in T_values:
    #     no_damage_results_file = (
    #         results_folder + "dpa=0/T={:.0f}/derived_quantities.csv".format(T)
    #     )
    #     no_damage_data = np.genfromtxt(
    #         no_damage_results_file, delimiter=",", names=True
    #     )
    #     reference_inventories.append(no_damage_data["Total_retention_volume_1"][-1])

    # reference_inventories = reference_inventories

    # normalised_inventories = []
    # inventories = np.array(inventories)
    # for inv in inventories:
    #     normalised_inv = inv / np.array(reference_inventories)
    #     normalised_inventories.append(normalised_inv)

    # np.savetxt("reference_inventories_24h", reference_inventories)
    # np.savetxt("normalised_inventories_24h", normalised_inventories)
    # np.savetxt("inventories_24h", inventories)

    inventories_paper = []
    for dpa in dpa_values_paper:
        invs_per_dpa = []
        for T in T_values_paper:
            data_file = (
                results_folder
                + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
            )
            data = np.genfromtxt(data_file, delimiter=",", names=True)
            invs_per_dpa.append(data["Total_retention_volume_1"][-1])
        inventories_paper.append(invs_per_dpa)

    inventories_paper = np.array(inventories_paper)

    np.savetxt("inventories_24h_paper", inventories_paper)


def plot_transient_inventories_varying_T_and_damage_24h_alt(
    dpa_values, dpa_values_paper, T_values, T_values_paper
):
    norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
    colorbar = cm.viridis
    sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

    colours_paper = [colorbar(norm(dpa)) for dpa in dpa_values_paper]

    normalised_inventories = np.loadtxt("normalised_inventories_24h")
    inventories_paper = np.loadtxt("inventories_24h_paper")

    plt.rc("text", usetex=True)
    plt.rc("font", family="serif", size=12)

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=([6.4, 9.6]))

    for case, colour in zip(inventories_paper, colours_paper):
        axs[0].plot(T_values_paper, case, color=colour)

    axs[0].set_ylabel(r"T retention (m$^{-3}$)")
    axs[0].set_ylim(1e16, 1e23)
    axs[0].set_xlim(400, 1300)
    axs[0].set_yscale("log")
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["right"].set_visible(False)

    plt.colorbar(sm, label=r"Damage rate (dpa fpy$^{-1}$)", ax=axs[0])

    normalised_inventories_alt = []
    for case in normalised_inventories:
        new_case = np.where(case > 1, case, 1 + 1e-06)
        normalised_inventories_alt.append(new_case)

    normalised_inventories_alt = np.array(normalised_inventories_alt)
    X, Y = np.meshgrid(T_values, dpa_values)

    CS = axs[1].contourf(
        X,
        Y,
        normalised_inventories_alt,
        norm=LogNorm(),
        levels=np.geomspace(
            np.min(normalised_inventories_alt),
            np.max(normalised_inventories_alt),
            num=1000,
        ),
        cmap="plasma",
    )
    for c in CS.collections:
        c.set_edgecolor("face")
    CS2 = axs[1].contour(
        X,
        Y,
        normalised_inventories_alt,
        levels=[1e00, 1e01, 1e02, 1e03],
        colors="black",
    )
    axs[1].clabel(CS2, inline=True, fontsize=10, fmt="%.0f")

    plt.colorbar(
        CS,
        label=r"Normalised T retention (ret/ret$_{0 \ \mathrm{dpa}}$)",
        format="%.0f  ",
        ax=axs[1],
    )
    axs[1].set_yscale("log")
    axs[1].set_ylabel(r"Damage rate (dpa fpy$^{-1}$)")
    axs[1].set_xlabel(r"Temperature (K)")

    plt.tight_layout()


dpa_values = np.geomspace(1e-05, 1e03, num=100)
dpa_values_paper = np.geomspace(1e-05, 1e03, num=9)
T_values = np.linspace(400, 1300, num=100)
T_values_paper = np.linspace(400, 1300, num=50)

# retrive_data_and_save(
#     dpa_values=dpa_values,
#     dpa_values_paper=dpa_values_paper,
#     T_values=T_values,
#     T_values_paper=T_values_paper,
# )
plot_transient_inventories_varying_T_and_damage_24h_alt(
    dpa_values=dpa_values,
    dpa_values_paper=dpa_values_paper,
    T_values=T_values,
    T_values_paper=T_values_paper,
)

plt.show()
