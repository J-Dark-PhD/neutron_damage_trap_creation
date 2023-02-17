import sympy as sp
import numpy as np

t, F, A = sp.symbols("t F A")
n_max, n_0 = sp.symbols("n_max, n_0", integer=True)

n = sp.Function("n")(t)
ics = {n.subs(t, 0): n_0}

# ##### Just Creation ##### #
dndt_cr = sp.Eq(n.diff(t), F * (1 - (n / n_max)))
sol_cr = sp.dsolve(dndt_cr, ics=ics, simplify=True)
print("Just creation effects = ", sol_cr)

# ##### Just annealing effects ##### #
dndt_an = sp.Eq(n.diff(t), -A * n)
sol_an = sp.dsolve(dndt_an, ics=ics, simplify=True)
print("Just Annleaing effects = ", sol_an)

# ##### Creation with annealing ##### #
dndt = sp.Eq(n.diff(t), F * (1 - (n / n_max)) - A * n)
sol = sp.dsolve(dndt, ics=ics, simplify=True)
print("Creation and annealing = ", sol)
