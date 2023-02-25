from neutron_induced_traps_model import festim_sim
import numpy as np


dpa_values = np.geomspace(1e-03, 1e03, num=50)
temperature_values = np.linspace(1300, 400, num=50)[:4]

for temperature in temperature_values:
    for dpa in dpa_values:
        print("Running case: dpa={:.2e}, T={:.0f}".format(dpa, temperature))
        festim_sim(
            T=temperature,
            dpa=dpa,
            results_folder_name="Results/parametric_studies/case_1e09s/dpa={:.2e}/T={:.0f}/".format(
                dpa, temperature
            ),
            transient_run=True,
            total_time=1e09,
        )
