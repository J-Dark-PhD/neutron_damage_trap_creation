import matplotlib.pyplot as plt

# import fenics as f
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve
from scipy.interpolate import interp1d


from neutron_trap_creation_models import (
    neutron_trap_creation_numerical,
    trap1,
    trap2,
    trap3,
    trap4,
    dpa_list,
    dpa_values,
    A_0_optimised,
    E_A_optimised,
)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

green_ryb = (117 / 255, 184 / 255, 42 / 255)
firebrick = (181 / 255, 24 / 255, 32 / 255)
pewter_blue = (113 / 255, 162 / 255, 182 / 255)
blue_jeans = (96 / 255, 178 / 255, 229 / 255)
electric_blue = (83 / 255, 244 / 255, 255 / 255)

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
    label=r"Trap 2 fitting ($K = 8.0 \cdot 10^{21}$ s$^{-1}$, $n_{max, \phi} =  4.5\cdot 10^{25}$ m$^{-3}$)",
)

# trap 2
# plt.errorbar(
#     dpa_values,
#     trap2,
#     yerr=trap2_err,
#     fmt=".",
#     color=electric_blue,
#     capsize=5,
#     label=r"Trap 3 ($E_{t} = 1.30$ eV)",
# )
# plt.plot(
#     dpa_list,
#     damaged_trap2_densities,
#     color=electric_blue,
#     label=r"Trap 3 fitting ($K = 5 \cdot 10^{21}$ s$^{-1}$, $n_{max, \phi} =  3.1\cdot 10^{25}$ m$^{-3}$)",
# )

# trap 3
# plt.errorbar(
#     dpa_values,
#     trap3,
#     yerr=trap3_err,
#     fmt=".",
#     capsize=5,
#     color=pewter_blue,
#     label=r"Trap 4 ($E_{t} = 1.50$ eV)",
# )
# plt.plot(
#     dpa_list,
#     damaged_trap3_densities,
#     color=pewter_blue,
#     label=r"Trap 4 fitting ($K = 3.7\cdot 10^{21}$ s$^{-1}$, $n_{max, \phi} =  2.5\cdot 10^{25}$ m$^{-3}$)",
# )

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
    label=r"Trap 5 fitting ($K = 7\cdot 10^{21}$ s$^{-1}$, $n_{max, \phi} =  6\cdot 10^{25}$ m$^{-3}$) ",
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
plt.show()