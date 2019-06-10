# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import gurobipy as gb
from gurobipy import quicksum

### IMPORT DATA
gas_names = ["super", "regular", "diesel"]
gas_data = np.array([[3000, 70, 10, 1], [2000, 60, 8, 2], [1000, 50, 6, 1]])
oil_names = ["crude1", "crude2", "crude3"]
oil_data = np.array([[5000, 45, 12, 0.5], [5000, 35, 6, 2], [5000, 25, 8, 3]])

# global data
production_cost = 4
production_max = 14000
# each $1 spent on advertising increases demand by 10.
advert_return = 10

nb_gas  = len(gas_names)
nb_oils = len(oil_names)
range_gas = range(nb_gas)
range_oil = range(nb_oils)
#print("Number of gasoline types = {0}".format(nb_gas))
#print("Number of crude types = {0}".format(nb_oils))


df_gas = pd.DataFrame(gas_data)
df_oil = pd.DataFrame(oil_data)
df_gas.index = gas_names
df_oil.index= oil_names
df_gas.columns = ['demand','price','octane','lead']
df_oil.columns = ['capacity','price','octane','lead']

mod = gb.Model("oil_blending")

v_blends = mod.addVars(oil_names, gas_names, vtype="C", lb=0)
v_adv = mod.addVars(gas_names, vtype="C", lb=0)

### Demand:
mod.addConstrs( quicksum(v_blends[o,g] for o in oil_names) == df_gas.loc[g,"demand"] for g in gas_names)

### Maximum Capacity:
mod.addConstrs( quicksum(v_blends[o,g] for g in gas_names) <= df_oil.loc[o,"capacity"] for o in oil_names )

### Octane and Lead levels
mod.addConstrs(  )


mod.update()
mod.printStats()
