from ortools.linear_solver import pywraplp
from time import time
from numpy import sum

def test(a=True):
    mod = pywraplp.Solver("", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    p_x = [0.5, 1, 2, 3]
    p_y = [2, 3, 4, 5]


    N = len(p_x)


    z = [mod.BoolVar(name="z[{}]".format(i)) for i in range(N-1)]
    s = [mod.NumVar(lb=0, ub=10, name="s[{}]".format(i)) for i in range(N-1)]

    y = mod.NumVar(lb=0, ub=100, name="y")


    mod.Add(sum(z) == 1)

    for i, j in zip(s, z):
        mod.Add(i <= j)

    t = [0 for i in range(N)]
    for i in range(N-1):
        t[i] += z[i] - s[i]
        t[i + 1] += s[i]

    xx = 1.5

    xx_right = 0
    y_right = 0
    for i in range(N):
        xx_right += p_x[i] * t[i]
        y_right += p_y[i] * t[i]

    mod.Add(xx == xx_right)
    mod.Add(y == y_right)

    # mod.update()

    mod.Minimize(y)

    t_s = time()
    mod.Solve()
    print(y.solution_value())
    t_e = time()

    print(t_e - t_s)

    return a


    # mod.optimize()"""
test()
test()


