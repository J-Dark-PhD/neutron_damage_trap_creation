import numpy as np
import sys

sys.path.append("../../")
from FESTIM import k_B


def automatic_vertices(r_p, size, mat, traps, nb_cells, T, implantation_time, flux):
    """Generates an array of vertices for the TDS simulation

    Args:
        r_p (float): the implantation depth
        size (float): the size of the sample
        mat (FESTIM.Material): the material of the TDS
        traps (list of FESTIM.Traps): the traps
        nb_cells (int): number of cells x > r_p + r_d
        T (float): implantation temperature
        implantation_time (float): implantation time
        flux (float): implantation flux

    Returns:
        numpy.array: the mesh vertices
    """
    D = mat.D_0 * np.exp(-mat.E_D / k_B / T)
    ns = np.array([trap.density[0](r_p) for trap in traps])
    E_ps = np.array([trap.E_p for trap in traps])
    E_ks = np.array([trap.E_k for trap in traps])
    k_0s = np.array([trap.k_0 for trap in traps])
    p_0s = np.array([trap.p_0 for trap in traps])
    ps = p_0s * np.exp(-E_ps / k_B / T)
    ks = k_0s * np.exp(-E_ks / k_B / T)
    cmax = r_p * flux / D
    max_penetration_depth = r_p + r_d(cmax, implantation_time, D, ns, ks, ps)
    dx = 3e-6 / 300
    tolerance = 1.2

    if max_penetration_depth * tolerance > size * 0.9:
        max_penetration_depth = size
        print(
            "The estimated maximum penetration depth is: {:.2e} m".format(
                max_penetration_depth
            )
        )
        number_of_cells_required = int(round((max_penetration_depth - 3 * r_p) / dx))
        number_of_cells_required = int(number_of_cells_required)

        vertices = np.concatenate(
            [
                np.linspace(0, 3 * r_p, 100),  # highly refined around implantation
                # damage_zone_total,  # refined in damaged area
                np.linspace(
                    3 * r_p,
                    max_penetration_depth,
                    number_of_cells_required,
                ),  # refined in affected region
            ]
        )
        vertices = np.sort(np.unique(vertices))

    else:
        print(
            "The estimated maximum penetration depth is: {:.2e} m".format(
                max_penetration_depth
            )
        )

        number_of_cells_required = int(
            round((max_penetration_depth * tolerance - 3 * r_p) / dx)
        )
        number_of_cells_required = int(number_of_cells_required)

        vertices = np.concatenate(
            [
                np.linspace(0, 3 * r_p, 100),  # highly refined around implantation
                # damage_zone_total,
                np.linspace(
                    3 * r_p,
                    max_penetration_depth * tolerance,
                    number_of_cells_required,
                ),  # refined in affected region
                np.linspace(
                    max_penetration_depth * tolerance, size, nb_cells
                ),  # coarser elswhere
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
