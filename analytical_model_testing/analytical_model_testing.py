import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.colors import LogNorm
from matplotlib import cm


def trap_concentration(T, phi, K, n_max, A_0, E_A):
    """
    Function to evaluate the trap concentration at a given temperature, T, and
    damage, phi, level

    Args:
        T (float, int): temperature (K)
        phi (float, int): damage rate (dpa s-1),
        K (float int): trap creation factor (m-3 dpa-1),
        n_max (float, int):  maximum trap density (m-3),
        A_0 (float, int): trap_annealing_factor (s-1),
        E_A (float, int): annealing activation energy (eV).

    return:
        n_i (float): trap concentration (m-3)
    """
    if phi == 0:
        n_i = 0
    else:
        A = A_0 * np.exp(-E_A / k_B / T)
        n_i = 1 / ((A / (phi * K) + (1 / (n_max))))

    return n_i


def mobile_H_concentration(T, imp_flux, r_p, D_0, E_D):
    """
    Function to evaluate the mobile concentration of tritium

    Args:
        T (float, int): temperature (K)
        imp_flux (float, int): implantation flux (H m-2 s-1),
        r_p (float int): implantation depth (m),
        D_0 (float, int): diffusion coefficient pre-exponential factor (m2/s)
        E_D (float, int): diffusion coefficient activation energy (eV)

    return:
        c_m (float): mobile concentration of H (m-3)

    """
    D = D_0 * np.exp(-E_D / k_B / T)
    c_m = (imp_flux * r_p) / D

    return c_m


def trapped_H_concentration(T, c_m, k_0, E_k, p_0, E_p, n_i, A_0=0, E_A=1):
    """
    Function to evaluate the trapped concentration

    Args:
        T (float, int): temperature (K)
        c_m (float, int): implantation flux (H m-2 s-1),
        k_0 (float, int): trapping pre-exponential factor (m3 s-1)
        E_k (float, int): trapping activation energy (eV)
        p_0 (float, int): detrapping pre-exponential factor (s-1)
        E_p (float, int): detrapping activation energy (eV)
        A_0 (float, int): trap_annealing_factor (s-1),
        E_A (float, int): annealing activation energy (eV).

    return:
        c_t (float): trapped concentration of H (m-3)
        filling_ratio (float): filling ratio of trap
    """
    A = A_0 * np.exp(-E_A / k_B / T)
    v_t = k_0 * np.exp(-E_k / k_B / T)
    v_dt = p_0 * np.exp(-E_p / k_B / T)

    filling_ratio = 1 / (1 + ((v_dt + A) / (v_t * c_m)))

    c_t = filling_ratio * n_i

    return c_t, filling_ratio


def retention(c_m, c_t, L):
    """
    Function to evaluate the retention

     Args:
        c_m (float, int): mobile concentration of H (m-2)
        c_t (float, int): trapped concentration of H (m-2)
        L (float, int): Length of material (m)

    return:
        retention (float): total retention of H (m-2)

    """
    retention = L * (c_m + c_t)

    return retention


def analytical_model(phi=9 / (3600 * 24 * 365.25), T=761, L=0.002):
    trap_1_density = 8.22e25
    trap_2_density = 2.53e25
    trap_3_density = trap_concentration(
        T=T, phi=phi, K=1.5e28, n_max=5.2e25, A_0=A_0, E_A=E_A
    )
    trap_4_density = trap_concentration(
        T=T, phi=phi, K=4.0e27, n_max=4.5e25, A_0=A_0, E_A=E_A
    )
    trap_5_density = trap_concentration(
        T=T, phi=phi, K=3.0e27, n_max=4.0e25, A_0=A_0, E_A=E_A
    )
    trap_6_density = trap_concentration(
        T=T, phi=phi, K=9.0e27, n_max=4.2e25, A_0=A_0, E_A=E_A
    )

    c_m = mobile_H_concentration(T=T, imp_flux=imp_flux, r_p=r_p, D_0=D_0, E_D=E_D)

    c_t_1, filling_ratio_1 = trapped_H_concentration(
        c_m=c_m, k_0=k_0_1, E_k=E_k, p_0=p_0, E_p=0.87, n_i=trap_1_density, T=T
    )
    c_t_2, filling_ratio_2 = trapped_H_concentration(
        c_m=c_m, k_0=k_0_2, E_k=E_k, p_0=p_0, E_p=1.00, n_i=trap_2_density, T=T
    )
    c_t_3, filling_ratio_3 = trapped_H_concentration(
        c_m=c_m,
        k_0=k_0_1,
        E_k=E_k,
        p_0=p_0,
        E_p=1.15,
        A_0=A_0,
        E_A=E_A,
        n_i=trap_3_density,
        T=T,
    )
    c_t_4, filling_ratio_4 = trapped_H_concentration(
        c_m=c_m,
        k_0=k_0_1,
        E_k=E_k,
        p_0=p_0,
        E_p=1.35,
        A_0=A_0,
        E_A=E_A,
        n_i=trap_4_density,
        T=T,
    )
    c_t_5, filling_ratio_5 = trapped_H_concentration(
        c_m=c_m,
        k_0=k_0_1,
        E_k=E_k,
        p_0=p_0,
        E_p=1.65,
        A_0=A_0,
        E_A=E_A,
        n_i=trap_5_density,
        T=T,
    )
    c_t_6, filling_ratio_6 = trapped_H_concentration(
        c_m=c_m,
        k_0=k_0_1,
        E_k=E_k,
        p_0=p_0,
        E_p=1.85,
        A_0=A_0,
        E_A=E_A,
        n_i=trap_6_density,
        T=T,
    )

    trap_densities = [
        trap_1_density,
        trap_2_density,
        trap_3_density,
        trap_4_density,
        trap_5_density,
        trap_6_density,
    ]

    trap_filling_ratios = [
        filling_ratio_1,
        filling_ratio_2,
        filling_ratio_3,
        filling_ratio_4,
        filling_ratio_5,
        filling_ratio_6,
    ]

    total_trapped_H_concentration = c_t_1 + c_t_2 + c_t_3 + c_t_4 + c_t_5 + c_t_6

    total_retention = retention(c_m=c_m, c_t=total_trapped_H_concentration, L=L)

    return (total_retention, trap_densities, trap_filling_ratios)


def de_trapping_rate(E_p, T):
    v_dt = p_0 * np.exp(-E_p / k_B / T)

    return v_dt


def annealing_rate(T):
    A = A_0 * np.exp(-E_A / k_B / T)

    return A


def compare_annealing_and_detrapping():
    trap_1_detrapping_rates = []
    trap_2_detrapping_rates = []
    trap_3_detrapping_rates = []
    trap_4_detrapping_rates = []
    trap_5_detrapping_rates = []
    trap_6_detrapping_rates = []
    annealing_rates = []
    for T in T_range:
        trap_1_detrapping = de_trapping_rate(E_p=0.85, T=T)
        trap_2_detrapping = de_trapping_rate(E_p=1.00, T=T)
        trap_3_detrapping = de_trapping_rate(E_p=1.15, T=T)
        trap_4_detrapping = de_trapping_rate(E_p=1.25, T=T)
        trap_5_detrapping = de_trapping_rate(E_p=1.65, T=T)
        trap_6_detrapping = de_trapping_rate(E_p=1.85, T=T)
        annealing = annealing_rate(T=T)

        trap_1_detrapping_rates.append(trap_1_detrapping)
        trap_2_detrapping_rates.append(trap_2_detrapping)
        trap_3_detrapping_rates.append(trap_3_detrapping)
        trap_4_detrapping_rates.append(trap_4_detrapping)
        trap_5_detrapping_rates.append(trap_5_detrapping)
        trap_6_detrapping_rates.append(trap_6_detrapping)
        annealing_rates.append(annealing)

    return (
        trap_1_detrapping_rates,
        trap_2_detrapping_rates,
        trap_3_detrapping_rates,
        trap_4_detrapping_rates,
        trap_5_detrapping_rates,
        trap_6_detrapping_rates,
        annealing_rates,
    )


# ##### standard values ##### #

L = 0.002
imp_flux = 1e20
r_p = 3e-09
D_0 = 4.1e-7
E_D = 0.39
k_B = 8.6173303e-5
A_0 = 6.18e-03
E_A = 0.28
k_0_1 = 5.22e-17
k_0_2 = 8.93e-17
E_k = 0.39
p_0 = 1e13

trap_1_conc = 8.22e25
trap_2_conc = 2.53e25

# ##### test ranges ##### #

T_range = np.linspace(400, 1300, num=1000)
T_range_contour = np.linspace(400, 1300, num=100)
dpa_range = [0, 0.001, 0.01, 0.1, 1, 10, 100]
alt_dpa_range = np.geomspace(1e-03, 1e03, num=1000)
dpa_range_contour = np.geomspace(1e-3, 1e03, num=100)

# ##### analytical test results gathering ##### #


inventories = []
inventories_normalised = []
filling_ratios = []
trap_density_values_by_T = []
trap_density_values_standard_temp = []
inventories_standard_temp = []
inventories_standard_temp_normalised = []
inventories_by_T = []
trap_density_values = []
trap_densities_contour = []
trap_densities_contour_1 = []
trap_densities_contour_2 = []
trap_densities_contour_3 = []
trap_densities_contour_4 = []
inventories_contour = []

for dpa in dpa_range:
    phi = dpa / (3600 * 24 * 365.25)
    (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
        phi=phi, T=761
    )
    # print("H rentention in case dpa = {} = {:.2e}".format(dpa, H_retention))
    inventory_per_dpa = []
    trap_densities_per_dpa = []
    for T in T_range:
        phi = dpa / (3600 * 24 * 365.25)
        (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
            phi=phi, T=T
        )
        inventory_per_dpa.append(H_retention)
        trap_densities_per_dpa.append(trap_densities[5])
    inventories.append(inventory_per_dpa)
    trap_density_values.append(trap_densities_per_dpa)


for dpa in alt_dpa_range:
    phi = dpa / (3600 * 24 * 365.25)
    (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
        phi=phi, T=761
    )
    inventories_standard_temp.append(H_retention)
    trap_density_values_standard_temp.append(trap_densities)

for dpa in dpa_range_contour:
    phi = dpa / (3600 * 24 * 365.25)
    trap_densities_temporary = []
    trap_densities_temporary_1 = []
    trap_densities_temporary_2 = []
    trap_densities_temporary_3 = []
    trap_densities_temporary_4 = []
    inventory_temp = []
    for T in T_range_contour:
        (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
            phi=phi, T=T
        )
        trap_densities_temporary.append(trap_densities[-1])
        trap_densities_temporary_1.append(trap_densities[-4])
        trap_densities_temporary_2.append(trap_densities[-3])
        trap_densities_temporary_3.append(trap_densities[-2])
        trap_densities_temporary_4.append(trap_densities[-1])
        inventory_temp.append(H_retention)
    trap_densities_contour.append(trap_densities_temporary)
    trap_densities_contour_1.append(trap_densities_temporary_1)
    trap_densities_contour_2.append(trap_densities_temporary_2)
    trap_densities_contour_3.append(trap_densities_temporary_3)
    trap_densities_contour_4.append(trap_densities_temporary_4)
    inventories_contour.append(inventory_temp)

for T in T_range:
    inventory_per_temp = []
    trap_densities_by_T = []
    for dpa in dpa_range:
        phi = dpa / (3600 * 24 * 365.25)
        (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
            phi=phi, T=T
        )
        inventory_per_temp.append(H_retention)
    inventories_by_T.append(inventory_per_temp)
    (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
        phi=9 / (3600 * 24 * 365.25), T=T
    )
    filling_ratios.append(trap_filling_ratios)
    trap_density_values_by_T.append(trap_densities)

contour_0_dpa_case = []
for T in T_range_contour:
    (H_retention, trap_densities, trap_filling_ratios) = analytical_model(phi=0, T=T)
    contour_0_dpa_case.append(H_retention)
contour_0_dpa_case = np.array(contour_0_dpa_case)

# ##### Post processing ##### #

for inv in inventories:
    normalised_values = np.array(inv) / np.array(inventories[0])
    inventories_normalised.append(normalised_values)

for inv in inventories_standard_temp:
    normalised_values = np.array(inv) / np.array(inventories_standard_temp[0])
    inventories_standard_temp_normalised.append(normalised_values)

trap_1_filling_ratios, trap_2_filling_ratios = [], []
trap_3_filling_ratios, trap_4_filling_ratios = [], []
trap_5_filling_ratios, trap_6_filling_ratios = [], []
trap_1_densities_standard_temp, trap_2_densities_standard_temp = [], []
trap_3_densities_standard_temp, trap_4_densities_standard_temp = [], []
trap_5_densities_standard_temp, trap_6_densities_standard_temp = [], []
total_trap_density = []
trap_1_densities_by_T, trap_2_densities_by_T = [], []
trap_3_densities_by_T, trap_4_densities_by_T = [], []
trap_5_densities_by_T, trap_6_densities_by_T = [], []
trap_1_densities, trap_2_densities = [], []
trap_3_densities, trap_4_densities = [], []
trap_5_densities, trap_6_densities = [], []


for ratios in filling_ratios:
    trap_1_filling_ratios.append(ratios[0])
    trap_2_filling_ratios.append(ratios[1])
    trap_3_filling_ratios.append(ratios[2])
    trap_4_filling_ratios.append(ratios[3])
    trap_5_filling_ratios.append(ratios[4])
    trap_6_filling_ratios.append(ratios[5])

for density in trap_density_values_standard_temp:
    trap_1_densities_standard_temp.append(density[0])
    trap_2_densities_standard_temp.append(density[1])
    trap_3_densities_standard_temp.append(density[2])
    trap_4_densities_standard_temp.append(density[3])
    trap_5_densities_standard_temp.append(density[4])
    trap_6_densities_standard_temp.append(density[5])

    total = density[0] + density[1] + density[2] + density[3] + density[4] + density[5]
    total_trap_density.append(total)

for density in trap_density_values_by_T:
    trap_1_densities_by_T.append(density[0])
    trap_2_densities_by_T.append(density[1])
    trap_3_densities_by_T.append(density[2])
    trap_4_densities_by_T.append(density[3])
    trap_5_densities_by_T.append(density[4])
    trap_6_densities_by_T.append(density[5])

trap_densities_contour = np.array(trap_densities_contour)
trap_densities_contour_1 = np.array(trap_densities_contour_1)
trap_densities_contour_2 = np.array(trap_densities_contour_2)
trap_densities_contour_3 = np.array(trap_densities_contour_3)
trap_densities_contour_4 = np.array(trap_densities_contour_4)

trap_densities_contour_1_normalised = (
    trap_densities_contour_1 / trap_densities_contour_1[-1]
)
trap_densities_contour_2_normalised = (
    trap_densities_contour_2 / trap_densities_contour_2[-1]
)
trap_densities_contour_3_normalised = (
    trap_densities_contour_3 / trap_densities_contour_3[-1]
)
trap_densities_contour_4_normalised = (
    trap_densities_contour_4 / trap_densities_contour_4[-1]
)
trap_densities_contour_1_normalised -= 1e-16
trap_densities_contour_2_normalised -= 1e-16
trap_densities_contour_3_normalised -= 1e-16
trap_densities_contour_4_normalised -= 1e-16

normalised_inventories_contour = []
inventories_contour = np.array(inventories_contour)
for inventory in inventories_contour:
    inventory = inventory / np.array(contour_0_dpa_case)
    normalised_inventories_contour.append(inventory)


########################
# ##### Plotting ##### #
########################

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)

# ##### Trap densities ##### #


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
    plt.figure()
    plt.plot(
        alt_dpa_range,
        trap_1_densities_standard_temp,
        label="Trap 1 (0.87 eV)",
        color="black",
    )
    plt.plot(
        alt_dpa_range,
        trap_2_densities_standard_temp,
        label="Trap 2 (1.00 eV)",
        color="grey",
    )
    plt.plot(
        alt_dpa_range,
        trap_3_densities_standard_temp,
        label="Trap D1 (1.15 eV)",
        color=firebrick,
    )
    plt.plot(
        alt_dpa_range,
        trap_4_densities_standard_temp,
        label="Trap D2 (1.35 eV)",
        color=electric_blue,
    )
    plt.plot(
        alt_dpa_range,
        trap_5_densities_standard_temp,
        label="Trap D3 (1.65 eV)",
        color=pewter_blue,
    )
    plt.plot(
        alt_dpa_range,
        trap_6_densities_standard_temp,
        label="Trap D4 (1.85 eV)",
        color=green_ryb,
    )
    plt.ylabel(r"Trap concentraion (m$^{-3}$)")
    plt.xlabel(r"Damage rate (dpa/fpy)")
    plt.xlim(alt_dpa_range[0], alt_dpa_range[-1])
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


def plot_trap_density_variation_with_damage_seconds_standard_temperature():
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


def plot_total_trap_density_variation_with_damage_standard_temperatrue():
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


# ##### filling ratios ###### #


def plot_filling_ratio_variation_with_temperature():
    plt.figure()
    plt.plot(T_range, trap_1_filling_ratios, label="Trap 1 (0.87 eV)")
    plt.plot(T_range, trap_2_filling_ratios, label="Trap 2 (1.00 eV)")
    plt.plot(T_range, trap_3_filling_ratios, label="Trap 3 (1.15 eV)")
    plt.plot(T_range, trap_4_filling_ratios, label="Trap 4 (1.35 eV)")
    plt.plot(T_range, trap_5_filling_ratios, label="Trap 5 (1.65 eV)")
    plt.plot(T_range, trap_6_filling_ratios, label="Trap 6 (1.85 eV)")
    plt.ylabel(r"Filling ratio")
    plt.xlabel(r"Temperature (K)")
    plt.xlim(400, 1300)
    plt.ylim(0, 1)
    plt.legend()
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


# ##### compare annelaing and detrapping ##### #


def plot_annealing_vs_detrapping():
    (
        trap_1_detrapping_rates,
        trap_2_detrapping_rates,
        trap_3_detrapping_rates,
        trap_4_detrapping_rates,
        trap_5_detrapping_rates,
        trap_6_detrapping_rates,
        annealing_rates,
    ) = compare_annealing_and_detrapping()

    plt.figure()
    # plt.plot(
    #     T_range, trap_1_detrapping_rates, color="blue", alpha=0.8, label="De-trapping"
    # )
    # plt.plot(T_range, trap_2_detrapping_rates, color="blue", alpha=0.7)
    plt.plot(T_range, trap_3_detrapping_rates, color="blue", alpha=0.3)
    plt.plot(T_range, trap_4_detrapping_rates, color="blue", alpha=0.5)
    plt.plot(T_range, trap_5_detrapping_rates, color="blue", alpha=0.7)
    plt.plot(
        T_range, trap_6_detrapping_rates, color="blue", alpha=0.9, label="De-trapping"
    )
    plt.plot(T_range, annealing_rates, color="black", label="Annealing")

    plt.annotate("1.15 eV", (1310, trap_3_detrapping_rates[-1] * 1.1), color="black")
    plt.annotate("1.35 eV", (1310, trap_4_detrapping_rates[-1] * 0.4), color="black")
    plt.annotate("1.65 eV", (1310, trap_5_detrapping_rates[-1] * 0.7), color="black")
    plt.annotate("1.85 eV", (1310, trap_6_detrapping_rates[-1] * 0.5), color="black")

    plt.yscale("log")
    plt.legend()
    plt.xlim(400, 1400)
    plt.ylabel(r"Trapped tritium removal rate (s$^{-1}$)")
    plt.xlabel(r"Temperature (K)")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()


# ##### standard temperature case ##### #


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


# ##### specify plots to output ##### #

# plot_trap_density_variation_with_temperature_standard_damage()
# plot_trap_density_variation_with_damage_standard_temperature()
# plot_trap_density_variation_with_damage_seconds_standard_temperature()
# plot_total_trap_density_variation_with_damage_standard_temperatrue()
# plot_trap_6_density_varitation_with_temperature_and_damage()
# plot_varying_trap_6_temp_and_damage(dpa_range_contour)
# plot_varying_all_traps_temp_and_damage(dpa_range_contour)
# plot_varying_all_traps_temp_and_damage_normalised(dpa_range_contour)
# plot_filling_ratio_variation_with_temperature()
# plot_annealing_vs_detrapping()
# plot_inventory_varying_damage_standard_temperature()
# plot_normalised_inventory_varying_temperature_standard_dpa()
plot_inventory_varying_temperature_and_damage()
# plot_normalised_inventory_varying_temperature_and_damage()
# plot_inventory_contour(dpa_range_contour)

plt.show()