import numpy as np

# dpa_para_values = np.linspace(0, 20, 41)
dpa_para_values = [0, 1, 5, 9, 20]
# temperature_values = np.linspace(400, 1300, 73)
temperature_values = np.linspace(400, 1300, 100)

inventories_by_T = []
inventories_by_T_normalised = []
inventories_by_dpa = []
inventories_by_dpa_normalised = []
inventories_761 = []

for T in temperature_values:
    inventories = []
    for dpa in dpa_para_values:
        filename = (
            "../damaged_traps_testing/{:.1f}K/{:.1f}_dpa/derived_quantities.csv".format(
                T, dpa
            )
        )
        data = np.genfromtxt(filename, delimiter=",", names=True)
        inventory = data["Total_retention_volume_1"]
        inventories.append(inventory)
    inventories_by_T.append(inventories)

for case in inventories_by_T:
    norm = np.array(case) / case[0]
    inventories_by_T_normalised.append(norm)

for dpa in dpa_para_values:
    inventories = []
    for T in temperature_values:
        filename = (
            "../damaged_traps_testing/{:.1f}K/{:.1f}_dpa/derived_quantities.csv".format(
                T, dpa
            )
        )
        data = np.genfromtxt(filename, delimiter=",", names=True)
        inventory = data["Total_retention_volume_1"]
        inventories.append(inventory)
    inventories_by_dpa.append(inventories)

for case in inventories_by_dpa:
    norm = np.array(case) / inventories_by_dpa[0]
    inventories_by_dpa_normalised.append(norm)

for dpa in dpa_para_values:
    filename = (
        "../damaged_traps_testing/761.0K/{:.1f}_dpa/derived_quantities.csv".format(dpa)
    )
    data = np.genfromtxt(filename, delimiter=",", names=True)
    inventory = data["Total_retention_volume_1"]
    inventories_761.append(inventory)
