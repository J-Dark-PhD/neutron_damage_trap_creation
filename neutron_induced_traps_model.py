import festim as F
import fenics as f
import properties


def trap_conc_steady(A_0, E_A, phi, K, n_max, T):
    """
    Evaluates the trap concentration at steady state
    """
    if phi == 0:
        return 0
    else: 
        A = A_0 * f.exp(-E_A / F.k_B / T)
        return 1 / ((A / (phi * K) + (1 / (n_max))))


def festim_sim(
    dpa=1, T=761, results_folder_name="Results/damaged_traps_testing/{:.0}_dpa/", transient_run=False
):

    my_model = F.Simulation(log_level=20)

    # define mesh
    my_model.mesh = F.MeshFromRefinements(500, size=2e-03)

    V = f.FunctionSpace(my_model.mesh.mesh, "DG", 1)

    # define materials
    tungsten = F.Material(D_0=properties.D_0_W, E_D=properties.E_D_W, id=1)
    my_model.materials = F.Materials([tungsten])

    # define traps
    fpy = 3600 * 24 * 365.25

    trap_W_1 = F.Trap(
        k_0=properties.D_0_W / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=0.87,
        density=1.3e-3 * properties.atom_density_W,
        materials=tungsten,
    )
    trap_W_2 = F.Trap(
        k_0=properties.D_0_W / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.00,
        density=4e-4 * properties.atom_density_W,
        materials=tungsten,
    )
    trap_W_damage_1 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.15,
        density=trap_conc_steady(
            A_0=6.1838e-03, E_A=0.2792, phi=dpa / fpy, K=1.5e28, n_max=5.2e25, T=T
        ),
        materials=tungsten,
    )
    trap_W_damage_2 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.35,
        density=trap_conc_steady(
            A_0=6.1838e-03, E_A=0.2792, phi=dpa / fpy, K=4.0e27, n_max=4.5e25, T=T
        ),
        materials=tungsten,
    )
    trap_W_damage_3 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.65,
        density=trap_conc_steady(
            A_0=6.1838e-03,
            E_A=0.2792,
            phi=dpa / fpy,
            K=3.0e27,
            n_max=4.0e25,
            T=T,
        ),
        materials=tungsten,
    )
    trap_W_damage_4 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.85,
        density=trap_conc_steady(
            A_0=6.1838e-03,
            E_A=0.2792,
            phi=dpa / fpy,
            K=9.0e27,
            n_max=4.2e25,
            T=T,
        ),
        materials=tungsten,
    )

    my_model.traps = F.Traps(
        [
            trap_W_1,
            trap_W_2,
            trap_W_damage_1,
            trap_W_damage_2,
            trap_W_damage_3,
            trap_W_damage_4,
        ]
    )

    # define temperature
    my_model.T = F.Temperature(value=T)

    # define boundary conditions
    my_model.boundary_conditions = [
        F.ImplantationDirichlet(
            surfaces=1,
            phi=1e20,
            R_p=3e-09,
            D_0=properties.D_0_W,
            E_D=properties.E_D_W,
        )
    ]

    # define exports
    results_folder = results_folder_name
    my_derived_quantities = F.DerivedQuantities(
        filename=results_folder + "derived_quantities.csv"
    )
    my_derived_quantities.derived_quantities = [
        F.TotalVolume("solute", volume=1),
        F.TotalVolume("retention", volume=1),
        F.TotalVolume("1", volume=1),
        F.TotalVolume("2", volume=1),
        F.TotalVolume("3", volume=1),
        F.TotalVolume("4", volume=1),
        F.TotalVolume("5", volume=1),
        F.TotalVolume("6", volume=1),
    ]

    my_exports = F.Exports(
        [
            F.XDMFExport(
                "solute",
                label="solute",
                folder=results_folder,
                checkpoint=False,
                mode=1,
            ),
            F.XDMFExport(
                "retention",
                label="retention",
                folder=results_folder,
                checkpoint=False,
                mode=1,
            ),
            F.XDMFExport(
                "1", label="trap_W_1", folder=results_folder, checkpoint=False, mode=1
            ),
            F.XDMFExport(
                "2", label="trap_W_2", folder=results_folder, checkpoint=False, mode=1
            ),
            F.XDMFExport(
                "3",
                label="trap_damaged_1",
                folder=results_folder,
                checkpoint=False,
                mode=1,
            ),
            F.XDMFExport(
                "4",
                label="trap_damaged_2",
                folder=results_folder,
                checkpoint=False,
                mode=1,
            ),
            F.XDMFExport(
                "5",
                label="trap_damaged_3",
                folder=results_folder,
                checkpoint=False,
                mode=1,
            ),
            F.XDMFExport(
                "6",
                label="trap_damaged_4",
                folder=results_folder,
                checkpoint=False,
                mode=1,
            ),
            F.TrapDensityXDMF(
                trap=trap_W_damage_1,
                label="density_1",
                folder=results_folder,
                checkpoint=False,
            ),
            F.TrapDensityXDMF(
                trap=trap_W_damage_2,
                label="density_2",
                folder=results_folder,
                checkpoint=False,
            ),
            F.TrapDensityXDMF(
                trap=trap_W_damage_3,
                label="density_3",
                folder=results_folder,
                checkpoint=False,
            ),
            F.TrapDensityXDMF(
                trap=trap_W_damage_4,
                label="density_4",
                folder=results_folder,
                checkpoint=False,
            ),
            my_derived_quantities,
        ]
    )
    my_model.exports = my_exports

    # define settings
    if transient_run:
        my_model.dt = F.Stepsize(initial_value=1, stepsize_change_ratio=1.08, dt_min=1e-8)
        my_model.settings = F.Settings(
            transient=True,
            final_time=86400 * 12,
            absolute_tolerance=1e12,
            relative_tolerance=1e-08,
            maximum_iterations=50,
        )
    else:
        my_model.settings = F.Settings(
        transient=False,
        final_time=86400 * 12,
        absolute_tolerance=1e12,
        relative_tolerance=1e-08,
        maximum_iterations=50,
    )

    # run simulation
    my_model.initialise()
    my_model.run()


if __name__ == "__main__":

    festim_sim(
        dpa=9, T=761, results_folder_name="Results/damaged_traps_testing/test/", transient_run=False
    )
