import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

dpa_para_values = np.linspace(0, 20, 41)
temperature_values = np.linspace(400, 1300, 73)

inventories_by_T = []
inventories_by_T_normalised = []
inventories_by_dpa = []
inventories_by_dpa_normalised = []
inventories_by_dpa_trap_1 = []
inventories_761 = []
inventories_761_trap_1 = []

for T in temperature_values:
    inventories = []
    for dpa in dpa_para_values:
        filename = (
            "../damaged_traps_testing/{:.1f}K/{:.1f}_dpa/derived_quantities.csv".format(
                T, dpa
            )
        )
        data = np.genfromtxt(filename, delimiter=",", names=True)
        inventory = data["Total_retention_volume_1"]
        inventories.append(inventory)
    inventories_by_T.append(inventories)

for case in inventories_by_T:
    norm = np.array(case) / case[0]
    inventories_by_T_normalised.append(norm)

for dpa in dpa_para_values:
    inventories = []
    for T in temperature_values:
        filename = (
            "../damaged_traps_testing/{:.1f}K/{:.1f}_dpa/derived_quantities.csv".format(
                T, dpa
            )
        )
        data = np.genfromtxt(filename, delimiter=",", names=True)
        inventory = data["Total_retention_volume_1"]
        inventories.append(inventory)
    inventories_by_dpa.append(inventories)

for case in inventories_by_dpa:
    norm = np.array(case) / inventories_by_dpa[0]
    inventories_by_dpa_normalised.append(norm)

# for dpa in dpa_para_values:
#     filename = "761K/{:.0f}_dpa/derived_quantities.csv".format(dpa)
#     data = np.genfromtxt(filename, delimiter=",", names=True)
#     t = data["ts"]
#     inventory = data["Total_retention_volume_1"][-1]
#     inventory_transient = data["Total_retention_volume_1"]
#     trap_1_inventory = data["Total_1_volume_1"]
#     inventories_761.append(inventory)
#     inventories_761_transient.append(inventory_transient)
#     inventories_761_t.append(t)
#     inventories_761_trap_1.append(trap_1_inventory)

diffs = []
for case in inventories_by_T:
    diff = ((case[-1] - case[0]) / case[0]) * 100
    diffs.append(diff)

# plt.figure(figsize=[8, 4.8])
# inventories_761_t = np.array(inventories_761_t) / (3600 * 24)
# plt.plot(inventories_761_t[0], inventories_761_transient[0], label="0 dpa/fpy")
# plt.plot(inventories_761_t[5], inventories_761_transient[5], label="5 dpa/fpy")
# plt.plot(inventories_761_t[10], inventories_761_transient[10], label="10 dpa/fpy")
# plt.plot(inventories_761_t[15], inventories_761_transient[15], label="15 dpa/fpy")
# plt.plot(inventories_761_t[-1], inventories_761_transient[-1], label="20 dpa/fpy")
# plt.ylabel(r"Hydrogen inventory (m$^{-2}$)")
# plt.xlabel(r"Time (days)")
# plt.xlim(0, 3)
# plt.ylim(bottom=0)
# plt.legend(bbox_to_anchor=(1.2, 0.7))
# ax = plt.gca()
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
# plt.tight_layout()

# diff_761 = ((inventories_761[-1]-inventories_761[0])/inventories_761[0])*100
# print("Standard T difference = {:.1f}%".format(diff_761))
# plt.figure()
# plt.plot(dpa_para_values, inventories_761, label="761 K")
# plt.ylabel(r"Hydrogen inventory (m$^{-2}$)")
# plt.xlabel(r"Damage (dpa/fpy)")
# plt.xlim(left=0)
# plt.ylim(bottom=0)
# plt.legend()
# ax = plt.gca()
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
# plt.tight_layout()

# plt.figure(figsize=[7.5, 4.8])
# plt.plot(dpa_para_values, inventories_by_T[2], label="500 K")
# plt.plot(dpa_para_values, inventories_by_T[4], label="600 K")
# plt.plot(dpa_para_values, inventories_by_T[6], label="700 K")
# plt.plot(dpa_para_values, inventories_by_T[8], label="800 K")
# plt.plot(dpa_para_values, inventories_by_T[10], label="900 K")
# plt.plot(dpa_para_values, inventories_by_T[12], label="1000 K")
# plt.ylabel(r"Hydrogen inventory (m$^{-2}$)")
# plt.xlabel(r"Damage (dpa/fpy)")
# plt.xlim(left=0)
# plt.yscale("log")
# plt.legend(bbox_to_anchor =(1.05, 0.7))
# ax = plt.gca()
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
# plt.tight_layout()

# plt.figure()
# plt.plot(temperature_values, inventories_by_dpa[0], label="0 dpa/fpy")
# plt.plot(temperature_values, inventories_by_dpa[-1], label="20 dpa/fpy")
# plt.legend()
# plt.ylabel(r"Hydrogen inventory (m$^{-2}$)")
# plt.xlabel(r"Temperature (K)")
# plt.yscale("log")
# plt.xlim(400, 1300)
# ax = plt.gca()
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
# plt.tight_layout()

# plt.figure()
# plt.plot(temperature_values, inventories_by_dpa[0], label="0 dpa/fpy")
# plt.plot(temperature_values, inventories_by_dpa[1], label="1 dpa/fpy")
# plt.plot(temperature_values, inventories_by_dpa[5], label="5 dpa/fpy")
# plt.plot(temperature_values, inventories_by_dpa[10], label="10 dpa/fpy")
# plt.plot(temperature_values, inventories_by_dpa[20], label="20 dpa/fpy")
# plt.legend()
# plt.ylabel(r"Hydrogen inventory (m$^{-2}$)")
# plt.xlabel(r"Temperature (K)")
# plt.xlim(400, 1300)
# plt.yscale("log")
# ax = plt.gca()
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
# plt.tight_layout()

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
plt.vlines(761, 1, 3, color="grey", linestyles="dashed")
plt.annotate("761K", (675, 2), color="grey")

h, l = plt.gca().get_legend_handles_labels()
plt.legend(
    [h[4], h[3], h[2], h[1], h[0]], [l[4], l[3], l[2], l[1], l[0]], loc="upper right"
)
plt.ylabel(r"Normalised hydrogen inventory")
plt.xlabel(r"Temperature (K)")
plt.xlim(400, 1300)
plt.ylim(0.9, 3)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

# plt.figure()
# plt.bar(temperature_values, np.array(diffs), width=10, linewidth=1)
# plt.ylabel(r"Hydrogen inventory difference (\%) 0 vs 20 dpa")
# plt.xlabel(r"Temperature (K)")
# plt.xlim(400, 1300)
# ax = plt.gca()
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
# plt.tight_layout()

plt.show()
