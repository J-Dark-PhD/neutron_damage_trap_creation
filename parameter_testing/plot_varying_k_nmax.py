from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import fsolve

from neutron_trap_creation_models import (
    neutron_trap_creation_analytical,
    t_damage,
    atom_density_W,
)

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)


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

plt.show()
