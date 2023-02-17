import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(0, 5e-06, num=1000)
line = 1 / (1 + np.exp((x - 3e-06) / 5e-07))

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
# plt.vlines(3e-06, 0, 1e26, linestyles="dashed", color="black")
# plt.vlines(7e-06, 0, 1e26, color="black")
plt.plot(x, line, color="black")
# plt.yscale("log")
plt.ylabel(r"$\frac{n_{t}(x)}{n_{t}}$", fontsize=18)
plt.xlabel(r"x (m)")
plt.ylim(0, 1)
# plt.yticks([])
plt.xlim(0, 5e-06)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.show()
