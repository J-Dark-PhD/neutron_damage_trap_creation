import numpy as np
from scipy.integrate import odeint

t_damage = 144 * 3600
t_annealing = 3600
t_total = t_damage + t_annealing

t = np.linspace(0, t_total, t_total)
# t = np.linspace(0, t_annealing, t_annealing)

atom_density_W = 6.3e28
k_B = 8.617333e-05
T_list = np.linspace(1, 1400, 100)
T_list_2 = np.linspace(1, 1400, 20)

# ##### Etienne data ##### #
temperatures = [298, 600, 800, 1000, 1200]
trap_1 = [0.09, 0.08, 0.06, 0.00, 0.00]
trap_2 = [0.28, 0.23, 0.19, 0.15, 0.05]
trap_3 = [0.08, 0.06, 0.05, 0.02, 0.04]

# ##### T selinger data ##### #
dpa_values = [0, 0.001, 0.005, 0.023, 0.1, 0.23, 0.5, 2.5]
dpa_list = np.linspace(0, 3, 50)
trap1 = [0, 3.5e24, 5e24, 1.75e25, 3.7e25, 4.1e25, 4.2e25, 4.8e25]
trap2 = [0, 1e24, 2.4e24, 1e25, 2.5e25, 2.8e25, 2.9e25, 3.3e25]
trap3 = [0, 1e24, 1.5e24, 6.0e24, 1.7e25, 2.1e25, 2.4e25, 2.5e25]
trap4 = [0, 1e24, 2.5e24, 2e25, 4.3e25, 5.0e25, 5.7e25, 6.1e25]


# ##### optimised values ##### #
A_0_optimised = 6.1838e-03
E_A_optimised = 0.2792


def neutron_trap_creation_numerical(
    n, t, phi=9.64e-7, K=3.5e28, n_max=1e40, A_0=6.1838e-03, E_A=0.2792, T=298
):
    """
    Temporal evolution of n with resepct to time, for a given value of n and t

    Args:
        n (float): number of traps (m-3)
        t (float): time of simulation (s)
        phi (float): damage per second (dpa s-1). Defaults to 9.64e-07
        K (float): trap creation factor (traps dpa-1). Defaults to 1e28 traps
            s-1
        n_max (float): maximum traps per unit damage (m-3). Defaults to 1e40
            m-3
        A_0 (float): trap annealing factor (s-1). Defaults to 1e-02 s-1
        E_A (float): Annealing activation energy (eV). Defaults to 0.1034 eV
        T (float): the annealing temperature (K). Defaults to 298 K

    Returns:
        float: dn/dt
    """
    dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n
    return dndt


def neutron_trap_creation_numerical_beta(
    n, t, phi=9.64e-7, K=3.5e28, n_max=1e40, A_0=6.1838e-03, beta=1, E_A=0.2792, T=298
):
    """
    Temporal evolution of n with resepct to time, for a given value of n and t

    Args:
        n (float): number of traps (m-3)
        t (float): time of simulation (s)
        phi (float): damage per second (dpa s-1). Defaults to 9.64e-07
        K (float): trap creation factor (traps dpa-1). Defaults to 1e28 traps
            s-1
        n_max (float): maximum traps per unit damage (m-3). Defaults to 1e40
            m-3
        A_0 (float): trap annealing factor (s-1). Defaults to 1e-02 s-1
        beta (float): Another factor varying temperture. Defaults to 1
        E_A (float): Annealing activation energy (eV). Defaults to 0.1034 eV
        T (float): the annealing temperature (K). Defaults to 298 K

    Returns:
        float: dn/dt
    """
    dndt = (
        phi * K * (1 - (n / n_max)) - (A_0 * T**beta) * np.exp(-E_A / (k_B * T)) * n
    )
    return dndt


def damage_then_annealing(
    n,
    t,
    t_damage=518400,
    phi=9.64e-7,
    K=3.5e28,
    n_max=1e40,
    A_0=6.1838e-03,
    E_A=0.2792,
    T=298,
    T_annealing=298,
):
    """
    Temporal evolution of n with resepct to time, for a given value of n and T.
    As this is representing the work of (S. Markelj et al,. 2014, Phys. Scr.,
    014047), in which samples are damaged then annealed.

    Args:
        n (float): number of traps (m-3)
        t (float): time of simulation (s)
        t_damage (float): time of damage effects (s). Defaults to 518400 s
        T_annealing (float): the annealing temperature (K). Defaults to 298 K
        phi_damage (float): damage per second (dpa s-1). Defaults to 9.64e-07
        K (float): trap creation factor (traps dpa-1). Defaults to 1e28 traps
            s-1
        n_max (float): maximum traps per unit damage (m-3). Defaults to 1e40
            m-3
        A_0 (float): trap annealing factor (s-1). Defaults to 1e-02 s-1
        E_A (float): Annealing activation energy (eV). Defaults to 0.1034 eV

    Returns:
        float: dn/dt
    """
    # t = np.linspace(0, t_total, t_total)
    if t < t_damage:
        phi = phi
        T = T
    else:
        phi = 0
        T = T_annealing
    dndt = phi * K * (1 - (n / n_max)) - A_0 * np.exp(-E_A / (k_B * T)) * n
    return dndt


def neutron_trap_creation_analytical(
    t, K=3.7e26, n_max=5.4e27, phi=9.64e-7, A_0=6.1838e-03, E_A=0.2792, T=298, n_0=0
):
    """
    Analytical solution for eq1: the temporal evolution of n with resepct to
    time, for a given value of n and t. Solution assumes steady state phi and
    T and thus is only valid in that case.

    Args:
        t (float): time of simulation (s)
        phi (float): damage per second (dpa s-1). Defaults to 9.64e-07
        K (float): trap creation factor (traps dpa-1). Defaults to 1e28 traps
            s-1
        n_max (float): maximum traps per unit damage (m-3). Defaults to 1e40
            m-3
        A_0 (float): trap annealing factor (s-1). Defaults to 1e-02 s-1
        E_A (float): Annealing activation energy (eV). Defaults to 0.1034 eV
        T (float): the annealing temperature (K). Defaults to 298 K
        n_0 (float): initial trap density (m-3)

    Returns:
        float: n_t: trap density (m-3)
    """

    F = phi * K
    A = A_0 * np.exp(-E_A / (k_B * T))
    n_t = F * n_max / (F + A * n_max) + (
        F * n_0 - F * n_max + A * n_0 * n_max
    ) * np.exp(t * (-F / n_max - A)) / (F + A * n_max)
    return n_t


def annealing_sim(A_0, E_A):
    """
    Runs a numerical model of annealing effects on traps induced by neutron
    damage

    Args:
        A_0 (float): trap annealing factor (s-1).
        E_A (float): Annealing activation energy (eV).

    Returns:
        (list): A list of trap densities at various annealing tempertures
    """
    annealed_trap_densities = []
    phi = 0
    K = 0
    n_max = 1
    n_0 = 0.28 * atom_density_W
    t = np.linspace(0, t_annealing, t_annealing)

    for T in T_list:
        extra_args = (phi, K, n_max, A_0, E_A, T)
        n_traps_annleaing = odeint(
            neutron_trap_creation_numerical, n_0, t, args=extra_args
        )
        end_value = float(n_traps_annleaing[-1])
        annealed_trap_densities.append(end_value)

    return annealed_trap_densities


def annealing_sim_beta(A_0, beta, E_A):
    """
    Runs a numerical model of annealing effects on traps induced by neutron
    damage

    Args:
        A_0 (float): trap annealing factor (s-1).
        beta (float): another factor
        E_A (float): Annealing activation energy (eV).

    Returns:
        (list): A list of trap densities at various annealing tempertures
    """
    annealed_trap_densities = []
    phi = 0
    K = 0
    n_max = 1
    n_0 = 0.28 * atom_density_W
    t = np.linspace(0, t_annealing, t_annealing)

    for T in T_list_2:
        extra_args = (phi, K, n_max, A_0, beta, E_A, T)
        n_traps_annleaing = odeint(
            neutron_trap_creation_numerical_beta, n_0, t, args=extra_args
        )
        end_value = float(n_traps_annleaing[-1])
        annealed_trap_densities.append(end_value)

    return annealed_trap_densities


def damaging_sim(K, n_max):
    """
    Runs a numerical model of annealing effects on traps induced by neutron
    damage

    Args:
        K (float): trap creation factor (traps dpa-1)
        n_max (float):  maximum traps per unit damage (m-3)

    Returns:
        (list): A list of trap densities at various annealing tempertures
    """
    damaged_trap_densities = []
    t_damage = 3600 * 24
    A_0 = A_0_optimised  # optimised value
    E_A = E_A_optimised  # optimised value
    T = 370
    n_0 = 0
    t = np.linspace(0, t_damage, t_damage)

    for dpa in dpa_list:
        phi = dpa / t_damage
        extra_args = (phi, K, n_max, A_0, E_A, T)
        n_traps_annleaing = odeint(
            neutron_trap_creation_numerical, n_0, t, args=extra_args
        )
        end_value = float(n_traps_annleaing[-1])
        damaged_trap_densities.append(end_value)

    return damaged_trap_densities
