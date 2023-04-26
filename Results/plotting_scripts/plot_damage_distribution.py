import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1e-5, num=1000)

traps = 1 / (1 + np.exp((x - 2.5e-06) / 5e-07))

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
plt.plot(x, traps, color="black")
plt.xlim(0, 1e-05)
plt.ylim(0, 1)
plt.ylabel(r"Trap density ratio")
plt.xlabel(r"x (m)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
plt.tight_layout()

plt.show()
