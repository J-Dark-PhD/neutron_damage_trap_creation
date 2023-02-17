from neutron_induced_traps_model import festim_sim
import numpy as np

temperature_values = np.linspace(400, 1300, 100)
dpa_values = np.geomspace(1e-03, 1e03, num=7)

for temperature in temperature_values:
    for dpa in dpa_values:

        print(
            "Current step is temp = {:.1f} and dpa = {:.1e}".format(
                temperature, dpa
            )
        )

        results_folder_name = (
            "Results/damaged_traps_testing/{:.1f}K/{:.1e}_dpa/".format(
                temperature, dpa
            )
        )
        festim_sim(
            dpa=dpa, T=temperature, results_folder_name=results_folder_name, transient_run=False
        )