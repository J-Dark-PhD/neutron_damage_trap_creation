from neutron_induced_traps_model import festim_sim
import numpy as np


dpa_values = np.geomspace(1e-03, 1e03, num=7)

for dpa in dpa_values:
    festim_sim(
        T=761,
        dpa=dpa,
        results_folder_name="Results/transient_testing/{:.0e}_dpa/".format(dpa),
        transient_run=True
    )