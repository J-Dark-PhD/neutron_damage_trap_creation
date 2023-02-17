from neutron_induced_traps_model import festim_sim
import numpy as np

temperature_values = np.linspace(400, 1300, 100)

for temperature in temperature_values:

    print("Current step is temp = {:.1f} and dpa = 0".format(temperature))

    results_folder_name = "Results/damaged_traps_testing/{:.1f}K/0.0_dpa/".format(
        temperature
    )
    festim_sim(T=temperature, dpa=0, results_folder_name=results_folder_name)