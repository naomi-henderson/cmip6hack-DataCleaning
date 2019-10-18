#!/usr/bin/env python
# coding: utf-8

# ## First Attempt at converting the ES-DOC Errata ISSUES and into a CSV to use to filter our CMIP6 catalogs
# 
# - download the web-page: https://errata.es-doc.org/static/index.html as file.html
# ![es-doc](../assets/es-doc.png)

# In[ ]:


get_ipython().system(' /bin/grep "<tr id=" file.html > issues.txt')
# For now, edit issues.txt, keeping only the lines we need  


# In[10]:


import os
import pandas as pd
from glob import glob
import qgrid


# In[13]:


filepath = 'issues.txt'
with open(filepath) as fp:
    issues = []
    line = fp.readline()
    while line:
        issue = line.split('"')[1]
        issues += [issue]
        command = '/usr/bin/esgissue retrieve --id ' + issue
        #print(command)
        #os.system(command)
        line = fp.readline()


# In[4]:


import json

df = pd.DataFrame(columns=['uid', 'title', 'description', 'project', 'severity', 'status','urls'])

df_list = []
for item,issue in enumerate(issues):
    file_dsets = '/home/naomi/.esdoc/errata/dsets_dw/dset_'+issue+'.txt'
    file_issue = '/home/naomi/.esdoc/errata/issue_dw/issue_'+issue+'.json'
    
    with open(file_issue) as json_file:
        dict_issue = json.load(json_file)
   
    try:
        dlist = dict_issue['urls']
    except:
        dict_issue['urls'] = []
    
    df = df.append(dict_issue,ignore_index=True)
    df_dsets = pd.read_csv(file_dsets,delim_whitespace=True,header=None)
    df_dsets = df_dsets.rename(columns={0: "file_id"}).set_index([df_dsets.index])
    df_list += [list(df_dsets.file_id.values)]

df['file_ids'] = df_list
df = df.rename(columns={"uid": "issue_uid"})
#df.file_ids.values[0]


# In[5]:


df


# In[14]:


keywords = ['issue_uid','source_id', 'experiment_id', 'member_id', 'table_id', 'variable_id', 'grid_label', 'version', 'file_id']
df_all = []
for item, file_id in enumerate(df.file_ids.values):
    dfs = pd.DataFrame(columns=keywords)
    for file in file_id:
        #print(file)
        try:
            [fill,activity_id,institution_id,source_id,experiment_id,member_id,table_id,variable_id,grid_version] = file.split('.')
        except:
            print('not working for ',file)
        [grid_label,version] = grid_version.split('#')
        klist = [source_id,experiment_id,member_id,table_id,variable_id,grid_label,version,file]
        kdict = dict(zip(keywords, klist))
        dfs = dfs.append(kdict,ignore_index=True)
        df_all += [dfs]
df_expand = pd.concat(df_all,sort=False)


# In[15]:


qgrid.show_grid(df_expand)


# In[ ]:




