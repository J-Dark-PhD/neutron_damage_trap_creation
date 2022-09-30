from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint

from neutron_trap_creation_models import (
    neutron_trap_creation_numerical,
    A_0_optimised,
    E_A_optimised,
)

fpy = 3600 * 24 * 365.25
t = 3600 * 24 * 3
phi = 1 / fpy
K = 6.0e26
n_max = 4.5e25
A_0 = A_0_optimised
E_A = E_A_optimised
T_list = np.linspace(400, 1300, 19)
n_0 = 0

annealed_trap_1_densities = []
for T in T_list:
    extra_args = (phi, K, n_max, A_0, E_A, T)
    n_traps_annleaing = odeint(neutron_trap_creation_numerical, n_0, t, args=extra_args)
    end_value = float(n_traps_annleaing[-1])
    annealed_trap_1_densities.append(end_value)

annealed_trap_1_densities = (np.array(annealed_trap_1_densities) / 6.3e28) * 100

plt.figure()
plt.plot(
    T_list,
    annealed_trap_1_densities,
    # color=firebrick,
    label=r"Trap 1 fitting ($A_{0} = 0.28$ eV, $E_{A} = 6.18 \cdot 10^{-3}$ s$^{-1}$)",
)
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Annealing temperature (K)")
# plt.ylim(0, 0.4)
plt.xlim(0, 1400)
plt.legend(loc="upper right")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
