import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve
from scipy.interpolate import interp1d

from neutron_trap_creation_models import (
    damage_then_annealing,
    neutron_trap_creation_analytical,
    neutron_trap_creation_numerical,
    t_total,
    t_damage,
    A_0_optimised,
    E_A_optimised,
    T_list,
    temperatures,
    trap_2,
    atom_density_W,
    trap1,
    trap2,
    trap3,
    trap4,
    dpa_list,
    dpa_values,
)

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)

##############################################
# ##### Plot for single standard case ###### #
# #### With damage and annealing stages #### #
##############################################

t = np.linspace(0, t_total, t_total)
phi = 0.5 / t_damage
K = 3.5e28
A_0 = A_0_optimised
E_A = E_A_optimised
n_max = 1e40
T = 298
T_annealing = 1200
extra_args = (t_damage, phi, K, n_max, A_0, E_A, T, T_annealing)
n_0 = 0

plt.figure()
n_traps = odeint(damage_then_annealing, n_0, t, args=extra_args)
plt.plot(t, n_traps, color="black")
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$")
plt.xlabel(r"Time (s)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

##############################################
# ##### Just annealing stage comparison ##### #
##############################################

damaged_trap_densities = []
phi = 9.64e-7
A_0 = A_0_optimised
E_A = E_A_optimised
T = 298
n_0 = 0

K = 3.6402e28
n_max = 5.0924e35

t = np.linspace(0, t_total, t_total)

for T_annealing in T_list:
    extra_args = (t_damage, phi, K, n_max, A_0, E_A, T, T_annealing)
    n_traps_damaging = odeint(damage_then_annealing, n_0, t, args=extra_args)
    end_value = float(n_traps_damaging[-1])
    damaged_trap_densities.append(end_value)

plt.figure()
damaged_trap_densities = np.array(damaged_trap_densities) / 6.3e28
plt.plot(T_list, damaged_trap_densities, color="black")
plt.scatter(temperatures, trap_2, color="blue", marker="x")
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Annealing temperature (K)")
plt.ylim(0, 0.3)
plt.xlim(0, 1400)
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

##############################################
# ########## varying K and n_max ########### #
##############################################


def function_to_solve(n_max, K):
    """
    Equation: f(t=t_damage) = 0.28e-02*atom_density_W
    or
    f(t=t_damage) - 0.28e-02*atom_density_W = 0
    where f is the analytical_model function

    Find a minimum value of n_max to satisfy the equation for a given
    time t
    """
    t = t_damage
    n_t = 0.28e-02 * atom_density_W
    return neutron_trap_creation_analytical(t, K, n_max) - n_t


t = np.linspace(0, t_damage, t_damage)

plt.figure()
K_min = 3.7e26
K_max = 2e28
for K in np.geomspace(K_min, K_max, 10):
    n_max = fsolve(function_to_solve, x0=1e26, args=(K))
    n_t = neutron_trap_creation_analytical(t, K, n_max)
    if n_t[-1] < 0.999 * 0.28e-2 * atom_density_W:
        print("K = {} is not valid".format(K))
        continue
    # plt.plot(t, n_t, label="K = {}, nmax = {}".format(K, n_max[0]))
    plt.plot(t, n_t, color="black")

plt.xlim(left=0)
# plt.ylim(0, 2e28)
plt.ylim(bottom=0)
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$")
plt.xlabel(r"Time (s)")
ax = plt.gca()
# plt.legend()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

# ##### Figure showing range of K and n_max values ##### #
K_values = []
n_max_values = []
for K in np.geomspace(K_min, K_max, 100):
    K_values.append(K)
    n_max = fsolve(function_to_solve, x0=1e26, args=(K))
    n_max_values.append(int(n_max))
plt.figure()
plt.plot(K_values, n_max_values, color="black")
plt.xscale("log")
plt.yscale("log")
plt.xlabel(r"K")
plt.ylim(1e26, 1e28)
plt.xlim(1e26, 1e29)
plt.ylabel(r"n$_{\mathrm{max}}$")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

##############################################
# ########## varying phi with x ########### #
##############################################

data_dist = np.genfromtxt("damage_profile.csv", delimiter=",", names=True)
x = data_dist["x"]
dpa = data_dist["dpa"]

plt.figure()
plt.scatter(x, dpa, marker="x", color="black")
plt.ylim(0, 0.6)
plt.xlim(left=0)
plt.ylabel(r"Damage (dpa)")
plt.xlabel(r"x (m)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

##############################################
# ########## varying flux of phi ########### #
##############################################
fluence = 20

phi_1 = 1
phi_2 = 2

t_damage_1 = fluence / phi_1
t_damage_2 = fluence / phi_2

t_1 = np.linspace(0, t_damage_1, int(1e05))
t_2 = np.linspace(0, t_damage_2, int(1e05))
K = 3.5e28
A_0 = A_0_optimised
E_A = E_A_optimised
n_max = 1e40
T = 298
T_annealing = 1200
extra_args_1 = (t_damage_1, phi_1, K, n_max, A_0, E_A, T, T_annealing)
extra_args_2 = (t_damage_2, phi_2, K, n_max, A_0, E_A, T, T_annealing)
n_0 = 0

plt.figure()
n_traps_1 = odeint(damage_then_annealing, n_0, t_1, args=extra_args_1)
n_traps_2 = odeint(damage_then_annealing, n_0, t_2, args=extra_args_2)
plt.plot(t_1 * phi_1, n_traps_1, color="black")
plt.plot(t_2 * phi_2, n_traps_2, color="red")
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$")
plt.xlabel(r"Fluence (dpa)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

print("time_1 = ", float(n_traps_1[-1]))
print("time_2 = ", float(n_traps_2[-1]))
difference = (n_traps_2[-1] - n_traps_1[-1]) * 100 / n_traps_1[-1]
print("difference = ", float(difference), "%")

##############################################
# ######## fitting for K and n_max ######### #
##############################################

data_dmg = np.genfromtxt("damage_dpa_t_selinger.csv", delimiter=",", names=True)
x_data = np.array(data_dmg["x"])
dpa_data = np.array(data_dmg["dpa"])
dpa_data = dpa_data / dpa_data.max()
interp_func = interp1d(x_data, dpa_data, fill_value="extrapolate")
x = np.linspace(0, x_data.max(), 1000)

t_damage = 86400
t = np.linspace(0, t_damage, t_damage)
A_0 = A_0_optimised  # optimised value
E_A = E_A_optimised  # optimised value
T = 370
n_0 = 0

trap1_K = 8.0e21
trap1_n_max = 4.5e25
trap2_K = 5.0e21
trap2_n_max = 3.1e25
trap3_K = 3.7e21
trap3_n_max = 2.5e25
trap4_K = 7.0e21
trap4_n_max = 6.0e25

phi = 2.5
K = 5e21
n_max = 3.1e25

damaged_trap1_densities = []
damaged_trap2_densities = []
damaged_trap3_densities = []
damaged_trap4_densities = []

dpa_list = np.linspace(0, 3, num=200)
for dpa in dpa_list:
    phi = dpa
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

plt.figure()

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
    label=r"Trap 2 fitting ($K = 8.0 \cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  4.5\cdot 10^{25}$ m$^{-3}$)",
)

# trap 2
plt.errorbar(
    dpa_values,
    trap2,
    yerr=trap2_err,
    fmt=".",
    color=electric_blue,
    capsize=5,
    label=r"Trap 3 ($E_{t} = 1.30$ eV)",
)
plt.plot(
    dpa_list,
    damaged_trap2_densities,
    color=electric_blue,
    label=r"Trap 3 fitting ($K = 5 \cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  3.1\cdot 10^{25}$ m$^{-3}$)",
)

# trap 3
plt.errorbar(
    dpa_values,
    trap3,
    yerr=trap3_err,
    fmt=".",
    capsize=5,
    color=pewter_blue,
    label=r"Trap 4 ($E_{t} = 1.50$ eV)",
)
plt.plot(
    dpa_list,
    damaged_trap3_densities,
    color=pewter_blue,
    label=r"Trap 4 fitting ($K = 3.7\cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  2.5\cdot 10^{25}$ m$^{-3}$)",
)

# trap 4
err_bar_2 = plt.errorbar(
    dpa_values,
    trap4,
    yerr=trap4_err,
    fmt=".",
    capsize=5,
    color=green_ryb,
    label=r"Trap 5 ($E_{t} = 1.85$ eV)",
)
plot_2 = plt.plot(
    dpa_list,
    damaged_trap4_densities,
    color=green_ryb,
    label=r"Trap 5 fitting ($K = 7\cdot 10^{26}$ s$^{-1}$, $n_{max, \phi} =  6\cdot 10^{25}$ m$^{-3}$) ",
)

# plt.xscale("log")
plt.ylim(bottom=0)
plt.xlim(0, 3)
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (m$^{-3}$)")
plt.xlabel(r"Damage (dpa)")

h, l = plt.gca().get_legend_handles_labels()
plt.legend([h[3], h[1], h[2], h[0]], [l[3], l[1], l[2], l[0]])
# plt.legend()
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
plt.tight_layout()

##############################################
# ################ plot show ############### #
##############################################

plt.show()
