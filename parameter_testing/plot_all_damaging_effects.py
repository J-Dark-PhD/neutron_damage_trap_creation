import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve

from neutron_trap_creation_models import (
    damage_then_annealing,
    neutron_trap_creation_analytical,
    t_total,
    t_damage,
    A_0_optimised,
    E_A_optimised,
    T_list,
    temperatures,
    trap_2,
    atom_density_W,
)

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)


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
# ################ plot show ############### #
##############################################

plt.show()
