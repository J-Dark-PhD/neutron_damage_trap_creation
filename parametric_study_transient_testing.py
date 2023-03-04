from neutron_induced_traps_model import festim_sim
import numpy as np


dpa_values = np.geomspace(1e-03, 1e03, num=50)
# temperature_values = np.linspace(1300, 400, num=50)
temperature_values = np.linspace(400, 1300, num=50)

dpa_values_1fpy = np.geomspace(1e-05, 1e03, num=9)


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


def case_1fpy():
    # for temperature in temperature_values:
    #     for dpa in dpa_values_1fpy:
    #         print("Running case: dpa={:.2e}, T={:.0f}".format(dpa, temperature))
    #         festim_sim(
    #             T=temperature,
    #             dpa=dpa,
    #             results_folder_name="Results/parametric_studies/case_1fpy/dpa={:.2e}/T={:.0f}/".format(
    #                 dpa, temperature
    #             ),
    #             transient_run=True,
    #             total_time=3600 * 24 * 365.25,
    #         )
    test_temperaure_values = np.linspace(400, 900, num=6)
    test_dpa_values = np.geomspace(1e-05, 1e01, num=7)
    # test_dpa_values = [1e-01]

    for temperature in test_temperaure_values:
        for dpa in test_dpa_values[4:]:
            print("Running case: dpa={:.2e}, T={:.0f}".format(dpa, temperature))
            festim_sim(
                T=temperature,
                dpa=dpa,
                results_folder_name="Results/parametric_studies/testing/dpa={:.2e}/T={:.0f}/".format(
                    dpa, temperature
                ),
                transient_run=True,
                total_time=3600 * 24 * 365.25,
            )


# case_steady()
# case_1e09s()
case_1fpy()
