import matplotlib.pyplot as plt
from analytical_model_testing import (
    T_range,
    trap_1_filling_ratios,
    trap_2_filling_ratios,
    trap_3_filling_ratios,
    trap_4_filling_ratios,
    trap_5_filling_ratios,
    trap_6_filling_ratios,
)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
plt.plot(T_range, trap_1_filling_ratios, label="Trap 1 (0.87 eV)")
plt.plot(T_range, trap_2_filling_ratios, label="Trap 2 (1.00 eV)")
plt.plot(T_range, trap_3_filling_ratios, label="Trap 3 (1.15 eV)")
plt.plot(T_range, trap_4_filling_ratios, label="Trap 4 (1.35 eV)")
plt.plot(T_range, trap_5_filling_ratios, label="Trap 5 (1.65 eV)")
plt.plot(T_range, trap_6_filling_ratios, label="Trap 6 (1.85 eV)")
plt.ylabel(r"Filling ratio")
plt.xlabel(r"Temperature (K)")
plt.xlim(400, 1300)
plt.ylim(0, 1)
plt.legend()
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()
