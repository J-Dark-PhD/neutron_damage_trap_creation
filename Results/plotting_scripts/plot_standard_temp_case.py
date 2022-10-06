import matplotlib.pyplot as plt
from damaged_traps_results import dpa_para_values, inventories_761

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


diff_761 = ((inventories_761[-1] - inventories_761[0]) / inventories_761[0]) * 100
DEMO_case = ((inventories_761[18] - inventories_761[0]) / inventories_761[0]) * 100
print("Inventory difference = {:.1f}%".format(diff_761))
print("DEMO case = {:.1f}%".format(DEMO_case))
plt.figure()
plt.plot(dpa_para_values, inventories_761, label="761 K")
plt.ylabel(r"Hydrogen inventory (m$^{-2}$)")
plt.xlabel(r"Damage (dpa/fpy)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend()
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()
