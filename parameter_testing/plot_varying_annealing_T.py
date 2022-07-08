from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from labellines import labelLines

from neutron_trap_creation_models import (
    neutron_trap_creation_numerical,
    t_annealing,
    A_0_optimised,
    E_A_optimised,
    atom_density_W,
    temperatures,
)

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

t = np.linspace(0, t_annealing, t_annealing)
phi = 0
K = 1
n_max = 1
A_0 = A_0_optimised
E_A = E_A_optimised
n_0 = 0.28e-02 * atom_density_W

plt.figure()
ax = plt.gca()
for T in temperatures:
    extra_args = (phi, K, n_max, A_0, E_A, T)
    n_traps_annleaing = odeint(neutron_trap_creation_numerical, n_0, t, args=extra_args)
    plt.plot(t, n_traps_annleaing, label="{}K".format(int(T)), color="black")

plt.ylim(bottom=0)
plt.xlim(0, t_annealing)
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Time (s)")
plt.xticks([])
ax = plt.gca()
labelLines(plt.gca().get_lines())
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

plt.show()
