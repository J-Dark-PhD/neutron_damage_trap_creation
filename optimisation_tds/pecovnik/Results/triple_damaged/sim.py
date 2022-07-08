import FESTIM as F
import sympy as sp

from compute_profile_depth import automatic_vertices

flux = 5.6e19
implantation_time = 1.5e25/flux
resting_time = 1*24*3600
exposure_temp = 370
resting_temp = 295
ramp = 3/60
tds_time = (1000 - 300)/ramp
size = 8e-04
atom_density_W = 6.3222e28

r = 0
center = 0.7e-9
width = 0.5e-9
distribution = 1/(width*(2*3.14)**0.5) * sp.exp(-0.5*((F.x-center)/width)**2)


def festim_sim(n1, n2, initial_number_cells=100):
    """Runs a FESTIM simulation

    Args:
        k_01 (_type_): _description_
        E_p1 (_type_): _description_
        n1 (_type_): _description_
        k_02 (_type_): _description_
        E_p2 (_type_): _description_
        n2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    my_model = F.Simulation(log_level=30)

    # define materials
    tungsten = F.Material(
                id=1,
                borders=[0, size],
                # Frauenfelder with a factor 1/sqrt(3)
                D_0=2.4e-07,
                E_D=0.39
            )
    my_model.materials = F.Materials(
        [tungsten]
    )

    # define traps
    my_model.traps = F.Traps([
            F.Trap(
                k_0=5.47e-17,
                E_k=0.39,
                p_0=2e13,  # modifying p_0 helps
                E_p=1.23,
                materials=1,
                density=n1
            ),
            F.Trap(
                k_0=8.96e-17,
                E_k=0.39,
                p_0=4e13,  # modifying p_0 helps
                E_p=1.61,
                materials=1,
                density=n2
            )
            ])

    # define mesh
    vertices = automatic_vertices(
        r_p=center,
        size=size,
        mat=tungsten,
        traps=my_model.traps.traps,
        nb_cells=initial_number_cells,
        T=exposure_temp,
        implantation_time=implantation_time,
        flux=flux
    )
    my_model.mesh = F.MeshFromVertices(vertices)

    # define temperature
    my_model.T = F.Temperature(
        value=exposure_temp*(F.t < implantation_time) +
        resting_temp*(F.t >= implantation_time)*(F.t < implantation_time + resting_time) +
        ((300 + ramp*(F.t - (implantation_time + resting_time))) *
         (F.t >= implantation_time + resting_time))
        )

    # define boundary conditions
    my_model.boundary_conditions = [
        F.DirichletBC(
            surfaces=[1, 2],
            value=0
            )
    ]

    # define sources
    my_model.sources = [
        F.Source(
            volume=1,
            field=0,
            value=flux*distribution*(F.t < implantation_time)
        )
    ]

    # define exports
    my_derived_quantities = F.DerivedQuantities(
        file="last.csv",
        folder="Results/derived_quantities",
        # nb_iterations_between_exports=1,
        )

    average_T = F.AverageVolume("T", volume=1)
    H_flux_left = F.HydrogenFlux(surface=1)
    H_flux_right = F.HydrogenFlux(surface=2)
    solute = F.TotalVolume("solute", volume=1)
    retention = F.TotalVolume("retention", volume=1)
    trap_1 = F.TotalVolume("1", volume=1)
    trap_2 = F.TotalVolume("2", volume=1)
    my_derived_quantities.derived_quantities = [
        average_T,
        H_flux_left,
        H_flux_right,
        solute,
        retention,
        trap_1,
        trap_2
        ]

    my_exports = F.Exports([
        F.XDMFExport("solute", label="solute", folder="Results",
                     checkpoint=False, nb_iterations_between_exports=1),
        F.XDMFExport("retention", label="retention", folder="Results",
                     checkpoint=False, nb_iterations_between_exports=1),
        my_derived_quantities
    ])
    my_model.exports = my_exports

    # define settings
    my_model.dt = F.Stepsize(
        1,
        stepsize_change_ratio=1.1,
        t_stop=implantation_time + resting_time*0.8,
        dt_min=1e-5,
        stepsize_stop_max=50
        )

    my_model.settings = F.Settings(
        absolute_tolerance=1e11,
        relative_tolerance=1e-8,
        final_time=implantation_time + resting_time + tds_time,
        transient=True
    )

    my_model.initialise()
    output = my_model.run()
    return output["derived_quantities"]


if __name__ == "__main__":

    festim_sim(
        # single-damaged values
        # k_01=5.47e-17,
        # E_p1=1.23,
        n1=6.31e+26,
        # k_02=8.96e-17,
        # E_p2=1.617,
        n2=2.10e+26
        )
