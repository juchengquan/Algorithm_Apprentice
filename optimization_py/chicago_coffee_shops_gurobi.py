# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:03:18 2019

@author: cqju
"""

import requests 
import json 
import pandas as pd
import numpy as np
import gurobipy as gb
from gurobipy import quicksum

def get_dist(loc1, loc2):
    dist = (float(loc1[0]) - float(loc2[0]))**2 + (float(loc1[1])- float(loc2[1]))**2
    return dist

from geopy.distance import great_circle

def get_distance(loc1, loc2):
    return great_circle((float(loc1[0]), float(loc1[1])), (float(loc2[0]), float(loc2[1]))).miles

r = requests.get("https://data.cityofchicago.org/api/views/x8fc-8rcq/rows.json?accessType=DOWNLOAD") 
myjson = json.loads(r.text, parse_constant='utf-8')
myjson = myjson['data']


lat_list = []
lng_list = []
name_list = []
for ele in myjson:
    lat = ele[16][1]
    lng = ele[16][2]
    lat_list.append(float(lat))
    lng_list.append(float(lng))
    name_list.append(str(ele[10]))

    #print(lat, lng)
coor = np.array([lat_list, lng_list, name_list]).T
#del lat, lng, lat_list, lng_list

pd_coor = pd.DataFrame(coor)
pd_coor.columns = ["lat", "lng", "name"]

set_loc = pd_coor.index
set_coffee = pd_coor.index
nb_shops = 5

mod = gb.Model()

v_coffee = mod.addVars(set_loc, vtype="B")
v_link = mod.addVars(set_coffee, set_loc, vtype="B")

#for i in set_coffee:
#    for j in set_loc:
        
mod.addConstrs( v_link[c, l] <= v_coffee[c] for c in set_coffee for l in set_loc)

mod.addConstrs( quicksum(v_link[c,l] for c in set_coffee) == 1 for l in set_loc)

mod.addConstr( quicksum(v_coffee[c] for c in set_coffee) == nb_shops )

obj = quicksum( v_link[c,l] * get_distance(pd_coor.loc[c], pd_coor.loc[l]) for c in set_coffee for l in set_loc )

mod.setObjective(obj, sense=1)

mod.optimize()


df_res = pd.DataFrame({"v_coffee": v_coffee})
df_res = df_res.v_coffee.apply(lambda x: x.X)

coffee_name = pd_coor.name[df_res == 1]

print(coffee_name)

