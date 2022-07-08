from matplotlib import pyplot as plt

from neutron_trap_creation_models import temperatures, trap_1, trap_2, trap_3

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

plt.figure()
ax = plt.gca()
plt.scatter(temperatures, trap_1, color="blue", marker="x", label=r"trap 1")
plt.scatter(temperatures, trap_2, color="black", marker="x", label=r"trap 2")
plt.scatter(temperatures, trap_3, color="red", marker="x", label=r"trap 3")
plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Annealing Temperature (K)")
plt.ylim(0, 0.3)
plt.xlim(0, 1400)
plt.legend()
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

plt.show()
