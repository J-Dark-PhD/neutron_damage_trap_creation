import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

optimised_A_0 = 

phi = 1e8
K = 1
n_max = 1e13
A_0 = 0
E_A = 0.1034
k_B = 8.617333e-05
T = 300
n_0 = 0
t_2 = np.linspace(0, 8e5, 30)
y_analytical = analytical_model(t_2)

results = "../derived_quantities.csv"
data = np.genfromtxt(results, delimiter=",", names=True)

t = data["ts"]
trap_data = data["Average_1_volume_1"]

plt.figure()
ax = plt.gca()
plt.plot(t, trap_data, color="black", label="FESTIM")
plt.scatter(t_2, y_analytical, color="red", marker="x", label="Analytical solution")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend()
plt.ylabel(r"No. traps, n$_{\mathrm{t}}$")
plt.xlabel(r"Time")
plt.xticks([])
plt.yticks([])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
plt.show()
