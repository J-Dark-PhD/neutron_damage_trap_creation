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
    E_p = 1.0

    plt.figure()
    p_values = []
    a_values = []
    for T in T_values:
        p_value = P(p_0=p_0, E_p=E_p, T=T)
        p_values.append(p_value)
        a_value = A(A_0=A_0, E_A=E_A, T=T)
        a_values.append(a_value)
    plt.plot(T_values, p_values, color="black", label=r"detrapping")
    plt.plot(T_values, a_values, color="red", label=r"annealing")

    plt.ylabel(r"Rate, (s$^{-1}$)")
    plt.xlabel(r"Temperature (K)")
    plt.ylim(1e-12, 1e11)
    plt.yscale("log")
    plt.xlim(0, 2000)
    plt.legend()
    ax = plt.gca()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    plt.show()
