#!/usr/bin/env python
# coding: utf-8

# ## CMIP6 Data Challenge
# - Current: 23 institutions, 48 models. As usual, the modelers were ambitious and feel pressure to get their data up quickly, leading to inevitable inconsistencies in the products.  
# 
# ### A. Current Situation
# - Some data is collected at a few large sites - the ESGF nodes.  Most remains at home institution - must be downloaded from there. Transfers are between 100Mbps to 100Kbps. All servers go up and down. Recently, even the LLNL ESGF search API goes down every weekend.
# 
# - We have collected a very small subset - about 600,000 netcdf files at NCAR/Glade, most < 2.1 G, split in `time` dimension.
# 
# - We have concatenated netcdf in time (using `xarray`, saving as `zarr` stores) - about 30,000 zarr stores in Google Cloud. The time concatenation is very problematic.
# 
# ### B. Goals
# - Various 'reduction' products
# - Visualization techniques
# - Multi-model means
# 
# ### How to go from A -> B ?????
# - Data Cleaning - much, much work remains
# - Regridding (space and time)
#     - tripolar ocean grids, unstructured, ...
#     - time issues, e.g., is 'Oyr' reported at end of year (CESM2) or middle of year (everyone else)
# - Methods, methods, methods for doing our usual analyses
# - New tools, improved tools
# 
# 
# ### Data Cleaning - my project for the Hackathon
# - quick intro, following [intake-esm tutorial](https://intake-esm.readthedocs.io/en/latest/notebooks/tutorial.html)

# In[1]:


import numpy as np
import pandas as pd
import xarray as xr
import gcsfs

import warnings
warnings.simplefilter("ignore")


# In[2]:


fs = gcsfs.GCSFileSystem(token='anon', access='read_only')


# In[3]:


# define a simple search on keywords
def search_df(df, verbose= False, **search):
    "search by keywords - if list, then match exactly, otherwise match as substring"
    keys = ['activity_id','institution_id','source_id','experiment_id','member_id', 'table_id', 'variable_id', 'grid_label']
    d = df
    for skey in search.keys():
        
        if isinstance(search[skey], str):  # match a string as a substring
            d = d[d[skey].str.contains(search[skey])]
        else:
            dk = []
            for key in search[skey]:       # match a list of strings exactly
                dk += [d[d[skey]==key]]
            d = pd.concat(dk)
            keys.remove(skey)
    if verbose:
        for key in keys:
            print(key,' = ',list(d[key].unique()))      
    return d


# Open CMIP6 catalog in Pangeo's Google storage. 

# In[4]:


cat = pd.read_csv('https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv')
#cat = pd.read_csv('ftp://ftp.cgd.ucar.edu/archive/aletheia-data/intake-esm-datastore/catalogs/glade-cmip6.csv')
cat.info()


# view the `pandas.DataFrame` as follows:

# In[5]:


cat.head()


# ### Searching for specific datasets
# Let's find all the dissolved oxygen data at annual frequency from the ocean for the `piControl` experiment.

# In[6]:


subcat = search_df(cat, experiment_id=['piControl'], table_id='Oyr', variable_id=['o2'], 
                   grid_label=['gn'], verbose=True)


# In[7]:


len(subcat), len(cat)


# ## Loading data
# 
# - Blind aggregations rarely work with CMIP6
# - Especially important to LOOK at datasets you are getting for 4-D ocean data !!!
# - IPSL changed their depth coordinate name from deptht to olevel (sometimes in the middle of a run!)

# make a dictionary, called `dset_dict`, of `xarray.Dataset`s

# In[8]:


zstores = subcat.zstore.unique()

dset_dict = {}
for zstore in zstores:
    name = zstore.split('gs://cmip6/')[1].replace('/','.')[:-1]
    print(name)

    ds = xr.open_zarr(fs.get_mapper(zstore))       # DO NOT USE "decode_times = False"
    print(dict(ds.dims),'\n')
    
    dset_dict[name] = ds


# In[ ]:


dset_dict.keys()


# We can access a particular dataset as follows:

# In[ ]:


# use <TAB> to complete the names
ds = dset_dict['CMIP.']
ds


# In[ ]:


ds.o2.isel(time=0, lev=0).plot()


# In[ ]:


# combine ensemble members? 

model = 'CanESM5'
names = dset_dict.keys()

# make a list of all datasets for this model:

pick = [dset_dict[name] for name in names if model in name] 
xr.concat(pick,dim='member')


# We can execute more searches against the original catalog and/or against a subset of the original catalog:

# In[ ]:


get_ipython().run_cell_magic('time', '', "cat_Ofx = search_df(cat, table_id='Ofx', variable_id='volcello', grid_label=['gn'])\ncat_Ofx")


# In[ ]:


dfa = search_df(cat_Ofx, source_id = ["CESM2"], verbose=True)
dfa


# In[ ]:




