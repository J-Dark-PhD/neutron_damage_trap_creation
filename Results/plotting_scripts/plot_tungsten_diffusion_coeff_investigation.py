import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


def effect_on_inventories():
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


def effect_on_filling_ratios():
    k_B = 8.6173303e-05
    atom_density_W = 6.3222e28
    T = 761

    D_0_W_fraunfelder = 4.10e-07
    E_D_W_frauenfelder = 0.39

    D_0_W_holzner = (2.06e-07) / (3**0.5)
    E_D_W_holzner = 0.28

    D_0_W_dft = (1.96e-07) / (3**0.5)
    E_D_W_dft = 0.20

    def k(k_0, E_k):
        return k_0 * np.exp(-E_k / k_B / T)

    def p(p_0, E_p):
        return p_0 * np.exp(-E_p / k_B / T)

    k_frauenfelder = k(
        k_0=D_0_W_fraunfelder / (1.1e-10**2 * 6 * atom_density_W),
        E_k=E_D_W_frauenfelder,
    )
    k_holzner = k(
        k_0=D_0_W_holzner / (1.1e-10**2 * 6 * atom_density_W), E_k=E_D_W_holzner
    )
    k_dft = k(k_0=D_0_W_dft / (1.1e-10**2 * 6 * atom_density_W), E_k=E_D_W_dft)

    p_1 = p(p_0=1e13, E_p=0.97)
    p_2 = p(p_0=1e13, E_p=1)

    p_damaged_1 = p(p_0=1e13, E_p=1.15)
    p_damaged_2 = p(p_0=1e13, E_p=1.30)
    p_damaged_3 = p(p_0=1e13, E_p=1.50)
    p_damaged_4 = p(p_0=1e13, E_p=1.85)

    cm_frauenfelder = 2.8e20
    cm_holzner = 1.8e20
    cm_dft = 6e19

    frauenfelder_trap_1 = 1 / (1 + (p_1 / (k_frauenfelder * cm_frauenfelder)))
    frauenfelder_trap_2 = 1 / (1 + (p_2 / (k_frauenfelder * cm_frauenfelder)))
    frauenfelder_damaged_trap_1 = 1 / (
        1 + (p_damaged_1 / (k_frauenfelder * cm_frauenfelder))
    )
    frauenfelder_damaged_trap_2 = 1 / (
        1 + (p_damaged_2 / (k_frauenfelder * cm_frauenfelder))
    )
    frauenfelder_damaged_trap_3 = 1 / (
        1 + (p_damaged_3 / (k_frauenfelder * cm_frauenfelder))
    )
    frauenfelder_damaged_trap_4 = 1 / (
        1 + (p_damaged_4 / (k_frauenfelder * cm_frauenfelder))
    )

    holzner_trap_1 = 1 / (1 + (p_1 / (k_holzner * cm_holzner)))
    holzner_trap_2 = 1 / (1 + (p_2 / (k_holzner * cm_holzner)))

    dft_trap_1 = 1 / (1 + (p_1 / (k_dft * cm_dft)))
    dft_trap_2 = 1 / (1 + (p_2 / (k_dft * cm_dft)))

    # ##### Plotting ##### #

    plt.rc("text", usetex=True)
    plt.rc("font", family="serif", size=12)

    labels = ["Trap 1 (0.87 eV)", "Trap 2 (1.00 eV)"]
    frauenfelder_values = [frauenfelder_trap_1, frauenfelder_trap_2]
    holzner_values = [frauenfelder_trap_1, dft_trap_2]
    dft_values = [dft_trap_1, dft_trap_2]

    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars

    fig, ax = plt.subplots(figsize=(5, 4.8))
    rects1 = ax.bar(x - width, frauenfelder_values, width, label="Frauenfelder")
    rects1 = ax.bar(x, holzner_values, width, label="Holzner")
    rects2 = ax.bar(x + width, dft_values, width, label="dft")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Filling ratio")
    ax.set_xticks(x, labels)
    ax.legend()
    fig.tight_layout()

    # with damage

    labels = [
        r"Trap 1 \\ (0.87 eV)",
        r"Trap 2 \\ (1.00 eV)",
        r"Damaged Trap 1 \\ (1.15 eV)",
        r"Damaged Trap 2 \\ (1.30 eV)",
        r"Damaged Trap 3 \\ (1.50 eV)",
        r"Damaged Trap 4 \\ (1.85 eV)",
    ]
    frauenfelder_values = [
        frauenfelder_trap_1,
        frauenfelder_trap_2,
        frauenfelder_damaged_trap_1,
        frauenfelder_damaged_trap_2,
        frauenfelder_damaged_trap_3,
        frauenfelder_damaged_trap_4,
    ]

    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 4.8))
    rects1 = ax.bar(x, frauenfelder_values, width, label="Frauenfelder")
    plt.yscale("log")
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Filling ratio")
    ax.set_xticks(x, labels)
    ax.legend()

    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    fig.tight_layout()


effect_on_inventories()
effect_on_filling_ratios()

plt.show()
