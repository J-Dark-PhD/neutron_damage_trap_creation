import numpy as np
from scipy.integrate import odeint
import properties

k_B = 8.6173303e-5


def penetration_depth_at_1e05(dpa, T, implantation_time=1e05):
    """Generates an array of vertices for the TDS simulation

    Args:
        dpa (float): the damage (dpa/fpy)
        T (float): the temperature (K)
        implantation_time (float): implantation time
        traps (list of FESTIM.Traps): the traps

    Returns:
        numpy.array: the mesh vertices
    """
    r_p = 3e-09
    A_0_W = 6.1838e-03
    E_A_W = 0.2792
    fpy = 3600 * 24 * 365.25
    phi = dpa / fpy
    flux = 1e20
    n_0 = 0
    t = np.linspace(0, int(implantation_time), int(1000))

    def numerical_trap_creation_model_trap_1(n, t, phi=phi, A_0=A_0_W, E_A=E_A_W, T=T):
        K = 1.5e28
        n_max = 5.2e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    def numerical_trap_creation_model_trap_2(n, t, phi=phi, A_0=A_0_W, E_A=E_A_W, T=T):
        K = 4.0e27
        n_max = 4.5e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    def numerical_trap_creation_model_trap_3(n, t, phi=phi, A_0=A_0_W, E_A=E_A_W, T=T):
        K = 3.0e27
        n_max = 4.0e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    def numerical_trap_creation_model_trap_4(n, t, phi=phi, A_0=A_0_W, E_A=E_A_W, T=T):
        K = 9.0e27
        n_max = 4.2e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    ns1 = 1.3e-3 * properties.atom_density_W
    ns2 = 4e-4 * properties.atom_density_W
    nsd1 = odeint(
        numerical_trap_creation_model_trap_1,
        n_0,
        t,
    )
    nsd2 = odeint(
        numerical_trap_creation_model_trap_2,
        n_0,
        t,
    )
    nsd3 = odeint(
        numerical_trap_creation_model_trap_3,
        n_0,
        t,
    )
    nsd4 = odeint(
        numerical_trap_creation_model_trap_4,
        n_0,
        t,
    )

    D = properties.D_0_W * np.exp(-properties.E_D_W / k_B / T)

    ns = np.array(
        [np.array([ns1]), np.array([ns2]), nsd1[-1], nsd2[-1], nsd3[-1], nsd4[-1]]
    )
    E_ps = np.array([0.87, 1.00, 1.15, 1.35, 1.65, 1.85])
    E_ks = np.array(
        [
            properties.E_D_W,
            properties.E_D_W,
            properties.E_D_W,
            properties.E_D_W,
            properties.E_D_W,
            properties.E_D_W,
        ]
    )
    k_0s = np.array(
        [
            4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        ]
    )
    p_0s = np.array(
        [
            1e13,
            1e13,
            1e13,
            1e13,
            1e13,
            1e13,
        ]
    )
    ps = p_0s * np.exp(-E_ps / k_B / T)
    ks = k_0s * np.exp(-E_ks / k_B / T)
    cmax = r_p * flux / D
    max_penetration_depth = r_p + r_d(cmax, implantation_time, D, ns, ks, ps)

    a = 0.05 * dpa ** (-0.35)
    b = -0.2 * np.log(dpa) + 3.7
    tolerance = a * (T - 400) + b

    modified_penetration_depth = max_penetration_depth * tolerance

    return modified_penetration_depth


def automatic_vertices(dpa, T, implantation_time, traps):
    """Generates an array of vertices for the TDS simulation

    Args:
        dpa (float): the damage (dpa/fpy)
        T (float): the temperature (K)
        implantation_time (float): implantation time
        traps (list of FESTIM.Traps): the traps

    Returns:
        numpy.array: the mesh vertices
    """
    r_p = 3e-09
    size = 2e-03
    A_0_W = 6.1838e-03
    E_A_W = 0.2792
    fpy = 3600 * 24 * 365.25
    phi = dpa / fpy
    flux = 1e20
    n_0 = 0
    t = np.linspace(0, int(implantation_time), int(1000))

    def numerical_trap_creation_model_trap_1(n, t, phi=phi, A_0=A_0_W, E_A=E_A_W, T=T):
        K = 1.5e28
        n_max = 5.2e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    def numerical_trap_creation_model_trap_2(n, t, phi=phi, A_0=A_0_W, E_A=E_A_W, T=T):
        K = 4.0e27
        n_max = 4.5e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    def numerical_trap_creation_model_trap_3(n, t, phi=phi, A_0=A_0_W, E_A=E_A_W, T=T):
        K = 3.0e27
        n_max = 4.0e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    def numerical_trap_creation_model_trap_4(n, t, phi=phi, A_0=A_0_W, E_A=E_A_W, T=T):
        K = 9.0e27
        n_max = 4.2e25

        dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n

        return dndt

    ns1 = 1.3e-3 * properties.atom_density_W
    ns2 = 4e-4 * properties.atom_density_W
    nsd1 = odeint(
        numerical_trap_creation_model_trap_1,
        n_0,
        t,
    )
    nsd2 = odeint(
        numerical_trap_creation_model_trap_2,
        n_0,
        t,
    )
    nsd3 = odeint(
        numerical_trap_creation_model_trap_3,
        n_0,
        t,
    )
    nsd4 = odeint(
        numerical_trap_creation_model_trap_4,
        n_0,
        t,
    )

    D = properties.D_0_W * np.exp(-properties.E_D_W / k_B / T)

    ns = np.array(
        [np.array([ns1]), np.array([ns2]), nsd1[-1], nsd2[-1], nsd3[-1], nsd4[-1]]
    )
    E_ps = np.array([trap.E_p for trap in traps])
    E_ks = np.array([trap.E_k for trap in traps])
    k_0s = np.array([trap.k_0 for trap in traps])
    p_0s = np.array([trap.p_0 for trap in traps])
    ps = p_0s * np.exp(-E_ps / k_B / T)
    ks = k_0s * np.exp(-E_ks / k_B / T)
    cmax = r_p * flux / D
    max_penetration_depth = r_p + r_d(cmax, implantation_time, D, ns, ks, ps)

    dx = 2e-3 / 100

    # a = 0.05 * dpa ** (-0.35)
    # a = 0.02 * dpa ** (-0.375)
    a = 0.09 * dpa ** (-0.25)
    if a > 0.8:
        a = 0.8
    # b = -0.2 * np.log(dpa) + 3.8
    b = -0.2 * np.log(dpa) + 3.7
    if b < 2.74:
        b = 2.74
    tolerance = a * (T - 400) + b
    # tolerance = a * (T - 400) + 6

    print(
        "The estimated maximum penetration depth is: {:.2e} m".format(
            max_penetration_depth
        )
    )

    print("Tolerance = {:.1f}".format(tolerance))

    print("With correction: {:.2e} m".format(max_penetration_depth * tolerance))

    if max_penetration_depth * tolerance > size:
        vertices = np.concatenate(
            [
                np.linspace(0, size, 500),
            ]
        )
    else:
        number_of_cells_required = int(
            round((size - (max_penetration_depth * tolerance)) / dx)
        )
        vertices = np.concatenate(
            [
                np.linspace(
                    0,
                    max_penetration_depth * tolerance,
                    500,
                ),
                np.linspace(
                    max_penetration_depth * tolerance, size, number_of_cells_required
                ),
            ]
        )

    vertices = np.sort(np.unique(vertices))

    print("The mesh size is: {}".format(len(vertices)))

    return vertices


def r_trap(c, k, p):
    """Computes the filling rate of a trap for a given mobile concentration

    Args:
        c (float): the concentration in H/m3/s
        k (float): the trapping rate in m3/s
        p (float): the detrapping rate(s) in s-1

    Returns:
        float: the filling rate
    """
    val = 1 + p / (k * c)
    val = 1 / val
    return val


def r_d(c_max, t, D, n, k, p):
    """Computes the maximum R_d based on trap parameters and time.
    See Equation 3.31 of Etienne Hodille's phd thesis

    Args:
        c_max (float): the maximum concentration in H/m3/s
        t (float): the time in s
        D (float): the diffusion coefficient in m2/s
        n (array_like): the trap(s) density(ies) in trap/m3
        k (array_like): the trapping rate(s) in m3/s
        p (array_like): the detrapping rate(s) in s-1

    Returns:
        float: the penetration depth in m
    """
    R_d = 2 * D * c_max * t
    R_d /= (r_trap(c_max, k, p) * n).sum()
    R_d = R_d**0.5

    return R_d
