import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import LogNorm, ListedColormap, Normalize

dpa_values = np.geomspace(1e-03, 1e03, num=50)
T_values = np.linspace(400, 1300, num=50)

inventories = []

results_folder = "../parametric_studies/case_steady/"

for dpa in dpa_values:
    invs_per_T = []
    for T in T_values:
        data_file = (
            results_folder + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, T)
        )
        data = np.genfromtxt(data_file, delimiter=",", names=True)
        invs_per_T.append(data["Total_retention_volume_1"])
    inventories.append(invs_per_T)

norm = LogNorm(vmin=min(dpa_values), vmax=max(dpa_values))
colorbar = cm.viridis
sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)
colours = [colorbar(norm(dpa)) for dpa in dpa_values]

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
for inv, dpa, colour in zip(inventories, dpa_values, colours):
    plt.plot(T_values, inv, label="{} dpa/fpy".format(dpa), color=colour)
plt.ylabel(r"T inventory (m$^{-3}$)")
plt.xlabel(r"Temperature (K)")
plt.xlim(400, 1300)
plt.ylim(1e16, 1e24)
plt.yscale("log")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.subplots_adjust(wspace=0.112, hspace=0.071)
cb = plt.colorbar(sm, label=r"Damage rate (dpa/fpy)")

plt.show()
