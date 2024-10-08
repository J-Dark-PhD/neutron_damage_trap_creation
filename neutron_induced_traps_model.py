import festim as F
import fenics as f
import properties
from compute_profile_depth import automatic_vertices
import numpy as np


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
    dpa=1,
    T=761,
    results_folder_name="Results/damaged_traps_testing/{:.0}_dpa/",
    transient_run=False,
    total_time=1e05,
):
    my_model = F.Simulation(log_level=40)

    # define materials
    tungsten = F.Material(D_0=properties.D_0_W, E_D=properties.E_D_W, id=1)
    my_model.materials = F.Materials([tungsten])

    # define traps
    fpy = 3600 * 24 * 365.25
    A_0_W = 6.1838e-03
    E_A_W = 0.2792
    defined_absolute_tolerance = 1e07
    defined_relative_tolerance = 1e-01
    defined_maximum_iterations = 10

    trap_W_1 = F.Trap(
        k_0=properties.D_0_W / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.0,
        density=2e22,
        materials=tungsten,
    )
    if transient_run:
        trap_W_damage_1 = F.NeutronInducedTrap(
            k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            E_k=properties.E_D_W,
            p_0=1e13,
            E_p=1.15,
            A_0=A_0_W,
            E_A=E_A_W,
            phi=dpa / fpy,
            K=1.5e28,
            n_max=5.2e25,
            materials=tungsten,
            absolute_tolerance=defined_absolute_tolerance,
            relative_tolerance=defined_relative_tolerance,
            maximum_iterations=defined_maximum_iterations,
        )
        trap_W_damage_2 = F.NeutronInducedTrap(
            k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            E_k=properties.E_D_W,
            p_0=1e13,
            E_p=1.35,
            A_0=A_0_W,
            E_A=E_A_W,
            phi=dpa / fpy,
            K=4.0e27,
            n_max=4.5e25,
            materials=tungsten,
            absolute_tolerance=defined_absolute_tolerance,
            relative_tolerance=defined_relative_tolerance,
            maximum_iterations=defined_maximum_iterations,
        )
        trap_W_damage_3 = F.NeutronInducedTrap(
            k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            E_k=properties.E_D_W,
            p_0=1e13,
            E_p=1.65,
            A_0=A_0_W,
            E_A=E_A_W,
            phi=dpa / fpy,
            K=3.0e27,
            n_max=4.0e25,
            materials=tungsten,
            absolute_tolerance=defined_absolute_tolerance,
            relative_tolerance=defined_relative_tolerance,
            maximum_iterations=defined_maximum_iterations,
        )
        trap_W_damage_4 = F.NeutronInducedTrap(
            k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            E_k=properties.E_D_W,
            p_0=1e13,
            E_p=1.85,
            A_0=A_0_W,
            E_A=E_A_W,
            phi=dpa / fpy,
            K=9.0e27,
            n_max=4.2e25,
            materials=tungsten,
            absolute_tolerance=defined_absolute_tolerance,
            relative_tolerance=defined_relative_tolerance,
            maximum_iterations=defined_maximum_iterations,
        )
    else:
        trap_W_damage_1 = F.Trap(
            k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            E_k=properties.E_D_W,
            p_0=1e13,
            E_p=1.15,
            density=trap_conc_steady(
                A_0=A_0_W, E_A=E_A_W, phi=dpa / fpy, K=1.5e28, n_max=5.2e25, T=T
            ),
            materials=tungsten,
        )
        trap_W_damage_2 = F.Trap(
            k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            E_k=properties.E_D_W,
            p_0=1e13,
            E_p=1.35,
            density=trap_conc_steady(
                A_0=A_0_W, E_A=E_A_W, phi=dpa / fpy, K=4.0e27, n_max=4.5e25, T=T
            ),
            materials=tungsten,
        )
        trap_W_damage_3 = F.Trap(
            k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
            E_k=properties.E_D_W,
            p_0=1e13,
            E_p=1.65,
            density=trap_conc_steady(
                A_0=A_0_W,
                E_A=E_A_W,
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
                A_0=A_0_W,
                E_A=E_A_W,
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
            trap_W_damage_1,
            trap_W_damage_2,
            trap_W_damage_3,
            trap_W_damage_4,
        ]
    )

    implantation_depth = 3e-09
    implantation_flux = 1e20

    simple = True

    if dpa == 0:
        vertices = np.linspace(0, 2e-03, num=500)
    elif simple is True:
        vertices = np.linspace(0, 2e-03, num=500)
    else:
        vertices = automatic_vertices(
            dpa=dpa, T=T, implantation_time=total_time, traps=my_model.traps.traps
        )

    my_model.mesh = F.MeshFromVertices(vertices)

    # define temperature
    my_model.T = F.Temperature(value=T)

    # define boundary conditions
    my_model.boundary_conditions = [
        F.ImplantationDirichlet(
            surfaces=1,
            phi=implantation_flux,
            R_p=implantation_depth,
            D_0=properties.D_0_W,
            E_D=properties.E_D_W,
        ),
        # F.DirichletBC(surfaces=2, value=0, field="solute"),
    ]

    # define exports
    results_folder = results_folder_name
    my_derived_quantities = F.DerivedQuantities(
        filename=results_folder + "derived_quantities.csv"
    )
    my_derived_quantities.derived_quantities = [
        F.TotalVolume("solute", volume=1),
        F.TotalVolume("retention", volume=1),
        # F.TotalVolume("1", volume=1),
        # F.TotalVolume("2", volume=1),
        # F.TotalVolume("3", volume=1),
        # F.TotalVolume("4", volume=1),
        # F.TotalVolume("5", volume=1),
    ]

    my_exports = F.Exports(
        [
            # F.XDMFExport(
            #     "solute",
            #     label="solute",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.XDMFExport(
            #     "retention",
            #     label="retention",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.XDMFExport(
            #     "1", label="trap_W_1", folder=results_folder, checkpoint=False, mode=1
            # ),
            # F.XDMFExport(
            #     "2",
            #     label="trap_damaged_1",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.XDMFExport(
            #     "3",
            #     label="trap_damaged_2",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.XDMFExport(
            #     "4",
            #     label="trap_damaged_3",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.XDMFExport(
            #     "5",
            #     label="trap_damaged_4",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.TrapDensityXDMF(
            #     trap_W_damage_1,
            #     label="trap_damaged_1_density",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.TrapDensityXDMF(
            #     trap_W_damage_2,
            #     label="trap_damaged_2_density",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.TrapDensityXDMF(
            #     trap_W_damage_3,
            #     label="trap_damaged_3_density",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            # F.TrapDensityXDMF(
            #     trap_W_damage_4,
            #     label="trap_damaged_4_density",
            #     folder=results_folder,
            #     checkpoint=False,
            #     mode=1,
            # ),
            my_derived_quantities,
        ]
    )
    my_model.exports = my_exports

    # define settings
    if transient_run:
        my_model.dt = F.Stepsize(
            initial_value=0.1,
            stepsize_change_ratio=1.05,
            dt_min=1e-8,
        )
        my_model.settings = F.Settings(
            transient=True,
            final_time=total_time,
            absolute_tolerance=1e10,
            relative_tolerance=1e-10,
            maximum_iterations=30,
        )
    else:
        my_model.settings = F.Settings(
            transient=False,
            absolute_tolerance=1e10,
            relative_tolerance=1e-10,
            maximum_iterations=30,
        )

    # run simulation
    my_model.initialise()
    my_model.run()


if __name__ == "__main__":
    # temperature_values = np.linspace(400, 1300, num=100)
    # sim_times = [1e02, 1e03, 1e04, 1e05]
    # sim_times = [1e06]
    # for sim_time in sim_times:
    #     for T in temperature_values:
    #         print("running case T={:.0f}".format(T))

    #         festim_sim(
    #             dpa=0,
    #             T=T,
    #             results_folder_name="Results/parametric_studies/case_24h/dpa=0/time={:.1e}/T={:.0f}/".format(
    #                 sim_time, T
    #             ),
    #             transient_run=True,
    #             total_time=sim_time,
    #         )

    festim_sim(
        dpa=0,
        T=700,
        results_folder_name="Results/parametric_studies/case_1fpy/dpa=0/T=700/",
        transient_run=True,
        total_time=3600 * 24 * 365.25,
    )

    # temperature_values = np.linspace(400, 1300, num=10)
    # for T in temperature_values:
    #     print("running case T={:.0f}".format(T))
    #     festim_sim(
    #         dpa=0,
    #         T=T,
    #         results_folder_name="Results/parametric_studies/testing/dpa=0/T={:.0f}/".format(
    #             T
    #         ),
    #         transient_run=True,
    #         total_time=3600 * 24 * 365.25,
    #     )
