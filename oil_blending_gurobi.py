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
mod.addConstrs( quicksum(v_blends[o,g] for o in oil_names) == df_gas.loc[g,"demand"] + v_adv[g]*advert_return for g in gas_names)
### Maximum Capacity:
mod.addConstrs( quicksum(v_blends[o,g] for g in gas_names) <= df_oil.loc[o,"capacity"] for o in oil_names )
### Octane levels:
mod.addConstrs( quicksum(v_blends[o,g]*(df_oil.loc[o,"octane"] - df_gas.loc[g, "octane"]) for o in oil_names) >= 0 for g in gas_names )
### Lead:
mod.addConstrs(  quicksum(v_blends[o,g]*(df_oil.loc[o,"lead"] - df_gas.loc[g,"lead"]) for o in oil_names) <=0 for g in gas_names )
### Maximum production
mod.addConstr( quicksum(v_blends) <= production_max)

total_revenue = quicksum(v_blends[o,g] * df_gas.loc[g, "price"] for g in gas_names for o in oil_names)
total_production = production_cost * quicksum(v_blends)
total_oil_cost = quicksum( v_blends[o,g] * df_oil.loc[o, "price"] for g in gas_names for o in oil_names )
total_adv_cost = quicksum( v_adv )

mod.update()
mod.printStats()

mod.setObjective(total_revenue-total_production-total_oil_cost-total_adv_cost, sense=-1)

mod.optimize()

df_res_blend = pd.DataFrame({"var_value": v_blends})
df_res_blend.index.names = ["oil", "gas"]
df_res_blend = df_res_blend.var_value.apply(lambda x: x.X).unstack(level="oil")

df_res_adv = pd.DataFrame({"var_value": v_adv})
df_res_adv.index.names = ["gas"]
df_res_adv = df_res_adv.var_value.apply(lambda x: x.X)

