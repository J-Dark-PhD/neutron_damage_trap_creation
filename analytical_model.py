import numpy as np

# ##### standard values ##### #

L = 0.002
k_B = 8.6173303e-5
imp_flux = 1e20
r_p = 3e-09
fpy = 3600 * 24 * 365.25

# diffusion parameters
D_0 = 4.1e-7
E_D = 0.39

# annealing parameters
A_0 = 6.18e-03
E_A = 0.28

# general trap parameters
k_0 = 5.22e-17
p_0 = 1e13
trap_1_density = 2e22


def trap_density(T, phi, K, n_max, A_0, E_A):
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


def analytical_model(phi=9 / fpy, T=700, L=0.002):
    trap_d1_density = trap_density(
        T=T, phi=phi, K=1.5e28, n_max=5.2e25, A_0=A_0, E_A=E_A
    )
    trap_d2_density = trap_density(
        T=T, phi=phi, K=4.0e27, n_max=4.5e25, A_0=A_0, E_A=E_A
    )
    trap_d3_density = trap_density(
        T=T, phi=phi, K=3.0e27, n_max=4.0e25, A_0=A_0, E_A=E_A
    )
    trap_d4_density = trap_density(
        T=T, phi=phi, K=9.0e27, n_max=4.2e25, A_0=A_0, E_A=E_A
    )

    c_m = mobile_H_concentration(T=T, imp_flux=imp_flux, r_p=r_p, D_0=D_0, E_D=E_D)

    c_t_1, filling_ratio_1 = trapped_H_concentration(
        c_m=c_m, k_0=k_0, E_k=E_D, p_0=p_0, E_p=0.87, n_i=trap_1_density, T=T
    )
    c_t_d1, filling_ratio_d1 = trapped_H_concentration(
        c_m=c_m,
        k_0=k_0,
        E_k=E_D,
        p_0=p_0,
        E_p=1.15,
        A_0=A_0,
        E_A=E_A,
        n_i=trap_d1_density,
        T=T,
    )
    c_t_d2, filling_ratio_d2 = trapped_H_concentration(
        c_m=c_m,
        k_0=k_0,
        E_k=E_D,
        p_0=p_0,
        E_p=1.35,
        A_0=A_0,
        E_A=E_A,
        n_i=trap_d2_density,
        T=T,
    )
    c_t_d3, filling_ratio_d3 = trapped_H_concentration(
        c_m=c_m,
        k_0=k_0,
        E_k=E_D,
        p_0=p_0,
        E_p=1.65,
        A_0=A_0,
        E_A=E_A,
        n_i=trap_d3_density,
        T=T,
    )
    c_t_d4, filling_ratio_d4 = trapped_H_concentration(
        c_m=c_m,
        k_0=k_0,
        E_k=E_D,
        p_0=p_0,
        E_p=1.85,
        A_0=A_0,
        E_A=E_A,
        n_i=trap_d4_density,
        T=T,
    )

    trap_densities = [
        trap_1_density,
        trap_d1_density,
        trap_d2_density,
        trap_d3_density,
        trap_d4_density,
    ]

    trap_filling_ratios = [
        filling_ratio_1,
        filling_ratio_d1,
        filling_ratio_d2,
        filling_ratio_d3,
        filling_ratio_d4,
    ]

    total_trapped_H_concentration = c_t_1 + c_t_d1 + c_t_d2 + c_t_d3 + c_t_d4

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
    trap_d1_detrapping_rates = []
    trap_d2_detrapping_rates = []
    trap_d3_detrapping_rates = []
    trap_d4_detrapping_rates = []
    annealing_rates = []
    for T in T_range:
        trap_1_detrapping = de_trapping_rate(E_p=1.00, T=T)
        trap_d1_detrapping = de_trapping_rate(E_p=1.15, T=T)
        trap_d2_detrapping = de_trapping_rate(E_p=1.35, T=T)
        trap_d3_detrapping = de_trapping_rate(E_p=1.65, T=T)
        trap_d4_detrapping = de_trapping_rate(E_p=1.85, T=T)
        annealing = annealing_rate(T=T)

        trap_1_detrapping_rates.append(trap_1_detrapping)
        trap_d1_detrapping_rates.append(trap_d1_detrapping)
        trap_d2_detrapping_rates.append(trap_d2_detrapping)
        trap_d3_detrapping_rates.append(trap_d3_detrapping)
        trap_d4_detrapping_rates.append(trap_d4_detrapping)
        annealing_rates.append(annealing)

    return (
        trap_1_detrapping_rates,
        trap_d1_detrapping_rates,
        trap_d2_detrapping_rates,
        trap_d3_detrapping_rates,
        trap_d4_detrapping_rates,
        annealing_rates,
    )


# ##### test ranges ##### #

T_range = np.linspace(400, 1300, num=50)
dpa_range = np.geomspace(1e-5, 1e03, num=10)
T_range_contour = np.linspace(400, 1300, num=100)
dpa_range_contour = np.geomspace(1e-3, 1e03, num=100)

# ##### analytical test results gathering ##### #

inventories = []
inventories_no_damage = []
inventories_normalised = []
inventories_standard_temp = []
inventories_standard_temp_normalised = []
inventories_contour = []
filling_ratios = []
trap_d1_densities = []
trap_d2_densities = []
trap_d3_densities = []
trap_d4_densities = []
trap_d1_densities_contour = []
trap_d2_densities_contour = []
trap_d3_densities_contour = []
trap_d4_densities_contour = []
trap_1_detrapping_rates = []
trap_d1_detrapping_rates = []
trap_d2_detrapping_rates = []
trap_d3_detrapping_rates = []
trap_d4_detrapping_rates = []
annealing_rates = []

# for dpa in dpa_range:
#     phi = dpa / fpy
#     (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
#         phi=phi, T=761
#     )
#     inventory_per_dpa = []
#     trap_densities_per_dpa = []
#     for T in T_range:
#         phi = dpa / fpy
#         (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
#             phi=phi, T=T
#         )
#         inventory_per_dpa.append(H_retention)
#     inventories.append(inventory_per_dpa)

# for dpa in dpa_range_contour:
#     phi = dpa / fpy
#     trap_d1_densities_per_dpa = []
#     trap_d2_densities_per_dpa = []
#     trap_d3_densities_per_dpa = []
#     trap_d4_densities_per_dpa = []
#     inventory_per_dpa = []
#     for T in T_range_contour:
#         (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
#             phi=phi, T=T
#         )
#         trap_d1_densities_per_dpa.append(trap_densities[1])
#         trap_d2_densities_per_dpa.append(trap_densities[2])
#         trap_d3_densities_per_dpa.append(trap_densities[3])
#         trap_d4_densities_per_dpa.append(trap_densities[4])
#         inventory_per_dpa.append(H_retention)
#     trap_densities_contour_1.append(trap_densities_temporary_1)
#     trap_densities_contour_2.append(trap_densities_temporary_2)
#     trap_densities_contour_3.append(trap_densities_temporary_3)
#     trap_densities_contour_4.append(trap_densities_temporary_4)
#     inventories_contour.append(inventory_temp)

# for T in T_range:
#     inventory_per_temp = []
#     trap_densities_by_T = []
#     for dpa in dpa_range:
#         phi = dpa / (3600 * 24 * 365.25)
#         (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
#             phi=phi, T=T
#         )
#         inventory_per_temp.append(H_retention)
#     inventories_by_T.append(inventory_per_temp)
#     (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
#         phi=9 / (3600 * 24 * 365.25), T=T
#     )
#     filling_ratios.append(trap_filling_ratios)
#     trap_density_values_by_T.append(trap_densities)

# contour_0_dpa_case = []
# for T in T_range_contour:
#     (H_retention, trap_densities, trap_filling_ratios) = analytical_model(phi=0, T=T)
#     contour_0_dpa_case.append(H_retention)
# contour_0_dpa_case = np.array(contour_0_dpa_case)

for T in T_range:
    dpa = 10
    phi = dpa / fpy
    (H_retention, trap_densities, trap_filling_ratios) = analytical_model(phi=phi, T=T)
    filling_ratios.append(trap_filling_ratios)

    trap_1_detrapping_rates.append(de_trapping_rate(E_p=1.00, T=T))
    trap_d1_detrapping_rates.append(de_trapping_rate(E_p=1.15, T=T))
    trap_d2_detrapping_rates.append(de_trapping_rate(E_p=1.35, T=T))
    trap_d3_detrapping_rates.append(de_trapping_rate(E_p=1.65, T=T))
    trap_d4_detrapping_rates.append(de_trapping_rate(E_p=1.85, T=T))
    annealing_rates.append(annealing_rate(T=T))

# ##### Post processing ##### #

# for inv in inventories:
#     normalised_values = np.array(inv) / np.array(inventories[0])
#     inventories_normalised.append(normalised_values)

# for inv in inventories_standard_temp:
#     normalised_values = np.array(inv) / np.array(inventories_standard_temp[0])
#     inventories_standard_temp_normalised.append(normalised_values)

trap_1_filling_ratios = []
trap_d1_filling_ratios, trap_d2_filling_ratios = [], []
trap_d3_filling_ratios, trap_d4_filling_ratios = [], []
# trap_1_densities_standard_temp, trap_2_densities_standard_temp = [], []
# trap_3_densities_standard_temp, trap_4_densities_standard_temp = [], []
# trap_5_densities_standard_temp, trap_6_densities_standard_temp = [], []
# total_trap_density = []
# trap_1_densities_by_T, trap_2_densities_by_T = [], []
# trap_3_densities_by_T, trap_4_densities_by_T = [], []
# trap_5_densities_by_T, trap_6_densities_by_T = [], []
# trap_1_densities, trap_2_densities = [], []
# trap_3_densities, trap_4_densities = [], []
# trap_5_densities, trap_6_densities = [], []


for ratios in filling_ratios:
    trap_1_filling_ratios.append(ratios[0])
    trap_d1_filling_ratios.append(ratios[1])
    trap_d2_filling_ratios.append(ratios[2])
    trap_d3_filling_ratios.append(ratios[3])
    trap_d4_filling_ratios.append(ratios[4])

# for density in trap_density_values_standard_temp:
#     trap_1_densities_standard_temp.append(density[0])
#     trap_2_densities_standard_temp.append(density[1])
#     trap_3_densities_standard_temp.append(density[2])
#     trap_4_densities_standard_temp.append(density[3])
#     trap_5_densities_standard_temp.append(density[4])
#     trap_6_densities_standard_temp.append(density[5])

#     total = density[0] + density[1] + density[2] + density[3] + density[4] + density[5]
#     total_trap_density.append(total)

# for density in trap_density_values_by_T:
#     trap_1_densities_by_T.append(density[0])
#     trap_2_densities_by_T.append(density[1])
#     trap_3_densities_by_T.append(density[2])
#     trap_4_densities_by_T.append(density[3])
#     trap_5_densities_by_T.append(density[4])
#     trap_6_densities_by_T.append(density[5])

# trap_densities_contour = np.array(trap_densities_contour)
# trap_densities_contour_1 = np.array(trap_densities_contour_1)
# trap_densities_contour_2 = np.array(trap_densities_contour_2)
# trap_densities_contour_3 = np.array(trap_densities_contour_3)
# trap_densities_contour_4 = np.array(trap_densities_contour_4)

# trap_densities_contour_1_normalised = (
#     trap_densities_contour_1 / trap_densities_contour_1[-1]
# )
# trap_densities_contour_2_normalised = (
#     trap_densities_contour_2 / trap_densities_contour_2[-1]
# )
# trap_densities_contour_3_normalised = (
#     trap_densities_contour_3 / trap_densities_contour_3[-1]
# )
# trap_densities_contour_4_normalised = (
#     trap_densities_contour_4 / trap_densities_contour_4[-1]
# )
# trap_densities_contour_1_normalised -= 1e-16
# trap_densities_contour_2_normalised -= 1e-16
# trap_densities_contour_3_normalised -= 1e-16
# trap_densities_contour_4_normalised -= 1e-16

# normalised_inventories_contour = []
# inventories_contour = np.array(inventories_contour)
# for inventory in inventories_contour:
#     inventory = inventory / np.array(contour_0_dpa_case)
#     normalised_inventories_contour.append(inventory)

# ##### Export results ##### #

results_folder = "Results/analytical_model_testing/"

np.savetxt(
    results_folder + "T_range.csv",
    T_range,
    delimiter=",",
)

# annealing vs detrapping
annealing_detrapping_results = [
    trap_1_detrapping_rates,
    trap_d1_detrapping_rates,
    trap_d2_detrapping_rates,
    trap_d3_detrapping_rates,
    trap_d4_detrapping_rates,
    annealing_rates,
]
annealing_detrapping_case_names = [
    "trap_1_detrapping_rates",
    "trap_d1_detrapping_rates",
    "trap_d2_detrapping_rates",
    "trap_d3_detrapping_rates",
    "trap_d4_detrapping_rates",
    "annealing_rates",
]
for case, filename in zip(
    annealing_detrapping_results, annealing_detrapping_case_names
):
    np.savetxt(
        results_folder + "{}.csv".format(filename),
        case,
        delimiter=",",
    )

# filling ratio variation
filling_ratio_results = [
    trap_1_filling_ratios,
    trap_d1_filling_ratios,
    trap_d2_filling_ratios,
    trap_d3_filling_ratios,
    trap_d4_filling_ratios,
]
filling_ratio_case_names = [
    "trap_1_filling_ratios",
    "trap_d1_filling_ratios",
    "trap_d2_filling_ratios",
    "trap_d3_filling_ratios",
    "trap_d4_filling_ratios",
]
for case, filename in zip(filling_ratio_results, filling_ratio_case_names):
    np.savetxt(
        results_folder + "{}.csv".format(filename),
        case,
        delimiter=",",
    )
