from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint

from neutron_trap_creation_models import (
    damage_then_annealing,
    t_damage,
    A_0_optimised,
    E_A_optimised,
    t_total,
)

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

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

plt.show()
