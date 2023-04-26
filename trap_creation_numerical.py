import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


# time points
final_time = 86400 * 365 * 7
num = int(1e07)
t = np.linspace(0, final_time, num)

k_B = 8.617333e-05
fpy = 86400 * 365

phi = 9 / fpy
A_0 = 6.1838e-03
E_A = 0.2792
T = 761

# ##### initial condition
n_0 = 0
dpa_values = np.geomspace(1e-03, 1e03, num=7)
T_values = np.linspace(1300, 400, num=50)

traps_concs = []

for dpa in dpa_values:
    phi = dpa / fpy

    def numerical_trap_creation_model_trap_1(n, t, phi=phi, A_0=A_0, E_A=E_A, T=T):
        K = 1.5e28
        n_max = 5.2e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    trap_1 = odeint(
        numerical_trap_creation_model_trap_1,
        n_0,
        t,
    )
    traps_concs.append(trap_1)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
for case, dpa in zip(traps_concs, dpa_values):
    plt.plot(t, case, label="{:.0e} dpa/fpy".format(dpa))
h, l = plt.gca().get_legend_handles_labels()
plt.legend(
    [h[6], h[5], h[4], h[3], h[2], h[1], h[0]],
    [l[6], l[5], l[4], l[3], l[2], l[1], l[0]],
    loc="lower right",
)
plt.yscale("log")
plt.xscale("log")
# plt.legend(loc="lower right")
plt.xlabel("Time (s)")
plt.ylabel("Trap concentration (m$^{-3}$)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)


t_plot = t / (3600)

plt.figure()
for case, dpa in zip(traps_concs, dpa_values):
    plt.plot(t_plot, case, label="{:.0e} dpa/fpy".format(dpa))
h, l = plt.gca().get_legend_handles_labels()
plt.legend(
    [h[6], h[5], h[4], h[3], h[2], h[1], h[0]],
    [l[6], l[5], l[4], l[3], l[2], l[1], l[0]],
    loc="lower right",
)
plt.yscale("log")
plt.xlim(0, 15)
# plt.legend(loc="lower right")
plt.xlabel("Time (s)")
plt.ylabel("Trap concentration (m$^{-3}$)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

plt.show()
