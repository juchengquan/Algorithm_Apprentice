import numpy as np
import gurobipy as gb
from time import time

def test():
    mod = gb.Model()

    p_x = [0, 0.5, 1, 2, 3]
    p_y = [0, 2, 3, 4, 5]

    N = len(p_x)

    z = [mod.addVar(vtype="B", name="z[{}]".format(i)) for i in range(N-1)]
    s = [mod.addVar(vtype="C", name="s[{}]".format(i)) for i in range(N-1)]

    mod.addConstr(sum(z) == 1)

    for i, j in zip(s, z):
        mod.addConstr(i <= j)

    t = [0 for i in range(N)]
    for i in range(N-1):
        t[i] += z[i] - s[i]
        t[i + 1] += s[i]

    xx = 1.5  # power
    y = mod.addVar(vtype="C", name="y")  # cost
    mod.addConstr(xx == sum(p_x[i] * t[i] for i in range(N)))
    mod.addConstr(y == sum(p_y[i] * t[i] for i in range(N)))

    mod.update()

    mod.setObjective(y)

    t_s = time()
    mod.optimize()
    t_e = time()

    print(t_e - t_s)


test()
