#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:26:38 2021

@author: Xingyun Wu
"""

import pandas as pd
import re


## read unemployment_v2 data because unemployment_v3 data has some mismatched county names
df0 = pd.read_csv('~/Desktop/Unemployment_v2.csv')
df0.columns
# get rid of multiple row index that was saved in v2 by mistake
df0 = df0.iloc[:, 5:]
df0.sort_values(by=['fips'], inplace = True)


## read current data
df1 = pd.read_excel('~/Documents/ra/HPC_datahub/unemployment/laucntycur14_20210620.xlsx',\
                   skiprows = [0, 1, 2, 3, 5, 45072, 45073, 45074],\
                   names = ['laus_code', 'stfips', 'ctyfips', 'loc', 'period',\
                            'laborforce', 'employed', 'unemployed', 'unemployment'])
df1.columns
# split county-state name column into county name and state name columns
df1[['ctyname', 'stname']] = df1['loc'].str.split(', ', expand = True)
# concatenate state fips with county fips
df1.ctyfips = df1.ctyfips.map("{:03}".format)
df1['fips'] = df1['stfips'].astype('str') + df1['ctyfips']
df1['period'] = df1['period'].str.strip('p').str.strip()


## reshape
df2 = df1[['stname', 'stfips', 'ctyname', 'ctyfips', 'fips', 'period', \
          'laborforce', 'unemployment']].copy()
# change format of period
df2['period'] = pd.to_datetime(df2['period'], format = '%b-%y').dt.strftime('%Y%m')
# reshape
df2 = df2.pivot(index = ['stname', 'stfips', 'ctyname', 'ctyfips', 'fips'],\
                columns = 'period').reset_index(drop = False)
# change multi-index after reshape to sinble index
df2.columns = [(x[0] + '_' + x[1]).strip('_') for x in df2.columns]
# change column type to prepare merging
df2['fips'] = df2['fips'].astype('int')
df2['ctyfips'] = df2['ctyfips'].astype('int64')
# sort rows by fips
df2.sort_values(by='fips', inplace = True)
# reset index as sequence number
df2.reset_index(drop = True, inplace = True)
df2.rename({'stname': 'stabbr'}, axis = 1, inplace = True)
#df2 = ctyfips.merge(df2, how = 'right', on = ['stfips', 'stabbr', 'ctyfips', 'ctyname', 'fips'])


## merge
# get rid of duplicate columns => if both occurs in df0 and df2, keep those in df2 (newer)
col_diff = list(df0.columns.difference(df2.columns))
col_diff = ['stfips', 'ctyfips', 'ctyname', 'fips'] + col_diff
df0 = df0[col_diff]
# merge df0 an df2
fnl = df0.merge(df2, how = 'left', on = ['stfips', 'ctyfips', 'fips'])
fnl.columns
# see different county names: ctyname_x, ctyname_y
t = []
for i in range(fnl.shape[0]):
    if fnl.ctyname_x[i] != fnl.ctyname_y[i]:
        t.append(i)
fnl.iloc[t, :][['ctyname_x', 'ctyname_y']]
# keep the original county name
fnl.rename({'ctyname_x': 'ctyname', 'neighbor1_2017': 'neighbor01_2017', \
            'neighbor2_2017': 'neighbor02_2017', 'neighbor3_2017': 'neighbor03_2017',\
            'neighbor4_2017': 'neighbor04_2017', 'neighbor5_2017': 'neighbor05_2017',\
            'neighbor6_2017': 'neighbor06_2017', 'neighbor7_2017': 'neighbor07_2017',\
            'neighbor8_2017': 'neighbor08_2017', 'neighbor9_2017': 'neighbor09_2017'},\
           axis = 1, inplace = True)
fnl.drop(columns = 'ctyname_y', inplace = True)
# reorder columns
fips_col = ['stfips', 'stabbr', 'stname', 'ctyfips', 'ctyname', 'fips']
fnl_col =  fips_col + sorted([x for x in fnl.columns if x not in fips_col])
fnl = fnl[fnl_col]
# sort fnl rows by fips to make sure
fnl.sort_values(by='fips', inplace = True)


## output data
fnl.to_csv('~/Documents/GitHub/COVID_DataHub/Unemployment/unemployment_v4.csv', \
           index = False, na_rep = '')


# get data dictionary
base_dict = pd.read_csv('~/Documents/GitHub/COVID_DataHub/Unemployment/unemployment_base_dictionary.csv')

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
fnl_dict.to_csv('~/Documents/GitHub/COVID_DataHub/Unemployment/unemployment_dictionary_v4.csv',\
                index = False)
