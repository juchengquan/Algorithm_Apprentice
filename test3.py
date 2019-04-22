import requests, json
import numpy as np
import pandas as pd
from datetime import datetime


#time = datetime.fromtimestamp(1555939857).strftime("%Y%m%d_%H%M%S")

url_list = "http://api.openweathermap.org/data/2.5/weather?units=metric&id=1880252&appid=a4578a7d1a079ac38e668076bc858513"
url_list = "https://api.darksky.net/forecast/1c698c75fe3d21783bcbea43a5328295/1.290270,103.851959,1555945200"


#1.28967,103.850067"

resp = requests.get(url=url_list, )
data_set = resp.json()

    #d[idx] = np.asarray( data_set["series"][0]["data"] )

    #p[idx] = dict(zip( d[idx][:,0].astype(str), d[idx][:,1].astype(float) ))


    #p[idx] = pd.DataFrame.from_dict(p[idx],orient="index",columns=[column_names[idx]])
    #ddd = d[idx]
    #mm = d[idx,-1]

#pp = pd.concat(p, axis=1, sort=True)
#pp.index = pd.DatetimeIndex(pp.index).strftime("%Y%m%d_%H")
"""
def convert_to_dict(data_set):
    data = {}
    data["time"] = datetime.fromtimestamp(data_set["dt"])
    data["cloudness"] = data_set["clouds"]["all"]
    data["coord_x"] = data_set["coord"]["lat"]
    data["coord_y"] = data_set["coord"]["lon"]
    data["id"] = data_set["id"]
    data["name"] = data_set["name"]
    data["visibility"] = data_set["visibility"]

    for key in data_set["weather"][0].keys():
        data["weather_"+key] = data_set["weather"][0][key]

    for key in data_set["wind"].keys():
        data["wind_"+key] = data_set["wind"][key]

    # in main:
    for key in data_set["main"].keys():
        data[key] = data_set["main"][key]

    return data

data = convert_to_dict(data_set)
mm = pd.DataFrame(data, index=[data["time"]])

mm.to_csv("test.csv", mode="a")
"""