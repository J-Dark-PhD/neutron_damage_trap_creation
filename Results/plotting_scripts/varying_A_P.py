import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

k_B = 8.617333e-05


def A(A_0, E_A, T):
    """formulation for A"""
    A = A_0 * np.exp(-E_A / (k_B * T))
    return A


def P(p_0, E_p, T):
    """forulation for"""
    P = p_0 * np.exp(-E_p / (k_B * T))
    return P


if __name__ == "__main__":
    T_values = np.linspace(100, 2000, num=1000)
    A_0 = 6.1838e-03
    E_A = 0.2792
    p_0 = 1e13
    E_p_1 = 0.87
    E_p_2 = 1.0
    E_p_3 = 1.15
    E_p_4 = 1.3
    E_p_5 = 1.5
    E_p_6 = 1.85

    plt.figure()
    p_1_values = []
    p_2_values = []
    p_3_values = []
    p_4_values = []
    p_5_values = []
    p_6_values = []
    a_values = []
    for T in T_values:
        p_1_value = P(p_0=p_0, E_p=E_p_1, T=T)
        p_1_values.append(p_1_value)
        p_2_value = P(p_0=p_0, E_p=E_p_2, T=T)
        p_2_values.append(p_2_value)
        p_3_value = P(p_0=p_0, E_p=E_p_3, T=T)
        p_3_values.append(p_3_value)
        p_4_value = P(p_0=p_0, E_p=E_p_4, T=T)
        p_4_values.append(p_4_value)
        p_5_value = P(p_0=p_0, E_p=E_p_5, T=T)
        p_5_values.append(p_5_value)
        p_6_value = P(p_0=p_0, E_p=E_p_6, T=T)
        p_6_values.append(p_6_value)
        a_value = A(A_0=A_0, E_A=E_A, T=T)
        a_values.append(a_value)
    plt.plot(T_values, p_1_values, color="black", label=r"detrapping (0.87 eV)")
    plt.plot(T_values, p_2_values, label=r"detrapping (1.00 eV)")
    plt.plot(T_values, p_3_values, label=r"detrapping (1.15 eV)")
    plt.plot(T_values, p_4_values, label=r"detrapping (1.30 eV)")
    plt.plot(T_values, p_5_values, label=r"detrapping (1.50 eV)")
    plt.plot(T_values, p_6_values, label=r"detrapping (1.85 eV)")
    plt.plot(T_values, a_values, color="red", label=r"annealing")

    plt.ylabel(r"Rate, (s$^{-1}$)")
    plt.xlabel(r"Temperature (K)")
    plt.ylim(1e-14, 1e11)
    plt.yscale("log")
    plt.xlim(300, 2000)
    plt.legend()
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    plt.show()
