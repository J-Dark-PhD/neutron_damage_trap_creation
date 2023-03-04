import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize


k_B = 8.617333e-05
fpy = 86400 * 365
A_0 = 6.1838e-03
E_A = 0.2792
n_0 = 0

dpa_values = np.geomspace(1e-03, 1e04, num=50)
T_values = np.linspace(1300, 400, num=500)
t = np.geomspace(1e01, 1e09, int(1e04))

trap_densities = []

for T in T_values:
    traps_per_T = []
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
        traps_per_T.append(trap_1)
    trap_densities.append(traps_per_T)

normalised_traps = []
for T_case in trap_densities:
    normalised_traps_per_T = []
    for dpa_case in T_case:
        norm_values = dpa_case / dpa_case[-1]
        normalised_traps_per_T.append(norm_values)
    normalised_traps.append(normalised_traps_per_T)

characteristic_times = []
for T_case in normalised_traps:
    char_times_per_T = []
    for dpa_case in T_case:
        char_time = np.where(dpa_case > 0.99)
        first = char_time[0][0]
        char_times_per_T.append(t[first])
    characteristic_times.append(char_times_per_T)


norm = Normalize(vmin=min(T_values), vmax=max(T_values))
colorbar = cm.inferno
sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

colours = [colorbar(norm(T)) for T in T_values]

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure(figsize=[8, 4.8])

day = 3600 * 24
month = day * 31
year = day * 365.25
plt.hlines(day, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")
plt.hlines(month, 1e-03, 5e04, color="black", alpha=0.3, linestyle="dashed")

# dpa_values = dpa_valuses / year
for T, char_times, colour in zip(T_values, characteristic_times, colours):
    plt.plot(dpa_values, char_times, color=colour)

plt.xscale("log")
plt.yscale("log")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.ylabel(r"$\tau_{c}$ (s)")
plt.xlabel(r"Damage rate (dpa/fpy)")
plt.subplots_adjust(wspace=0.112, hspace=0.071)
plt.colorbar(sm, label=r"Temperature (K)")
plt.xlim(1e-03, 1e03)
plt.ylim(1e03, 1e07)

plt.annotate("1 day", [3e02, day * 1.1], color="black", alpha=0.3)
plt.annotate("1 month", [1.5e02, month * 1.1], color="black", alpha=0.3)

plt.show()
