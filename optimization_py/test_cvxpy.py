import numpy as np
import pandas as pd
import cvxpy as cp
#import cvxopt
#from cvxpy.reductions.solvers.defines import INSTALLED_SOLVERS

x = cp.Variable(shape=1,)
y = cp.Variable(shape=1)
const = []
const.append(x >= 0)
const.append(x <= 10)
const.append(y >= 0)
const.append(y <=10)
const.append(x**2 + y**2 <=1)

obj = x+y

mod = cp.Problem( cp.Maximize(obj), const )
mod.solve(solver="CVXOPT", verbose=True) 
