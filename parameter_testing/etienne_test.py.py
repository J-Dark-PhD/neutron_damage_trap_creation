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
# ############# All 3 data sets ############ #
##############################################

t = np.linspace(0, t_annealing, t_annealing)
phi = 0
K = 1
n_max = 1
A_0 = A_0_optimised
E_A = E_A_optimised

A_0 = 1e5
E_A = 1.7


n_0_trap1 = trap_1[0] * atom_density_W * 1e-02
n_0_trap2 = trap_2[0] * atom_density_W * 1e-02
n_0_trap3 = trap_3[0] * atom_density_W * 1e-02

annealed_trap_2_densities = []

test_list = [1e02, 1e03, 1e04, 1e05, 1e06]

plt.figure()

for A_0 in test_list:
    annealed_trap_2_densities = []
    for T in T_list:
        extra_args = (phi, K, n_max, A_0, E_A, T)
        n_traps_annleaing_trap_2 = odeint(
            neutron_trap_creation_numerical, n_0_trap2, t, args=extra_args
        )
        end_value_trap_2 = float(n_traps_annleaing_trap_2[-1])
        annealed_trap_2_densities.append(end_value_trap_2)

    trap_2_err = np.array(trap_2) * 0.1
    annealed_trap_2_densities = (np.array(annealed_trap_2_densities) / 6.3e28) * 100
    plt.plot(
        T_list,
        annealed_trap_2_densities,
        color="black",
        label="{:.1e}".format(A_0),
    )
err_bar_2 = plt.errorbar(
    temperatures,
    trap_2,
    yerr=trap_2_err,
    fmt=".",
    capsize=5,
    color=firebrick,
)
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Annealing temperature (K)")
plt.ylim(bottom=0)
plt.xlim(0, 1400)
labelLines(plt.gca().get_lines())
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

plt.show()
