# import pkg.OptEngine as OptEngine
import mip
from time import time
from numba import jit
import numpy as np

# opt_model = OptEngine.OptModel(None, solver_type="ORTOOLS")
p_x = [0.5, 1, 2, 3]
p_y = [2, 3, 4, 5]
N = len(p_x)

mod = mip.Model(solver_name="CBC")
mod.verbose = 0
z = [mod.add_var(var_type="B", name="z[{}]".format(i)) for i in range(N-1)]
s = [mod.add_var(var_type="C", lb=0, ub=10, name="s[{}]".format(i)) for i in range(N-1)]

y = mod.add_var(lb=0, ub=100, name="y")

mod.add_constr(sum(z) == 1)

for i, j in zip(s, z):
    mod.add_constr(i <= j)

t = [0 for i in range(N)]
for i in range(N-1):
    t[i] += z[i] - s[i]
    t[i + 1] += s[i]

xx = 1.5

mod.add_constr(xx == np.array(p_x) @ np.array(t))
mod.add_constr(y == np.array(p_y) @ np.array(t))

# mod.update()

# mod.objective = y

t_s = time()
mod.optimize()
# print(y.solution_value())
t_e = time()

print(t_e - t_s)

