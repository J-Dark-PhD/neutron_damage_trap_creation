from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint

from neutron_trap_creation_models import (
    neutron_trap_creation_numerical_beta,
    T_list,
    trap_2,
    t_annealing,
    atom_density_W,
    temperatures,
)

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

t = np.linspace(0, t_annealing, t_annealing)
phi = 0
K = 1
n_max = 1
A_0 = 0.006618356972644625
beta = 4.5944499958728266e-06
E_A = 0.2839061632941078

n_0 = 0.28e-02 * atom_density_W

annealed_trap_densities = []
for T in T_list:
    extra_args = (phi, K, n_max, A_0, beta, E_A, T)
    n_traps_annleaing = odeint(
        neutron_trap_creation_numerical_beta, n_0, t, args=extra_args
    )
    end_value = float(n_traps_annleaing[-1])
    annealed_trap_densities.append(end_value)

plt.figure()
at_fr_annealed_trap_densities = (np.array(annealed_trap_densities) / 6.3e28) * 100
plt.plot(T_list, at_fr_annealed_trap_densities, color="black")
plt.scatter(temperatures, trap_2, color="blue", marker="x")
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Annealing temperature (K)")
plt.ylim(0, 0.3)
plt.xlim(0, 1400)
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

plt.show()
