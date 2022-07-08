import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 1)
y = 3.79e-7*np.exp(-6.03*x)/3.79e-7

plt.figure()
plt.plot(x, y)

plt.xlabel("x (m)")
# plt.ylabel(r"$c_t$ (H m$^{-1}$)")

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.tight_layout()

plt.figure()

for i in range(50):
    a = np.random.uniform(0, 1, size=10)
    dist = 3.79e-7*np.exp(-6.03*a)/3.79e-7
    x = np.random.exponential(dist)
    y = np.random.uniform(0, 1, size=10)
    plt.scatter(x, y, color='black', marker='.', s=3)
    plt.ylim(0, 1)
    plt.xlim(0, 1)
    plt.xticks([])
    plt.yticks([])
    plt.draw()
    plt.pause(1e-2)


plt.show()
