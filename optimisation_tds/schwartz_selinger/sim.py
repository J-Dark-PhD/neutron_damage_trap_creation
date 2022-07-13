import sympy as sp
from compute_profile_depth import automatic_vertices
import FESTIM as F

fluence = 1.5e25
implantation_time = 72 * 3600
flux = fluence / implantation_time
resting_time = 0.5 * 24 * 3600
exposure_temp = 370
resting_temp = 295
ramp = 3 / 60
tds_time = (1000 - 300) / ramp
size = 8e-04
atom_density_W = 6.3222e28


def festim_sim(n1, E_p2, n2, E_p1=0.9134, initial_number_cells=500):
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
    r = 0
    center = 0.7e-9
    width = 0.5e-9
    distribution = (
        1 / (width * (2 * 3.14) ** 0.5) * sp.exp(-0.5 * ((F.x - center) / width) ** 2)
    )

    my_model = F.Simulation(log_level=30)

    # define materials
    tungsten = F.Material(
        id=1,
        borders=[0, size],
        D_0=2.4e-07,
        E_D=0.39,
    )
    my_model.materials = F.Materials([tungsten])

    # define traps
    my_model.traps = F.Traps(
        [
            F.Trap(
                k_0=2.4e-7 / (1.1e-10**2 * 6 * atom_density_W),
                E_k=0.39,
                p_0=1e13,
                E_p=E_p1,
                density=n1,
                materials=tungsten,
            ),
            F.Trap(
                k_0=4.1e-7 / (1.1e-10**2 * 6 * atom_density_W),
                E_k=0.39,
                p_0=1e13,
                E_p=E_p2,
                density=n2,
                materials=tungsten,
            ),
        ]
    )

    # define mesh
    vertices = automatic_vertices(
        r_p=center,
        size=size,
        mat=tungsten,
        traps=my_model.traps.traps,
        nb_cells=initial_number_cells,
        T=exposure_temp,
        implantation_time=implantation_time,
        flux=flux,
    )
    my_model.mesh = F.MeshFromVertices(vertices)

    # define temperature
    my_model.T = F.Temperature(
        value=exposure_temp * (F.t < implantation_time)
        + resting_temp
        * (F.t >= implantation_time)
        * (F.t < implantation_time + resting_time)
        + (
            (300 + ramp * (F.t - (implantation_time + resting_time)))
            * (F.t >= implantation_time + resting_time)
        )
    )

    # define boundary conditions
    my_model.boundary_conditions = [F.DirichletBC(surfaces=[1, 2], value=0)]

    # define sources
    my_model.sources = [
        F.Source(
            volume=1, field=0, value=flux * distribution * (F.t < implantation_time)
        )
    ]

    # define exports
    folder_results = "Results/"
    my_derived_quantities = F.DerivedQuantities(
        filename=folder_results + "last.csv",
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
        trap_2,
    ]

    my_exports = F.Exports(
        [
            F.XDMFExport(
                "solute",
                folder=folder_results,
                checkpoint=False,
                mode=1,
            ),
            F.XDMFExport(
                "retention",
                folder=folder_results,
                checkpoint=False,
                mode=1,
            ),
            my_derived_quantities,
        ]
    )
    my_model.exports = my_exports

    # define settings
    my_model.dt = F.Stepsize(
        1,
        stepsize_change_ratio=1.08,
        t_stop=implantation_time + resting_time * 0.6,
        dt_min=1e-4,
        stepsize_stop_max=50,
    )

    my_model.settings = F.Settings(
        absolute_tolerance=1e11,
        relative_tolerance=1e-8,
        final_time=implantation_time + resting_time + tds_time,
        transient=True,
    )

    my_model.initialise()
    my_model.run()
    return my_derived_quantities.data


if __name__ == "__main__":
    # 0 dpa values
    # E_p1=0.9134, n1=3.9927e22
    #
    # 0.001 dpa values
    festim_sim(E_p1=0.9134, n1=3.9927e22)
