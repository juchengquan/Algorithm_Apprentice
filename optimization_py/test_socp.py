# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from docplex.mp.model import Model
#import gurobipy as gb
"""
mod = gb.Model()

x = mod.addVar(lb=0, ub=2, vtype="C")
y = mod.addVar(lb=0, ub=2, vtype="C")

mod.addConstr(x*x + y*y <= 1) 

mod.setObjective( x + y, sense=-1 )

mod.optimize()
"""
mod = Model(name="socp")

x = mod.continuous_var(lb=0, ub=10)
y = mod.continuous_var(lb=0, ub=10)
z = mod.continuous_var(lb=0, ub=10)

mod.add_constraint(x**2 + y**2 <= 1)
mod.set_objective( sense="max", expr=x+y,) 

mod.solve()
mod.report()
