import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


invs_first_wall = []
invs_structure = []
folder = "../diffusion_coeff_testing/"

standard_filename = folder + "standard_steady/derived_quantities.csv"
data_standard = np.genfromtxt(standard_filename, delimiter=",", names=True)
invs_first_wall.append(data_standard["Total_retention_volume_1"])


alt_holzner_filename = folder + "alt_holzner_steady/derived_quantities.csv"
data_alt_holzner = np.genfromtxt(alt_holzner_filename, delimiter=",", names=True)
invs_first_wall.append(data_alt_holzner["Total_retention_volume_1"])

alt_filename = folder + "alt_steady/derived_quantities.csv"
data_alt = np.genfromtxt(alt_filename, delimiter=",", names=True)
invs_first_wall.append(data_alt["Total_retention_volume_1"])

k_B = 1.380649e-23
T = 761

D_0_W_fraunfelder = 4.10e-07
E_D_W_frauenfelder = 0.39

D_0_W_holzner = (2.06e-07) / (3**0.5)
E_D_W_holzner = 0.28

D_0_W_dft = (1.96e-07) / (3**0.5)
E_D_W_dft = 0.20


def D_W_frauenfelder(T):
    return D_0_W_holzner * np.exp(-E_D_W_holzner / k_B / T)


def D_W_holzner(T):
    return D_0_W_holzner * np.exp(-E_D_W_holzner / k_B / T)


def D_W_holzner(T):
    return D_0_W_holzner * np.exp(-E_D_W_holzner / k_B / T)


cases = ["standard", "holzner", "DFT"]

# diff_inv_W = ((invs_first_wall[-1] - invs_first_wall[0]) / invs_first_wall[0]) * 100
# print("W Inventory difference = {:.1f}%".format(diff_inv_W))

# diff_inv_structure = (
#     (invs_structure[-1] - invs_structure[0]) / invs_structure[0]
# ) * 100
# print("Structure Inventory difference = {:.1f}%".format(diff_inv_structure))

widths = np.array([0.2, 0.2, 0.2])

plt.figure(figsize=(4, 4.8))
plt.bar(cases, invs_first_wall, width=widths, color="red")
# plt.ylim(0, 6e17)
# plt.xlim(0, 20)
plt.ylabel(r"Inventory (T m$^{-1}$)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()
