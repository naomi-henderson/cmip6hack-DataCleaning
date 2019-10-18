#!/usr/bin/env python
# coding: utf-8

# ## Part 2.
# Here we are constructing a new database for collecting common issues and solutions going forward from here. Includes @naomi-henderson 's dataset of exceptions when concatenating the netcdf files in time to create the zarr stores for Googel Cloud Storage.
# 
# ![ExceptionsForm](../assets/Form.png)

# In[1]:


import os
import pandas as pd
import numpy as np
import my_search
import xarray as xr
import cftime
import qgrid
xr.__version__


# In[45]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/exceptions.csv')


# In[46]:


df


# In[47]:


cat = pd.read_csv('https://cmip6.storage.googleapis.com/cmip6.csv')


# In[65]:


# define a simple search on keywords
def search_df(df, **search):
    d = df
    for skey in search.keys():
        #print(skey,search[skey])
        d = d [ d[skey] == search[skey] ]
    return d


# In[68]:


keys = ['source_id','experiment_id','member_id', 'table_id', 'variable_id', 'grid_label'] 
dfall = []
for index, row in df[0:].iterrows():
    drow = row.to_dict()
    del drow['reason_code']
    del drow['reason_txt']
    if drow['variable_id'] == 'all'
    dfall += [search_df(cat,**drow)]
dfcat = pd.concat(dfall,sort=False)
qgrid.show_grid(dfcat)


# In[1]:


# grab tracking id from a zarr:
tracking_id = "hdl:21.14100/dca6a9f1-0ab9-4ab4-a661-9c49955bbd99\nhdl:21.14100/c13d7735-561e-4d34-9a9e-ec587ad18a2f\nhdl:21.14100/27d2a2f1-4ef7-4dfd-b1aa-c912ce569054\nhdl:21.14100/b36801f6-359a-4ce4-a423-f89676444659\nhdl:21.14100/7d61d119-9c99-4afa-9376-cd016c6520b6\nhdl:21.14100/2ebfd9a7-dea1-4bb6-97c1-a636901ed2e1\nhdl:21.14100/c5563f39-a6c7-41c8-a6e4-9221859019c9\nhdl:21.14100/f55c6182-0bfb-45c5-bebb-98af2465f6f5\nhdl:21.14100/e5dd99a9-df00-4c9b-93b2-e3d831a16d4e"


# In[4]:


tracks = tracking_id.split('\n')


# In[ ]:


import my_search
import pandas as pd

df_list = []
for track in tracks:
    files= my_search.esgf_search(server="https://esgf-node.llnl.gov/esg-search/search", mip_era='CMIP6', tracking_id=track, 
                                     page_size=500, verbose=False)
    files.loc[:,'version'] = [str.split('/')[-2] for str in files['HTTPServer_url']]
    files.loc[:,'file_name'] = [str.split('/')[-1] for str in files['HTTPServer_url']]
    # might need to set activity_id to activity_drs for some files (see old versions)
    files.loc[:,'activity_id'] = files.activity_drs
    files.loc[:,'time_range'] = [str[-28:-3] for str in files['file_name']]
    files.loc[:,'century'] = [str[-28:-26] for str in files['file_name']]
    #if (experiment_id=='highresSST-present')&(('3hr' in table_id)|('6hr' in table_id)):
    #    files = files[files.century=='20'] 

    df_list += [files.drop_duplicates(subset =["file_name","version","checksum"]) ]
dESGF = pd.concat(df_list,sort=False)
dESGF = dESGF.drop_duplicates(subset =["file_name","version","checksum"])


# In[13]:


dESGF.keys()


# In[19]:


dESGF.dataset_id.values


# In[18]:


dESGF.time_range


# In[21]:


dESGF.HTTPServer_url.values


# In[22]:


dESGF.retracted


# In[23]:


dESGF.replica


# In[ ]:




