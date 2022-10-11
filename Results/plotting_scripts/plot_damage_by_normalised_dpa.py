import matplotlib.pyplot as plt
import numpy as np
from damaged_traps_results import (
    temperature_values,
    inventories_by_dpa_normalised,
    inventories_by_T,
)

diffs = []
for case in inventories_by_T:
    diff = ((case[-1] - case[0]) / case[0]) * 100
    diffs.append(diff)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
plot_1 = plt.plot(
    temperature_values, inventories_by_dpa_normalised[0], label="0 dpa/fpy"
)
plot_2 = plt.plot(
    temperature_values, inventories_by_dpa_normalised[2], label="1 dpa/fpy"
)
plot_3 = plt.plot(
    temperature_values, inventories_by_dpa_normalised[10], label="5 dpa/fpy"
)
plot_4 = plt.plot(
    temperature_values, inventories_by_dpa_normalised[20], label="10 dpa/fpy"
)
plot_5 = plt.plot(
    temperature_values, inventories_by_dpa_normalised[-1], label="20 dpa/fpy"
)
plot_6 = plt.plot(
    temperature_values, inventories_by_dpa_normalised[18], label="9 dpa/fpy"
)
# plt.vlines(761, 1, 3, color="grey", linestyles="dashed")
# plt.annotate("761K", (675, 2), color="grey")

h, l = plt.gca().get_legend_handles_labels()
plt.legend(
    [h[4], h[3], h[5], h[2], h[1], h[0]],
    [l[4], l[3], l[5], l[2], l[1], l[0]],
    loc="upper right",
)
# plt.legend()
plt.ylabel(r"Normalised hydrogen inventory")
plt.xlabel(r"Temperature (K)")
plt.xlim(400, 1300)
plt.ylim(0.9, 3)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.figure()
plt.bar(temperature_values, np.array(diffs), width=10, linewidth=1)
plt.ylabel(r"Hydrogen inventory difference (\%) 0 vs 20 dpa")
plt.xlabel(r"Temperature (K)")
plt.xlim(400, 1300)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()
