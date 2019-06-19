from ortools.linear_solver import pywraplp
import numpy as np


solver = pywraplp.Solver('simple_lp_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# Create the variables x and y.
x = solver.NumVar(0, 1, 'x')
y = solver.NumVar(0, 2, 'y')
z = np.array([solver.NumVar(0, 1, str(i)+str(j)) for i in range(3) for j in range(3)]).reshape(3,3)

# Create a linear constraint, 0 <= x + y <= 2.
#ct = solver.Constraint(0, 2, 'ct')
#ct.SetCoefficient(x, 1)
#ct.SetCoefficient(y, 1)
solver.Add(x + y <=2)
solver.Add(x + y >=0)

# Create the objective function, 3 * x + y.
solver.Maximize(3*x + y)
#objective = solver.Objective()
#objective.SetCoefficient(x, 3)
#objective.SetCoefficient(y, 1)
#objective.SetMaximization()

# Call the solver and display the results.
solver.Solve()
print('Solution:')
#print('Objective value = ', objective.Value())
print('x = ', x.solution_value())
print('y = ', y.solution_value())