from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from labellines import labelLines

from neutron_trap_creation_models import (
    neutron_trap_creation_numerical,
    t_annealing,
    E_A_optimised,
    atom_density_W,
    temperatures,
    trap_2,
    T_list,
)

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

t = np.linspace(0, t_annealing, t_annealing)
phi = 0
K = 1
n_max = 1
E_A = E_A_optimised
n_0 = 0.28e-02 * atom_density_W

plt.figure()
ax = plt.gca()
A_0_values = np.geomspace(2.5858e-03 * 0.1, 2.5858e-03 * 10, 10)
for A_0 in A_0_values:
    annealed_trap_densities = []
    for T in T_list:
        extra_args = (phi, K, n_max, A_0, E_A, T)
        n_traps_annleaing = odeint(
            neutron_trap_creation_numerical, n_0, t, args=extra_args
        )
        end_value = float(n_traps_annleaing[-1])
        annealed_trap_densities.append(end_value)
    annealed_trap_densities = (np.array(annealed_trap_densities) / 6.3e28) * 100
    plt.plot(
        T_list,
        annealed_trap_densities,
        label="{:.2f}".format(A_0 * 1e03),
        color="black",
    )
plt.scatter(temperatures, trap_2, color="blue", marker="x")
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Annealing Temperature (K)")
plt.ylim(0, 0.3)
plt.xlim(0, 1400)
labelLines(plt.gca().get_lines())
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

plt.show()
