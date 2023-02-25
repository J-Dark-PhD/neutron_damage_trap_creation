import numpy as np


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
testing_T_range = np.linspace(400, 1300, num=50)
T_range_contour = np.linspace(400, 1300, num=100)
dpa_range = [0, 0.001, 0.01, 0.1, 1, 10, 100]
alt_dpa_range = np.geomspace(1e-03, 1e03, num=1000)
dpa_range_contour = np.geomspace(1e-3, 1e03, num=100)
test_dpa_range = np.geomspace(1e-3, 1e03, num=50)

# ##### analytical test results gathering ##### #


inventories = []
inventories_alt = []
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

for dpa in test_dpa_range:
    inventory_per_dpa_alt = []
    for T in testing_T_range:
        phi = dpa / (3600 * 24 * 365.25)
        (H_retention, trap_densities, trap_filling_ratios) = analytical_model(
            phi=phi, T=T
        )
        inventory_per_dpa_alt.append(H_retention)
    inventories_alt.append(inventory_per_dpa_alt)

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

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)
