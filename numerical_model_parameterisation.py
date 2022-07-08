import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotx

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

time = 30
final_time = 60


def numerical_model(n, t):
    dndt = phi*K*(1-(n/n_max)) - A_0*np.exp(-E_A/(k_B*T))*n
    return dndt


def analytical_model(t):
    A = phi*K
    B = A_0*np.exp(-E_A/(k_B*T))
    n_t = A*n_max/(A + B*n_max) + (A*n_0 - A*n_max + B*n_0*n_max) *\
        np.exp(t*(-A/n_max - B))/(A + B*n_max)
    return n_t


def ss_model(phi):
    A = phi*K
    B = A_0*np.exp(-E_A/(k_B*T))
    n_t = 1/((B/A)+(1/n_max))
    return n_t


# time points
t = np.linspace(0, final_time, 1000)

# ##### Analytical vs numerical comparison ##### #
phi = 1
K = 1
n_max = 5
A_0 = 0.1
E_A = 0.1034
k_B = 8.617333e-05
T = 1000

# initial condition
n_0 = 1

# time points
t_num = np.linspace(0, final_time, 30)
t_anal = np.linspace(0, final_time, 1000)

# values
y_num = odeint(numerical_model, n_0, t_num)
y_anal = analytical_model(t_anal)

# plot results
plt.figure()
ax = plt.gca()
plt.scatter(t_num, y_num, color="tab:blue", label='Numerical solution',
            marker='x')
plt.plot(t_anal, y_anal, color='black', label="Analytical solution")
plt.ylabel(r'Trap density, n$_{\mathrm{t}}$')
plt.xlabel(r'Time')
plt.xlim(0, final_time)
plt.ylim(0, n_max)
plt.xticks([])
plt.yticks([])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.legend(loc='lower right')

# ##### Varying temperature with time ##### #


def numerical_model_2(n, t_num):
    T = 1000*(t_num <= time) + (4000)*(t_num > time)
    dndt = phi*K*(1-(n/n_max)) - A_0*np.exp(-E_A/(k_B*T))*n
    return dndt


def analytical_model_2(t):
    T = 1000*(t <= time) + (4000)*(t > time)
    A = phi*K
    B = A_0*np.exp(-E_A/(k_B*T))
    n_t = A*n_max/(A + B*n_max) + (A*n_0 - A*n_max + B*n_0*n_max) *\
        np.exp(t*(-A/n_max - B))/(A + B*n_max)
    return n_t


y_num = odeint(numerical_model_2, n_0, t_num)
y_anal = analytical_model_2(t_anal)

plt.figure()
ax = plt.gca()
plt.scatter(t_num, y_num, color='tab:blue', label='Numerical solution', marker='x')
plt.plot(t_anal, y_anal, color='black', label="Analytical solution")
plt.ylabel(r'Trap density, n$_{\mathrm{t}}$')
plt.xlabel(r'Time')
plt.xlim(0, final_time)
plt.ylim(0, n_max)
plt.vlines(0.5*final_time, 0, n_max, color="tab:orange", linestyle="dashed", alpha=0.5)
plt.annotate("1000K", (0.2*final_time, 0.5*n_max), color="tab:orange", alpha=0.5)
plt.annotate("2000K", (0.7*final_time, 0.5*n_max), color="tab:orange", alpha=0.5)
plt.xticks([])
plt.yticks([])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.legend(loc='lower right')

# ############################## #
# ##### parametric studies ##### #
# ############################## #

# ##### Varience in T ##### #

T_span = np.linspace(100, 1800, 3)
plt.figure()
ax = plt.gca()
for T in T_span:
    y = odeint(numerical_model, n_0, t)
    plt.plot(t, y, label="{}K".format(int(T)), color="black")
plt.ylabel(r'Trap density, n$_{\mathrm{t}}$')
plt.xlabel(r'Time')
plt.xticks([])
plt.yticks([])
plt.annotate(r"T$_2$", (0.9*final_time, 0.815*n_max))
plt.annotate(r"T$_1$", (0.9*final_time, 0.9*n_max))
plt.annotate(r"T$_0$", (0.9*final_time, 1.025*n_max))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlim(0, final_time)
plt.ylim(0, n_max*1.1)

# ##### Varience in Phi.K ##### #

phi_span = np.linspace(0, 1, 3)
plt.figure()
ax = plt.gca()
for phi in phi_span:
    y = odeint(numerical_model, n_0, t)
    plt.plot(t, y, label="{:.2f}".format(phi), color='black')
plt.ylabel(r'Trap density, n$_{\mathrm{t}}$')
plt.xlabel(r'Time')
plt.xticks([])
plt.yticks([])
plt.annotate(r"$\phi_0$", (0.9*final_time, 0.05*n_max))
plt.annotate(r"$\phi_1$", (0.9*final_time, 0.7*n_max))
plt.annotate(r"$\phi_2$", (0.9*final_time, 0.85*n_max))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlim(0, final_time)
plt.ylim(0, n_max)

# ##### Varience in n_max ##### #

n_max_span = np.linspace(1, 15, 3)
plt.figure()
ax = plt.gca()
for n_max in n_max_span:
    y = odeint(numerical_model, n_0, t)
    plt.plot(t, y, label="{}".format(int(n_max)), color="black")
plt.ylabel(r'Trap density, n$_{\mathrm{t}}$')
plt.xlabel(r'Time')
plt.xticks([])
plt.yticks([])
plt.annotate(r"N$_0$", (0.9*final_time, 0.1*n_max))
plt.annotate(r"N$_1$", (0.9*final_time, 0.4*n_max))
plt.annotate(r"N$_2$", (0.9*final_time, 0.6*n_max))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlim(0, final_time)
plt.ylim(0, n_max)

# ##### Annealing effects ##### #

A_0_span = np.linspace(0, 3, 3)
plt.figure()
ax = plt.gca()
for A_0 in A_0_span:
    y = odeint(numerical_model, n_0, t)
    plt.plot(t, y, label="{}K".format(int(T)), color="black")
plt.ylabel(r'Trap density, n$_{\mathrm{t}}$')
plt.xlabel(r'Time')
plt.xticks([])
plt.yticks([])
plt.annotate(r"A$_0$", (0.9*final_time, 1.05*n_max))
plt.annotate(r"A$_1$", (0.9*final_time, 0.35*n_max))
plt.annotate(r"A$_2$", (0.9*final_time, 0.2*n_max))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlim(0, final_time)
plt.ylim(0, n_max*1.1)

# ##### varying E_A ##### #

T_2_span = np.linspace(100, 4000, 500)
plt.figure()
ax = plt.gca()
# E_A = 0.1034
E_A_values = np.linspace(0.1034, 0.1034*10, 10)
for E_A in E_A_values:
    n_values = []
    for T in T_2_span:
        phi = 0.1
        K = 1
        n_max = 5
        A_0 = 0.1
        k_B = 8.617333e-05
        y = ss_model()
        n_values.append(y)
    plt.plot(T_2_span, n_values, label="{:.0f}K".format(E_A/k_B), color="black")
plt.ylabel(r'Trap density, n$_{\mathrm{t}}$')
plt.xlabel(r'Temperature (K)')
# plt.legend()
plt.yticks([])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlim(left=0)

from labellines import labelLine, labelLines
labelLines(plt.gca().get_lines())

plt.show()
