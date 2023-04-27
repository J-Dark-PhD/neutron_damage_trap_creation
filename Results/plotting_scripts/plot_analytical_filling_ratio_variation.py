import matplotlib.pyplot as plt
import numpy as np
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2dir = os.path.dirname(parentdir)
sys.path.insert(0, parent2dir)

from analytical_model import filling_ratio_evaluation

T_range = np.linspace(400, 1300, num=1000)
(
    trap_1_filling_ratios,
    trap_d1_filling_ratios,
    trap_d2_filling_ratios,
    trap_d3_filling_ratios,
    trap_d4_filling_ratios,
) = filling_ratio_evaluation(T_range)

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
plt.plot(T_range, trap_1_filling_ratios, label="Trap 1 (1.00 eV)")
plt.plot(T_range, trap_d1_filling_ratios, label="Trap D1 (1.15 eV)")
plt.plot(T_range, trap_d2_filling_ratios, label="Trap D2 (1.35 eV)")
plt.plot(T_range, trap_d3_filling_ratios, label="Trap D3 (1.65 eV)")
plt.plot(T_range, trap_d4_filling_ratios, label="Trap D4 (1.85 eV)")
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
