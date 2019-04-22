import requests
import numpy as np
import pandas as pd
#from datetime import datetime


url_list = ["http://api.eia.gov/series/?api_key=c6581939be6f0e59b490fc62584d5931&series_id=EBA.PJM-ALL.DF.H&start=20160101&end=20190101",
       "http://api.eia.gov/series/?api_key=c6581939be6f0e59b490fc62584d5931&series_id=EBA.PJM-ALL.D.H&start=20160101&end=20190101"]
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