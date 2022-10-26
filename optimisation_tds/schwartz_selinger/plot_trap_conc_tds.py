import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

atom_density_W = 6.3222e28

data = np.genfromtxt(
    "Results/dpa_2.5/retention_before_tds.csv", delimiter=",", names=True
)

x = data["arc_length"]
retention = data["retention"]

retention = (np.array(retention) / atom_density_W) * 100

plt.figure()
plt.plot(x, retention)
plt.ylabel(r"T concentration, n$_{\mathrm{t}}$ (at. \%)")
plt.xlabel(r"x (m)")
plt.yscale("log")
plt.ylim(1e-3, 1e1)
plt.xlim(left=0)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.show()
