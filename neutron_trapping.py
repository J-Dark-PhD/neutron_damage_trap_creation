import FESTIM as F
import fenics as f
import numpy as np
from scipy.interpolate import interp1d


class InterpolatedExpression(f.UserExpression):
    def __init__(self) -> None:
        super().__init__()
        data_dmg = np.genfromtxt(
            "parameter_testing/damage_profile.csv", delimiter=",", names=True
        )
        x_data = np.array(data_dmg["x"])
        dpa_data = np.array(data_dmg["dpa"])
        interp_func = interp1d(x_data, dpa_data, fill_value="extrapolate")
        self.interpolated_values = interp_func

    def eval(self, value, x):
        val = self.interpolated_values(x)[0]
        if np.isnan(val):
            val = 0
        value[0] = val


class OptimisedNeutronInducedTrap(F.NeutronInducedTrap):
    """
    class to have phi as an expression rather than a function
    """

    def __init__(self, k_0, E_k, p_0, E_p, materials, phi, K, n_max, A_0, E_A, id=None):
        super().__init__(
            k_0,
            E_k,
            p_0,
            E_p,
            materials,
            phi=phi,
            K=K,
            n_max=n_max,
            A_0=A_0,
            E_A=E_A,
            id=id,
        )
        self.phi = f.project(self.phi, V)


my_model = F.Simulation(log_level=30)

# define mesh
my_model.mesh = F.MeshFromRefinements(10000, size=5e-06)

V = f.FunctionSpace(my_model.mesh.mesh, "DG", 1)

# define materials
tungsten = F.Material(D_0=2.4e-7, E_D=0.39, id=1)
my_model.materials = F.Materials([tungsten])

# define traps
trap_1 = OptimisedNeutronInducedTrap(
    k_0=5.22e-17,
    E_k=0.39,
    p_0=1e13 * 0,
    E_p=1.0,
    materials=tungsten,
    phi=InterpolatedExpression(),
    K=1,
    n_max=1e2,
    A_0=6.1838e-03,
    E_A=0.2792,
)
trap_2 = F.Trap(
    k_0=5.22e-17, E_k=0.39, p_0=1e13 * 0, E_p=1.0, materials=tungsten, density=3
)
# my_model.traps = F.Traps([trap_1, trap_2])

# define temperature
my_model.T = F.Temperature(value=600)

# define boundary conditions
# bcs = [
#     F.DirichletBC(surfaces=[1, 2], value=3e22),
# ]
# my_model.boundary_conditions = bcs
my_model.initial_conditions = [F.InitialCondition(field="solute", value=3e22)]

# define settings
my_model.dt = F.Stepsize(initial_value=1, stepsize_change_ratio=1.05, dt_min=1e-8)
my_model.settings = F.Settings(
    absolute_tolerance=1e06,
    relative_tolerance=1e-08,
    maximum_iterations=50,
    final_time=8e5,
)

# define exports
my_derived_quantities = F.DerivedQuantities(filename="Results/derived_quantities.csv")
# my_derived_quantities.derived_quantities = [F.AverageVolume("1", volume=1)]

my_exports = F.Exports(
    [
        F.XDMFExport(
            "solute", label="solute", folder="Results", checkpoint=False, mode=1
        ),
        # F.XDMFExport("1", label="1", folder="Results", checkpoint=False, mode=1),
        # F.TrapDensityXDMF(
        #     trap=trap_1, label="density1", folder="results", checkpoint=False
        # ),
        # F.TrapDensityXDMF(
        #     trap=trap_2, label="density2", folder="results", checkpoint=False
        # ),
        my_derived_quantities,
    ]
)
my_model.exports = my_exports

# run simulation
my_model.initialise()
my_model.run()
