from neutron_induced_traps_model import festim_sim
import numpy as np
from os.path import exists


dpa_values = np.geomspace(1e-03, 1e03, num=50)
temperature_values = np.linspace(1300, 400, num=50)


def case_steady():
    for temperature in temperature_values:
        for dpa in dpa_values:
            print("Running case: dpa={:.2e}, T={:.0f}".format(dpa, temperature))
            festim_sim(
                T=temperature,
                dpa=dpa,
                results_folder_name="Results/parametric_studies/case_steady/dpa={:.2e}/T={:.0f}/".format(
                    dpa, temperature
                ),
                transient_run=False,
            )


def case_1e09s():
    results_folder = "Results/parametric_studies/case_1e09s_alt/"

    for temperature in temperature_values:
        for dpa in dpa_values:
            filename_test = (
                results_folder
                + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, temperature)
            )
            if exists(filename_test):
                continue
            else:
                print("Running case: dpa={:.2e}, T={:.0f}".format(dpa, temperature))
                festim_sim(
                    T=temperature,
                    dpa=dpa,
                    results_folder_name=results_folder
                    + "dpa={:.2e}/T={:.0f}/".format(dpa, temperature),
                    transient_run=True,
                    total_time=1e09,
                )


def case_1fpy():
    test_dpa_values = np.geomspace(1e-05, 1e03, num=10)
    results_folder = "Results/parametric_studies/case_1fpy/"

    for dpa in test_dpa_values:
        print("Running case: dpa={:.2e}".format(dpa))
        festim_sim(
            T=700,
            dpa=dpa,
            results_folder_name=results_folder + "dpa={:.2e}/T=700/".format(dpa),
            transient_run=True,
            total_time=3600 * 24 * 365.25,
        )


def case_24h():
    dpa_values = np.geomspace(1e-05, 1e03, num=17)
    temperature_values = np.linspace(400, 1300, num=50)

    results_folder = "Results/parametric_studies/case_24h/"

    for temperature in temperature_values:
        for dpa in dpa_values:
            filename_test = (
                results_folder
                + "dpa={:.2e}/T={:.0f}/derived_quantities.csv".format(dpa, temperature)
            )
            if exists(filename_test):
                continue
            else:
                print("Running case: dpa={:.2e}, T={:.0f}".format(dpa, temperature))
                festim_sim(
                    T=temperature,
                    dpa=dpa,
                    results_folder_name=results_folder
                    + "dpa={:.2e}/T={:.0f}/".format(dpa, temperature),
                    transient_run=True,
                    total_time=24 * 3600,
                )


# case_steady()
case_1e09s()
# case_1fpy()
# case_24h()
