from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint

from neutron_trap_creation_models import (
    damage_then_annealing,
    A_0_optimised,
    E_A_optimised,
)

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

fluence = 20

phi_1 = 1
phi_2 = 500

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
plt.plot(t_1 * phi_1, n_traps_1, color="black", linewidth=6, label="Phi_1")
plt.plot(t_2 * phi_2, n_traps_2, color="red", label="Phi_2")
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.legend()
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$")
plt.xlabel(r"Fluence (dpa)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

print("time_1 = ", float(n_traps_1[-1]))
print("time_2 = ", float(n_traps_2[-1]))
difference = (n_traps_2[-1] - n_traps_1[-1]) * 100 / n_traps_1[-1]
print("difference = ", float(difference), "%")

plt.show()
