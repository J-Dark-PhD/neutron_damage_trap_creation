from neutron_induced_traps_model import festim_sim
import numpy as np

dpa_values = np.geomspace(1e-03, 1e03, num=7)

for dpa in dpa_values:

    print("Current step is temp = 761 and dpa = {:.1e}".format(dpa))

    results_folder_name = "Results/damaged_traps_testing/761.0K/{:.1e}_dpa/".format(
        dpa
    )
    festim_sim(dpa=dpa, T=761, results_folder_name=results_folder_name, transient_run=False)
