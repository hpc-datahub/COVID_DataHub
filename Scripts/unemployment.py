# -*- coding: utf-8 -*-
"""
Initially created on Mon Apr 26 12:26:38 2021
Modified on 2023-02-10, Yifeng Wan

Monthly update of BLS unemployment data on the basis of unemployment_v17
Make unemployment_v18

@author: Xingyun Wu
"""

import pandas as pd
import re
import os


###########
# initiate
###########

datadir = '~/Library/CloudStorage/OneDrive-JohnsHopkins/HPC_datahub/unemployment/'
outdir = '../Unemployment/'
version = 18
date = 20230210


#######
# data
#######

## read processed unemployment data from last month
dir_ = outdir + 'unemployment_v' + str(version - 1) + '.csv'
df0 = pd.read_csv(os.path.join(os.path.dirname(__file__), dir_)) # current file path
df0.columns
# drop the last month in df0 because the last month is always preliminary data
df0.drop(columns = ['laborforce_202211', 'unemployment_202211'], inplace = True)
df0.columns
df0.rename(columns = {'fips': 'scfips'}, inplace = True)


## read current data
df1 = pd.read_excel(datadir + 'laucntycur14_' + str(date) + '.xlsx',\
                    skiprows = [0, 1, 2, 3, 5, 45086, 45087, 45088, 45089],\
                    names = ['laus_code', 'stfips', 'ctyfips', 'loc', 'period',\
                             'laborforce', 'employed', 'unemployed', 'unemployment'])
# check columns in data
df1.columns
# check whether extract rows right
df1

# split county-state name column into county name and state name columns
df1[['ctyname', 'stname']] = df1['loc'].str.split(', ', expand = True)
# concatenate state fips with county fips
df1['stfips'] = df1['stfips'].astype('int')
df1.ctyfips = df1.ctyfips.map("{:03}".format)
# get state-county fips
df1['scfips'] = df1['stfips'].astype('str') + df1['ctyfips']
df1['period'] = df1['period'].str.strip('p').str.strip()
df1['period'] = df1['period'].str.strip('c').str.strip()


## reshape
df2 = df1[['stfips', 'stname', 'ctyfips', 'ctyname', 'scfips', 'period', \
          'laborforce', 'unemployment']].copy()
# change format of period
df2['period'] = pd.to_datetime(df2['period'], format = '%b-%y').dt.strftime('%Y%m')
# reshape
df2 = df2.pivot(index = ['stname', 'stfips', 'ctyname', 'ctyfips', 'scfips'],\
                columns = 'period').reset_index(drop = False)
# change multi-index after reshape to sinble index
df2.columns = [(x[0] + '_' + x[1]).strip('_') for x in df2.columns]
# change column type to prepare merging
df2['scfips'] = df2['scfips'].astype('int')
df2['ctyfips'] = df2['ctyfips'].astype('int')
# sort rows by fips
df2.sort_values(by='scfips', inplace = True)
# reset index as sequence number
df2.reset_index(drop = True, inplace = True)
df2.rename({'stname': 'stabbr'}, axis = 1, inplace = True)
df2.columns


## merge
# get rid of duplicate columns => if both occurs in df0 and df2, keep those in df2 (newer)
col_diff = list(df0.columns.difference(df2.columns))
col_diff.remove('stname')
col_d0 = ['stfips', 'stabbr', 'stname', 'ctyfips', 'ctyname', 'scfips'] + col_diff
df0 = df0[col_d0]
# merge df0 and df2
fnl = df0.merge(df2, how = 'left', on = ['stfips', 'stabbr', 'ctyfips', 'scfips'])
fnl.columns
# see different county names: ctyname_x, ctyname_y
t = []
for i in range(fnl.shape[0]):
    if fnl.ctyname_x[i] != fnl.ctyname_y[i]:
        t.append(i)
fnl.loc[t, ['ctyname_x', 'ctyname_y']]
fnl.iloc[t, :][['ctyname_x', 'ctyname_y']] # inspect
# keep the original county name
fnl.rename({'ctyname_x': 'ctyname'}, axis = 1, inplace = True)
fnl.drop(columns = 'ctyname_y', inplace = True)
# reorder columns
fips_col = ['stfips', 'stabbr', 'stname', 'ctyfips', 'ctyname', 'scfips']
fnl_col =  fips_col + sorted([x for x in fnl.columns if x not in fips_col])
fnl = fnl[fnl_col]
# sort fnl rows by fips to make sure
fnl.sort_values(by='scfips', inplace = True)
# check columns after merging
list(fnl.columns)


## output data
fnl.to_csv(os.path.join(os.path.dirname(__file__), outdir + 'unemployment_v' + str(version) + '.csv'), index = False, na_rep = '')


#############
# dictionary
#############
    
base_dict = pd.read_csv(datadir + 'unemployment_base_dictionary.csv')

d = {'variable_name': [] , 'start_column': [], 'end_column': [],\
     'start_month': [], 'end_month': []}

for i in range(base_dict.shape[0]):
    d['variable_name'].append(base_dict.loc[i, 'variable_name'])
    temp_var = base_dict.loc[i, 'variable_name'].replace('_yyyymm', '')
    if temp_var == 'fips':
        temp_id = [5]
    else:
        temp_id = [i for i, s in enumerate(fnl.columns) if temp_var in s]
    if len(temp_id) > 0:
        d['start_column'].append(temp_id[0] + 1)
        d['end_column'].append(temp_id[-1] + 1)
        if(len(temp_id) > 1):
            temp_month = [re.findall('20[\d]+', x)[0] for x in fnl.columns[temp_id]]
            d['start_month'].append(temp_month[0])
            d['end_month'].append(temp_month[-1])
        else:
            d['start_month'].append('')
            d['end_month'].append('')
    else:
        d['start_column'].append('')
        d['end_column'].append('')
        d['start_month'].append('')
        d['end_month'].append('')
        
fnl_dict = pd.DataFrame(d)
fnl_dict

# merge with base dictionary
fnl_dict = base_dict.merge(fnl_dict, how = 'outer', on = 'variable_name')

# save results
fnl_dict.to_csv(os.path.join(os.path.dirname(__file__), outdir + 'unemployment_dictionary_v' + str(version) + '.csv'), index = False)
