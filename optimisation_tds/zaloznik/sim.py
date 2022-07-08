import FESTIM as F
import sympy as sp

from compute_profile_depth import automatic_vertices

flux = 2.6e19
implantation_time = 1.3e25/flux
resting_time = 1*24*3600
exposure_temp = 500
resting_temp = 295
ramp = 15/60
tds_time = (1000 - 300)/ramp
size = 1.5e-04
atom_density_W = 6.3222e28

r = 0
# ##### NEED TO FIND THESE ##### #
center = 0.7e-9
width = 0.5e-9
distribution = 1/(width*(2*3.14)**0.5) * sp.exp(-0.5*((F.x-center)/width)**2)
# ##### NEED TO FIND THESE ##### #


def festim_sim(E_p1, n1, initial_number_cells=500):
    """Runs a FESTIM simulation

    Args:
        k_01 (float, list): trapping rate pre-exponential factor (m3/s)
        E_p1 (float, list): trapping rate actiavtion energy (eV)
        n1 (float, list): trap density (m-3)

    Returns:
        .XDMF file: Simulation outputs
    """
    my_model = F.Simulation(log_level=30)

    # define materials
    tungsten = F.Material(
                id=1,
                borders=[0, size],
                D_0=2.4e-07,
                E_D=0.39
            )
    my_model.materials = F.Materials(
        [tungsten]
    )

    # define traps
    my_model.traps = F.Traps([
            # neutron induced trap
            F.Trap(
                k_0=5.22e-17,
                E_k=0.39,
                p_0=1e13,  # modifying p_0 helps
                E_p=E_p1,
                materials=1,
                density=n1*(F.x < 2.4e-06)
            ),
            # standard traps
            F.Trap(
                k_0=5.22e-17,
                E_k=0.39,
                p_0=1e13,
                E_p=0.87,
                materials=1,
                density=8.21886e25
            ),
            F.Trap(
                k_0=8.93e-17,
                E_k=0.39,
                p_0=1e13,
                E_p=1.0,
                materials=1,
                density=2.7817e25
            ),
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
    my_derived_quantities.derived_quantities = [
        F.AverageVolume("T", volume=1),
        F.HydrogenFlux(surface=1),
        F.HydrogenFlux(surface=2),
        F.TotalVolume("solute", volume=1),
        F.TotalVolume("retention", volume=1),
        F.TotalVolume("1", volume=1),
        F.TotalVolume("2", volume=1),
        ]
    my_exports = F.Exports([
        F.XDMFExport("solute", label="solute", folder="Results",
                     checkpoint=False, nb_iterations_between_exports=1),
        F.XDMFExport("retention", label="retention", folder="Results",
                     checkpoint=False, nb_iterations_between_exports=2),
        my_derived_quantities
    ])
    my_model.exports = my_exports

    # define settings
    my_model.dt = F.Stepsize(
        1,
        stepsize_change_ratio=1.1,
        t_stop=implantation_time + resting_time*0.75,
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
        E_p1=1.2,
        n1=1e+26,
        )
