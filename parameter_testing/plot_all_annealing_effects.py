from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from labellines import labelLines

from neutron_trap_creation_models import (
    neutron_trap_creation_numerical,
    neutron_trap_creation_numerical_beta,
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
# ########## Just annealing stage ########## #
##############################################

# t = np.linspace(0, t_annealing, t_annealing)
# phi = 0
# K = 1
# n_max = 1
# A_0 = A_0_optimised
# E_A = E_A_optimised

# n_0 = 0.28e-02 * atom_density_W

# annealed_trap_densities = []
# for T in T_list:
#     extra_args = (phi, K, n_max, A_0, E_A, T)
#     n_traps_annleaing = odeint(neutron_trap_creation_numerical, n_0, t, args=extra_args)
#     end_value = float(n_traps_annleaing[-1])
#     annealed_trap_densities.append(end_value)

# plt.figure()
# at_fr_annealed_trap_densities = (np.array(annealed_trap_densities) / 6.3e28) * 100
# plt.plot(T_list, at_fr_annealed_trap_densities, color="black")
# plt.scatter(temperatures, trap_2, color="blue", marker="x")
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Annealing temperature (K)")
# plt.ylim(0, 0.3)
# plt.xlim(0, 1400)
# ax = plt.gca()
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)

# ##############################################
# # ############ Variation in E_A ############ #
# ##############################################

# t = np.linspace(0, t_annealing, t_annealing)
# phi = 0
# K = 1
# n_max = 1
# A_0 = A_0_optimised
# n_0 = 0.28e-02 * atom_density_W

# plt.figure()
# ax = plt.gca()
# E_A_values = np.linspace(0.2191 * 0.2, 0.2191 * 2, 10)
# for E_A in E_A_values:
#     annealed_trap_densities = []
#     for T in T_list:
#         extra_args = (phi, K, n_max, A_0, E_A, T)
#         n_traps_annleaing = odeint(
#             neutron_trap_creation_numerical, n_0, t, args=extra_args
#         )
#         end_value = float(n_traps_annleaing[-1])
#         annealed_trap_densities.append(end_value)
#     annealed_trap_densities = (np.array(annealed_trap_densities) / 6.3e28) * 100
#     plt.plot(T_list, annealed_trap_densities, label="{:.2f}".format(E_A), color="black")
# plt.scatter(temperatures, trap_2, color="blue", marker="x")
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Annealing Temperature (K)")
# plt.ylim(0, 0.3)
# plt.xlim(0, 1400)
# labelLines(plt.gca().get_lines())
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)

# ##############################################
# # ############ Variation in A_0 ############ #
# ##############################################

# t = np.linspace(0, t_annealing, t_annealing)
# phi = 0
# K = 1
# n_max = 1
# E_A = E_A_optimised
# n_0 = 0.28e-02 * atom_density_W

# plt.figure()
# ax = plt.gca()
# A_0_values = np.geomspace(2.5858e-03 * 0.1, 2.5858e-03 * 10, 10)
# for A_0 in A_0_values:
#     annealed_trap_densities = []
#     for T in T_list:
#         extra_args = (phi, K, n_max, A_0, E_A, T)
#         n_traps_annleaing = odeint(
#             neutron_trap_creation_numerical, n_0, t, args=extra_args
#         )
#         end_value = float(n_traps_annleaing[-1])
#         annealed_trap_densities.append(end_value)
#     annealed_trap_densities = (np.array(annealed_trap_densities) / 6.3e28) * 100
#     plt.plot(
#         T_list,
#         annealed_trap_densities,
#         label="{:.2f}".format(A_0 * 1e03),
#         color="black",
#     )
# plt.scatter(temperatures, trap_2, color="blue", marker="x")
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Annealing Temperature (K)")
# plt.ylim(0, 0.3)
# plt.xlim(0, 1400)
# labelLines(plt.gca().get_lines())
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)

# ##############################################
# # ############# Variation in T ############# #
# ##############################################

# t = np.linspace(0, t_annealing, t_annealing)
# phi = 0
# K = 1
# n_max = 1
# A_0 = A_0_optimised
# E_A = E_A_optimised
# n_0 = 0.28e-02 * atom_density_W

# plt.figure()
# ax = plt.gca()
# for T in temperatures:
#     extra_args = (phi, K, n_max, A_0, E_A, T)
#     n_traps_annleaing = odeint(neutron_trap_creation_numerical, n_0, t, args=extra_args)
#     plt.plot(t, n_traps_annleaing, label="{}K".format(int(T)), color="black")

# plt.ylim(bottom=0)
# plt.xlim(0, t_annealing)
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Time (s)")
# plt.xticks([])
# ax = plt.gca()
# labelLines(plt.gca().get_lines())
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)

# ##############################################
# # ########### plot Etienne data ############ #
# ##############################################

# plt.figure()
# ax = plt.gca()
# plt.scatter(temperatures, trap_1, color="blue", marker="x", label=r"trap 1")
# plt.scatter(temperatures, trap_2, color="black", marker="x", label=r"trap 2")
# plt.scatter(temperatures, trap_3, color="red", marker="x", label=r"trap 3")
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Annealing Temperature (K)")
# plt.ylim(0, 0.3)
# plt.xlim(0, 1400)
# plt.legend()
# ax = plt.gca()
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)

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
for T in T_list:
    extra_args = (phi, K, n_max, A_0, E_A, T)
    n_traps_annleaing = odeint(
        neutron_trap_creation_numerical, n_0_trap1, t, args=extra_args
    )
    end_value = float(n_traps_annleaing[-1])
    annealed_trap_1_densities.append(end_value)

# plt.figure()
annealed_trap_1_densities = (np.array(annealed_trap_1_densities) / 6.3e28) * 100
# plt.plot(T_list, annealed_trap_1_densities, color="black")
# plt.scatter(temperatures, trap_1, color="blue", marker="x")
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Annealing temperature (K)")
# plt.ylim(bottom=0)
# plt.xlim(0, 1400)
# ax = plt.gca()
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)

annealed_trap_2_densities = []
for T in T_list:
    extra_args = (phi, K, n_max, A_0, E_A, T)
    n_traps_annleaing = odeint(
        neutron_trap_creation_numerical, n_0_trap2, t, args=extra_args
    )
    end_value = float(n_traps_annleaing[-1])
    annealed_trap_2_densities.append(end_value)

# plt.figure()
annealed_trap_2_densities = (np.array(annealed_trap_2_densities) / 6.3e28) * 100
# plt.plot(T_list, annealed_trap_2_densities, color="black")
# plt.scatter(temperatures, trap_2, color="blue", marker="x")
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Annealing temperature (K)")
# plt.ylim(bottom=0)
# plt.xlim(0, 1400)
# ax = plt.gca()
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)

annealed_trap_3_densities = []
for T in T_list:
    extra_args = (phi, K, n_max, A_0, E_A, T)
    n_traps_annleaing = odeint(
        neutron_trap_creation_numerical, n_0_trap3, t, args=extra_args
    )
    end_value = float(n_traps_annleaing[-1])
    annealed_trap_3_densities.append(end_value)

# plt.figure()
annealed_trap_3_densities = (np.array(annealed_trap_3_densities) / 6.3e28) * 100
# plt.plot(T_list, annealed_trap_3_densities, color="black")
# plt.scatter(temperatures, trap_3, color="blue", marker="x")
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Annealing temperature (K)")
# plt.ylim(bottom=0)
# plt.xlim(0, 1400)
# ax = plt.gca()
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)


# plot all on one
plt.figure()
# plt.plot(
#     T_list,
#     annealed_trap_1_densities,
#     color=pewter_blue,
#     label=r"Trap 3 ($E_{t} = 1.65 eV$)",
# )
# plt.scatter(temperatures, trap_1, color=pewter_blue, marker="x")

trap_2_err = np.array(trap_2) * 0.1
err_bar_1 = plt.errorbar(
    temperatures,
    trap_2,
    yerr=trap_2_err,
    fmt=".",
    capsize=5,
    color=firebrick,
    label=r"Trap 4 ($E_{t} = 2.10$ eV)",
)

plt.plot(
    T_list,
    annealed_trap_2_densities,
    color=firebrick,
    label=r"Trap 4 fitting ($A_{0} = 0.28$ eV, $E_{A} = 6.18 \cdot 10^{-3}$ s$^{-1}$)",
)
# plt.scatter(
#     temperatures,
#     trap_2,
#     color=blue_jeans,
#     marker="x",
#     label=r"Trap 4 ($E_{t} = 1.85 eV$)",
# )
# plt.plot(
#     T_list,
#     annealed_trap_3_densities,
#     color=electric_blue,
#     label=r"Trap 5 ($E_{t} = 2.06 eV$)",
# )
# plt.scatter(temperatures, trap_3, color=electric_blue, marker="x")
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Annealing temperature (K)")
plt.ylim(0, 0.4)
plt.xlim(0, 1400)
plt.legend(loc="upper right")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

##############################################
# ########## Just annealing stage ########## #
# ########### with beta variable ########### #
##############################################

# t = np.linspace(0, t_annealing, t_annealing)
# phi = 0
# K = 1
# n_max = 1
# A_0 = 0.006618356972644625
# beta = 4.5944499958728266e-06
# E_A = 0.2839061632941078

# n_0 = 0.28e-02 * atom_density_W

# annealed_trap_densities = []
# for T in T_list:
#     extra_args = (phi, K, n_max, A_0, beta, E_A, T)
#     n_traps_annleaing = odeint(
#         neutron_trap_creation_numerical_beta, n_0, t, args=extra_args
#     )
#     end_value = float(n_traps_annleaing[-1])
#     annealed_trap_densities.append(end_value)

# plt.figure()
# at_fr_annealed_trap_densities = (np.array(annealed_trap_densities) / 6.3e28) * 100
# plt.plot(T_list, at_fr_annealed_trap_densities, color="black")
# plt.scatter(temperatures, trap_2, color="blue", marker="x")
# plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
# plt.xlabel(r"Annealing temperature (K)")
# plt.ylim(0, 0.3)
# plt.xlim(0, 1400)
# ax = plt.gca()
# ax.spines["right"].set_visible(False)
# ax.spines["top"].set_visible(False)

##############################################
# ################ plot show ############### #
##############################################

plt.show()
