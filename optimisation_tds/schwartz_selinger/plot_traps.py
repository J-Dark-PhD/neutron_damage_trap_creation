import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

atom_density_W = 6.3222e28

trap1 = [0, 3.5e24, 5e24, 1.75e25, 3.7e25, 4.1e25, 4.2e25, 4.8e25]
trap2 = [0, 1e24, 2.4e24, 1e25, 2.5e25, 2.8e25, 2.9e25, 3.3e25]
trap3 = [0, 1e24, 1.5e24, 6.0e24, 1.7e25, 2.1e25, 2.4e25, 2.5e25]
trap4 = [0, 1e24, 2.5e24, 2e25, 4.3e25, 5.0e25, 5.7e25, 6.1e25]

dpa_values = [0, 0.001, 0.005, 0.023, 0.1, 0.23, 0.5, 2.5]

trap1 = (np.array(trap1) / atom_density_W) * 100
trap2 = (np.array(trap2) / atom_density_W) * 100
trap3 = (np.array(trap3) / atom_density_W) * 100
trap4 = (np.array(trap4) / atom_density_W) * 100

plt.figure()
plt.scatter(dpa_values, trap1)
plt.plot(dpa_values, trap1, label=r"Trap 2 ($E_{t} = 1.15 eV$)")

plt.scatter(dpa_values, trap2)
plt.plot(dpa_values, trap2, label=r"Trap 3 ($E_{t} = 1.30 eV$)")

plt.scatter(dpa_values, trap3)
plt.plot(dpa_values, trap3, label=r"Trap 4 ($E_{t} = 1.50 eV$)")

plt.scatter(dpa_values, trap4)
plt.plot(dpa_values, trap4, label=r"Trap 5 ($E_{t} = 1.85 eV$)")


plt.ylabel(r"Trap density, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"Damage (DPA)")
plt.legend()
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.show()
