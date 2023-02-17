import matplotlib.pyplot as plt
from analytical_model_testing import (
    compare_annealing_and_detrapping,
    T_range,
)

(
    trap_1_detrapping_rates,
    trap_2_detrapping_rates,
    trap_3_detrapping_rates,
    trap_4_detrapping_rates,
    trap_5_detrapping_rates,
    trap_6_detrapping_rates,
    annealing_rates,
) = compare_annealing_and_detrapping()

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
# plt.plot(
#     T_range, trap_1_detrapping_rates, color="blue", alpha=0.8, label="De-trapping"
# )
# plt.plot(T_range, trap_2_detrapping_rates, color="blue", alpha=0.7)
plt.plot(T_range, trap_3_detrapping_rates, color="blue", alpha=0.3)
plt.plot(T_range, trap_4_detrapping_rates, color="blue", alpha=0.5)
plt.plot(T_range, trap_5_detrapping_rates, color="blue", alpha=0.7)
plt.plot(
    T_range, trap_6_detrapping_rates, color="blue", alpha=0.9, label="De-trapping"
)
plt.plot(T_range, annealing_rates, color="black", label="Annealing")

plt.annotate("1.15 eV", (1310, trap_3_detrapping_rates[-1] * 1.1), color="black")
plt.annotate("1.35 eV", (1310, trap_4_detrapping_rates[-1] * 0.4), color="black")
plt.annotate("1.65 eV", (1310, trap_5_detrapping_rates[-1] * 0.7), color="black")
plt.annotate("1.85 eV", (1310, trap_6_detrapping_rates[-1] * 0.5), color="black")

plt.yscale("log")
plt.legend()
plt.xlim(400, 1400)
plt.ylabel(r"Trapped tritium removal rate (s$^{-1}$)")
plt.xlabel(r"Temperature (K)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.show()