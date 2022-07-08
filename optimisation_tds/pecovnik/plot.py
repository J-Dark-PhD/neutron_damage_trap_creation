import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import csv


flux = 5.6e19
implantation_time = 1.5e25/flux
implantation_time = 400
exposure_temp = 295
resting_time = 1*24*3600
ramp = 3/60
tds_time = (1000 - 300)/ramp


T_exp = []
d_exp = []

data_to_use = 'single'
# data_to_use = 'double'
# data_to_use = 'triple'

with open('Results/{}_damaged/{}_damaged.csv'.format(data_to_use,
                         data_to_use), 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        T_exp.append(float(row[0]))
        d_exp.append(float(row[1]))


plt.scatter(T_exp, d_exp, label="exp", color='black')

T_sim = []
flux1, flux2 = [], []
total_flux = []
solute = []
ret = []
t = []
trap1 = []
trap2 = []
# trap3 = []


with open('Results/derived_quantities/last.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if 't(s)' not in row:
            if float(row[0]) >= implantation_time + resting_time:
                t.append(float(row[0]))
                T_sim.append(float(row[1]))
                flux1.append(float(row[2]))
                flux2.append(float(row[3]))
                # solute.append(float(row[4]))
                # ret.append(float(row[5]))
                # trap1.append(float(row[6]))
                # trap2.append(float(row[7]))

# fields = [ret, solute, trap1, trap2]
# derivatives = [[] for i in range(len(fields))]

# legends = ["Total", "Solute", "Trap 1", "Trap 2"]
# for i in range(len(ret)-1):
#     for j in range(0, len(derivatives)):
#         derivatives[j].append(-(fields[j][i+1] - fields[j][i])/(t[i+1] - t[i]))

plt.plot(T_sim, -np.asarray(flux1)-np.asarray(flux2))
# plt.plot(T_sim, -np.asarray(flux2), label="flux2")
# T_sim.pop(0)
# for i in range(0, len(derivatives)):
#     if i != 0:
#         style = "dashed"
#         width = 0.8
#         plt.fill_between(T_sim, 0, derivatives[i], facecolor='grey', alpha=0.1)
#     else:
#         style = "-"
#         width = 1.7
#     if i != 1:
#         plt.plot(T_sim, derivatives[i], linewidth=width, linestyle=style, label=legends[i], alpha=1)

plt.xlim(300, 1000)
plt.ylim(0, 6e17)
plt.xlabel('T(K)')
plt.ylabel(r'Desorption flux (D/m$ ^{2}$/s)')
plt.title('TDS')
plt.legend()
plt.savefig("out.png")
plt.show()
