# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from docplex.mp.model import Model
import gurobipy as gb
#from gurobipy import quicksum

energies = ["coal", "gas", "diesel", "wind"]
df_energy = pd.DataFrame({"co2_cost": [30, 5, 15, 0]}, index=energies)

all_units = ["coal1", "coal2", 
             "gas1", "gas2", "gas3", "gas4", 
             "diesel1", "diesel2", "diesel3", "diesel4"]
             
ucp_raw_unit_data = {
        "energy": ["coal", "coal", "gas", "gas", "gas", "gas", "diesel", "diesel", "diesel", "diesel"],
        "initial" : [400, 350, 205, 52, 155, 150, 78, 76, 0, 0],
        "min_gen": [100, 140, 78, 52, 54.25, 39, 17.4, 15.2, 4, 2.4],
        "max_gen": [425, 365, 220, 210, 165, 158, 90, 87, 20, 12],
        "operating_max_gen": [400, 350, 205, 197, 155, 150, 78, 76, 20, 12],
        "min_uptime": [15, 15, 6, 5, 5, 4, 3, 3, 1, 1],
        "min_downtime":[9, 8, 7, 4, 3, 2, 2, 2, 1, 1],
        "ramp_up":   [212, 150, 101.2, 94.8, 58, 50, 40, 60, 20, 12],
        "ramp_down": [183, 198, 95.6, 101.7, 77.5, 60, 24, 45, 20, 12],
        "start_cost": [5000, 4550, 1320, 1291, 1280, 1105, 560, 554, 300, 250],
        "fixed_cost": [208.61, 117.37, 174.12, 172.75, 95.353, 144.52, 54.417, 54.551, 79.638, 16.259],
        "variable_cost": [22.536, 31.985, 70.5, 69, 32.146, 54.84, 40.222, 40.522, 116.33, 76.642],
        }

df_units = pd.DataFrame(ucp_raw_unit_data, index=all_units)

# Add a derived co2-cost column by merging with df_energies
# Use energy key from units and index from energy dataframe
df_up = pd.merge(df_units, df_energy, left_on="energy", right_index=True)
df_up.index.names=['units']


raw_demand = [1259.0, 1439.0, 1289.0, 1211.0, 1433.0, 1287.0, 1285.0, 1227.0, 1269.0, 1158.0, 1277.0, 1417.0, 1294.0, 1396.0, 1414.0, 1386.0,
              1302.0, 1215.0, 1433.0, 1354.0, 1436.0, 1285.0, 1332.0, 1172.0, 1446.0, 1367.0, 1243.0, 1275.0, 1363.0, 1208.0, 1394.0, 1345.0, 
              1217.0, 1432.0, 1431.0, 1356.0, 1360.0, 1364.0, 1286.0, 1440.0, 1440.0, 1313.0, 1389.0, 1385.0, 1265.0, 1442.0, 1435.0, 1432.0, 
              1280.0, 1411.0, 1440.0, 1258.0, 1333.0, 1293.0, 1193.0, 1440.0, 1306.0, 1264.0, 1244.0, 1368.0, 1437.0, 1236.0, 1354.0, 1356.0, 
              1383.0, 1350.0, 1354.0, 1329.0, 1427.0, 1163.0, 1339.0, 1351.0, 1174.0, 1235.0, 1439.0, 1235.0, 1245.0, 1262.0, 1362.0, 1184.0, 
              1207.0, 1359.0, 1443.0, 1205.0, 1192.0, 1364.0, 1233.0, 1281.0, 1295.0, 1357.0, 1191.0, 1329.0, 1294.0, 1334.0, 1265.0, 1207.0, 
              1365.0, 1432.0, 1199.0, 1191.0, 1411.0, 1294.0, 1244.0, 1256.0, 1257.0, 1224.0, 1277.0, 1246.0, 1243.0, 1194.0, 1389.0, 1366.0, 
              1282.0, 1221.0, 1255.0, 1417.0, 1358.0, 1264.0, 1205.0, 1254.0, 1276.0, 1435.0, 1335.0, 1355.0, 1337.0, 1197.0, 1423.0, 1194.0, 
              1310.0, 1255.0, 1300.0, 1388.0, 1385.0, 1255.0, 1434.0, 1232.0, 1402.0, 1435.0, 1160.0, 1193.0, 1422.0, 1235.0, 1219.0, 1410.0, 
              1363.0, 1361.0, 1437.0, 1407.0, 1164.0, 1392.0, 1408.0, 1196.0, 1430.0, 1264.0, 1289.0, 1434.0, 1216.0, 1340.0, 1327.0, 1230.0, 
              1362.0, 1360.0, 1448.0, 1220.0, 1435.0, 1425.0, 1413.0, 1279.0, 1269.0, 1162.0, 1437.0, 1441.0, 1433.0, 1307.0, 1436.0, 1357.0, 
              1437.0, 1308.0, 1207.0, 1420.0, 1338.0, 1311.0, 1328.0, 1417.0, 1394.0, 1336.0, 1160.0, 1231.0, 1422.0, 1294.0, 1434.0, 1289.0]
nb_periods = len(raw_demand)
print("nb periods = {}".format(nb_periods))

demand = pd.Series(raw_demand, index = range(0, nb_periods))


### MODEL 
ucpm = Model("ucp")

units = all_units
# periods range from 1 to nb_periods included
periods = range(nb_periods)

### Gurobi Model
mod = gb.Model()

in_use = mod.addVars(units, periods, vtype="B")
turn_on = mod.addVars(units, periods, vtype="B")
turn_off = mod.addVars(units, periods, vtype="B")
production = mod.addVars(units, periods, vtype="C")
mod.update()

# Organize all decision variables in a DataFrame indexed by 'units' and 'periods'
df_decision_vars = pd.DataFrame({'in_use': in_use, 'turn_on': turn_on, 'turn_off': turn_off, 'production': production})
# Set index names
df_decision_vars.index.names=['units', 'periods']

# Display first few rows of 'df_decision_vars' DataFrame
df_decision_vars.head()

# Create a join between 'df_decision_vars' and 'df_up' Data Frames based on common index id (ie: 'units')
# In 'df_up', one keeps only relevant columns: 'min_gen' and 'max_gen'
df_join_decision_vars_up = df_decision_vars.join(df_up[['min_gen', 'max_gen']], how='inner')

# Display first few rows of joined Data Frames
df_join_decision_vars_up.head()


### ADDING CONSTRAINTS

# When in use, the production level is constrained to be between min and max generation.
for item in df_join_decision_vars_up.itertuples(index=False):
    mod.addConstr(item.production <= item.max_gen * item.in_use)
    mod.addConstr(item.production >= item.min_gen * item.in_use)
    #print("adding contraints")

# Initial state
# If initial production is nonzero, then period #1 is not a turn_on
# else turn_on equals in_use
# Dual logic is implemented for turn_off
for u in units:
    if df_up.initial[u] > 0:
        # if u is already running, not starting up
        mod.addConstr(turn_on[u,0] == 0)
        # turnoff iff not in use
        mod.addConstr(turn_off[u,0]+in_use[u,0] == 1)
    else:
        # turn on at 1 iff in use at 1
        # ucpm.add_constraint(turn_on[u, 1] == in_use[u, 1])
        mod.addConstr(turn_on[u,0] == in_use[u,0])
        # already off, not switched off at t==1
        mod.addConstr(turn_off[u,0] == in_use[u,0])


# Use groupby operation to process each unit
for unit, r in df_decision_vars.groupby(level='units'):
    u_ramp_up = df_up.ramp_up[unit]
    u_ramp_down = df_up.ramp_down[unit]
    u_initial = df_up.initial[unit]
    # Initial ramp up/down
    # Note that r.production is a Series that can be indexed as an array (ie: first item index = 0)
    mod.addConstr(r.production[0] - u_initial <= u_ramp_up)
    mod.addConstr(u_initial - r.production[0] <= u_ramp_down)

    for (p_curr, p_next) in zip(r.production, r.production[1:]):
        mod.addConstr(p_next - p_curr <= u_ramp_up)
        mod.addConstr(p_curr - p_next <= u_ramp_down)
del unit, r, u_initial, u_ramp_up, u_ramp_down

# Turn_on, turn_off
# Use groupby operation to process each unit
for unit, r in df_decision_vars.groupby(level='units'):
    for (in_use_curr, in_use_next, turn_on_next, turn_off_next) in zip(r.in_use, r.in_use[1:], r.turn_on[1:], r.turn_off[1:]):
        # if unit is off at time t and on at time t+1, then it was turned on at time t+1
        mod.addConstr(in_use_next - in_use_curr <= turn_on_next)
        # if unit is on at time t and off at time t+1, then it was turned off at time t+1
        mod.addConstr(in_use_curr - in_use_next + turn_on_next == turn_off_next)

# Minimum uptime, downtime
for unit, r in df_decision_vars.groupby(level='units'):
    min_uptime   = df_up.min_uptime[unit]
    min_downtime = df_up.min_downtime[unit]
    # Note that r.turn_on and r.in_use are Series that can be indexed as arrays (ie: first item index = 0)
    for t in range(min_uptime-1, nb_periods):
        mod.addConstr(np.sum(r.turn_on[(t - min_uptime) + 1:t + 1]) <= r.in_use[t])

    for t in range(min_downtime-1, nb_periods):
        mod.addConstr(np.sum(r.turn_off[(t - min_downtime) + 1:t + 1]) <= 1 - r.in_use[t])


# Enforcing demand
# we use a >= here to be more robust, 
# objective will ensure  we produce efficiently
for period, r in df_decision_vars.groupby(level='periods'):
    total_demand = demand[period]
    mod.addConstr(np.sum(r.production) >= total_demand) 

mod.update()
mod.printStats()

# Create a join between 'df_decision_vars' and 'df_up' Data Frames based on common index ids (ie: 'units')
# In 'df_up', one keeps only relevant columns: 'fixed_cost', 'variable_cost', 'start_cost' and 'co2_cost'
df_join_obj = df_decision_vars.join(
    df_up[['fixed_cost', 'variable_cost', 'start_cost', 'co2_cost']], how='inner')

# Display first few rows of joined Data Frame
#df_join_obj.head()


# objective
total_fixed_cost = np.sum(df_join_obj.in_use * df_join_obj.fixed_cost)
total_variable_cost = np.sum(df_join_obj.production * df_join_obj.variable_cost)
total_startup_cost = np.sum(df_join_obj.turn_on * df_join_obj.start_cost)
total_co2_cost = np.sum(df_join_obj.production * df_join_obj.co2_cost)
total_economic_cost = total_fixed_cost + total_variable_cost + total_startup_cost

total_nb_used = np.sum(df_decision_vars.in_use)
total_nb_starts = np.sum(df_decision_vars.turn_on)

# store expression kpis to retrieve them later.
"""
ucpm.add_kpi(total_fixed_cost   , "Total Fixed Cost")
ucpm.add_kpi(total_variable_cost, "Total Variable Cost")
ucpm.add_kpi(total_startup_cost , "Total Startup Cost")
ucpm.add_kpi(total_economic_cost, "Total Economic Cost")
ucpm.add_kpi(total_co2_cost     , "Total CO2 Cost")
ucpm.add_kpi(total_nb_used, "Total #used")
ucpm.add_kpi(total_nb_starts, "Total #starts")
"""

# minimize sum of all costs
mod.setObjective( total_fixed_cost + total_variable_cost + total_startup_cost + total_co2_cost )

mod.update()
mod.optimize()

df_prods = df_decision_vars.production.apply(lambda v: v.X).unstack(level='units')
df_used = df_decision_vars.in_use.apply(lambda v: v.X).unstack(level='units')
df_started = df_decision_vars.turn_on.apply(lambda v: v.X).unstack(level='units')

# Display the first few rows of the pivoted 'production' data
df_prods.head()

df_spins = pd.DataFrame(df_up.max_gen.to_dict(), index=periods) - df_prods

# Display the first few rows of the 'df_spins' Data Frame, representing the reserve for each unit, over time
df_spins.head()

df_spins.coal2.plot(style='o-', ylim=[0,200]) 

df_used.sum(axis=1).plot(title="Number of plants online", kind='line', style="r-", ylim=[0, len(units)])

