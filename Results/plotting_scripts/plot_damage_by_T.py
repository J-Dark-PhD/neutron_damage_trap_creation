import matplotlib.pyplot as plt
from damaged_traps_results import dpa_para_values, inventories_by_T

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure(figsize=[7.5, 4.8])
plt.plot(dpa_para_values, inventories_by_T[2], label="500 K")
plt.plot(dpa_para_values, inventories_by_T[4], label="600 K")
plt.plot(dpa_para_values, inventories_by_T[6], label="700 K")
plt.plot(dpa_para_values, inventories_by_T[8], label="800 K")
plt.plot(dpa_para_values, inventories_by_T[10], label="900 K")
plt.plot(dpa_para_values, inventories_by_T[12], label="1000 K")
plt.ylabel(r"Hydrogen inventory (m$^{-2}$)")
plt.xlabel(r"Damage (dpa/fpy)")
plt.xlim(left=0)
plt.yscale("log")
plt.legend(bbox_to_anchor=(1.05, 0.7))
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()
