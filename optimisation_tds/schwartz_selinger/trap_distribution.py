import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(0, 15e-06, num=1000)
line = 1e25 / (1 + np.exp((x - 3e-06) / 5e-07))

plt.figure()
plt.vlines(3e-06, 0, 1e26, linestyles="dashed", color="black")
plt.vlines(7e-06, 0, 1e26, color="black")
plt.plot(x, line)
plt.yscale("log")
# plt.ylim(7.5e23, 1.2e25)
# plt.xlim(0, 6e-06)

plt.show()
