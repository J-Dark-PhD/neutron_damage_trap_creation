from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

data_dist = np.genfromtxt("damage_profile.csv", delimiter=",", names=True)
x_data = np.array(data_dist["x"])
dpa_data = np.array(data_dist["dpa"])
x_range = np.linspace(0, 2.5e-06, 50)

plt.figure()
plt.scatter(x_data, dpa_data, marker="x", color="black")
interp_model = interp1d(x_data, dpa_data, fill_value="extrapolate")
print(interp_model(2.3e-6))
interp_values = interp_model(x_range)
plt.plot(x_range, interp_values)

plt.ylim(0, 0.6)
plt.xlim(0, 2.5e-06)
plt.ylabel(r"Damage (dpa)")
plt.xlabel(r"x (m)")
plt.legend()
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

plt.show()
