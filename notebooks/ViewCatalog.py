#!/usr/bin/env python
# coding: utf-8

# <a id='top'></a>

# # Pangeo CMIP6 [Google Cloud Catalog](#catalog) and [NCAR/Glade Catalog](#NCARcatalog) Viewer 

# ### Helpful Links
# - To get started, '>Kernel >Restart Kernel & Run All Cells'
# - Check availability at: [ESGF](https://esgf-node.llnl.gov/search/cmip6/)
# - [Variable Names](#variables)
# - [Table Names](#tables)
# - [Model Information](#models)
# - Experiments: [Tier 1](#experiments1) [Tier 2](#experiments2) [Tier 3](#experiments3) [Tier 4](#experiments4)
# - Others: [Member_id](#member) [Grid_label](#grid)
# - file exceptions when concatenating in time: [Exceptions](#except)

# ## Google Cloud Catalog Viewer
# - Click on filters (top right of each column)
# - Reset by running 'widget' cell again

# In[9]:


import pandas as pd
import qgrid
dfcat = pd.read_csv('https://cmip6.storage.googleapis.com/cmip6.csv')
#dfcat = pd.read_csv('https://cmip6.storage.googleapis.com/cmip6-zarr-consolidated-stores.csv')
print('number of zstores:',dfcat.shape[0])


# <a id='catalog'></a>

# In[5]:


widget=qgrid.show_grid(dfcat.drop(['institution_id','dcpp_init_year'],1))
print('GCS Catalog')
widget


# In[4]:


# save results
df = widget.get_changed_df()     # use this to save filtered dataframe
# df = widget.get_selected_df()  # use this instead to save selected rows


# ## NCAR/Glade Catalog Viewer
# - Click on filters (top right of each column)
# - Reset by running 'widget' cell again

# In[7]:


import pandas as pd
import qgrid
dfcat2 = pd.read_csv('ftp://ftp.cgd.ucar.edu/archive/aletheia-data/intake-esm-datastore/catalogs/glade-cmip6.csv')

print('number of netcdf files:',dfcat2.shape[0])


# <a id='NCARcatalog'></a>

# In[6]:


widget=qgrid.show_grid(dfcat2.drop(['activity_id','institution_id','dcpp_init_year'],1))
print('NCAR/Glade Catalog')
widget


# In[7]:


# save results
df2 = widget.get_changed_df()     # use this to save filtered dataframe
# df2 = widget.get_selected_df()  # use this instead to save selected rows


# <a id='variables'></a>

# ## Variables
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)

# In[8]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/Variables.csv')
qgrid.show_grid(df, column_definitions={'description':{'width':400}})


# <a id='tables'></a>

# ## Tables
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)

# In[6]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/Tables.csv')
qgrid.show_grid(df, column_definitions={'description':{'width':400}})


# <a id='models'></a>

# # Model Information
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)

# In[8]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/Models.csv')
qgrid.show_grid(df)


# <a id='experiments1'></a>

# ## Tier 1 Experiments
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)

# In[11]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/Experiments_tier1.csv')
qgrid.show_grid(df)


# <a id='experiments2'></a>

# ## Tier 2 Experiments
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)

# In[12]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/Experiments_tier2.csv')
qgrid.show_grid(df)


# <a id='experiments3'></a>

# ## Tier 3 Experiments
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)

# In[13]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/Experiments_tier3.csv')
qgrid.show_grid(df)


# <a id='experiments4'></a>

# ## Tier 4 Experiments
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)

# In[14]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/Experiments_tier4.csv')
qgrid.show_grid(df)


# <a id='member'></a>

# ## member_id: 
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)
# 
# ```
# a key constructed from 4 indices stored as global attributes:
# 
# member_id = r<k>i<l>p<m>f<n>
# 
#        where
# 
#  k = realization_index
#  l = initialization_index
#  m = physics_index
#  n = forcing_index
# ```

# <a id='grid'></a>

# ## grid_label: 
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)
# ```
# a key indicating if on native grid, regridded, etc
# Modeling groups may choose to report their output on the model’s native grid and/or regrid it to one or more target grids. To distinguish between output reported on different grids, a “grid_label” attribute is defined.
# 
# The rules for assigning grid labels should make it easy for users to select (using the ESGF search tools) CMIP output that is on a grid considered by each
# modeling group to best represent its model -- the so-called “primary” grid. If output is reported on the native grid, this is always deemed the “primary”
# grid. If output is not reported on the native grid, then modeling groups should regrid the data to some primary grid of its choosing For the “primary”
# grid the following labels apply:
# 
# grid_label = "gn" (output is reported on the native grid)
# grid_label = "gr" (output is not reported on the native grid, but instead is regridded by the modeling group to a “primary grid” of its choosing)
# grid_label = “gm” (global mean output is reported, so data are not gridded)
# 
# As noted below sometimes a “z” or “a” or “g” is appended to the labels to indicate “zonal means” or grids limited to Antarctica or Greenland.
# If besides the “primary” grid, output is regridded to an additional grid, then for this output:
# grid_label = "gr[i]" (a “secondary” grid), where <i> should be replaced by a positive integer less than 10, which distinguishes this output from
# other regridded output.
# ```

# <a id='except'></a>

# ## time concatenation exceptions: 
# return to [GCS catalog](#catalog) or [NCAR catalog](#NCARcatalog)

# In[15]:


df = pd.read_csv('http://fletcher.ldeo.columbia.edu/catalogs/exceptions.csv')
qgrid.show_grid(df)


# [return to top](#top)

# Naomi Henderson (nhn2@columbia.edu), Oct 2019
