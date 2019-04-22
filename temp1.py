import requests
import numpy as np
import pandas as pd
#from datetime import datetime


url_list = ["https://api.data.gov.sg/v1/environment/air-temperature?date=2019-04-20"]
url_list = ["https://api.data.gov.sg/v1/transport/taxi-availability?date_time=2019-04-20T00%3A40%3A00%2B08%3A00"]
url_list = ["https://data.gov.sg/api/action/datastore_search?resource_id=85e22503-74c8-43a1-8cee-f4e4b1d9c5fc&limit=10"]
column_names = ["Day-ahead forcast", "Real"]

d = [None for i in range(len(url_list))]
p = [None for i in range(len(url_list))]
for idx, url in enumerate(url_list):
    resp = requests.get(url=url, )
    data_set = resp.json()

    d[idx] = np.asarray( data_set["series"][0]["data"] )
    
    p[idx] = dict(zip( d[idx][:,0].astype(str), d[idx][:,1].astype(float) ))
    
    
    p[idx] = pd.DataFrame.from_dict(p[idx],orient="index",columns=[column_names[idx]])
    #ddd = d[idx]
    #mm = d[idx,-1]

pp = pd.concat(p, axis=1, sort=True)
pp.index = pd.DatetimeIndex(pp.index).strftime("%Y%m%d_%H")