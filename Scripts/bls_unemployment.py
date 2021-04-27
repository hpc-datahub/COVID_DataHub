#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:26:38 2021

@author: Xingyun Wu
"""

import pandas as pd


# FIPS code
stfips = state_territory_fips = pd.read_csv('~/Documents/GitHub/COVID_DataHub/Pandemic/fips/state_territory_fips.csv')


# read 2019 data
df0 = pd.read_csv('~/Documents/GitHub/COVID_DataHub/unemployment/Unemployment_v2.csv')
# drop the multiple index columns
df0 = df0.iloc[:, 5:]
df0
# reorder column names
t = list(df0.columns[5:])
t0 = t[:30].copy()
t1 = t[30:43].copy()
t2 = t[43:].copy()
tf = list(df0.columns[:5]) + sorted(t0 + t2) + t1
# reorder columns
df0 = df0[tf]
df0.reset_index(drop = True, inplace = True)
# check dtypes for merging keys
df0.dtypes
df0['stname'] = df0['stname'].astype('str')
df0 = stfips.merge(df0, how = 'right', on = ['stfips', 'stname'])


# read 2020 to current data
df1 = pd.read_excel('~/Documents/ra/HPC_datahub/unemployment/laucntycur14.xlsx',\
                   skiprows = [0, 1, 2, 3, 5, 45072, 45073, 45074],\
                   names = ['laus_code', 'stfips', 'ctyfips', 'loc', 'period',\
                            'laborforce', 'employed', 'unemployed', 'unemployment'])
df1
# split county-state name column into county name and state name columns
df1[['ctyname', 'stname']] = df1['loc'].str.split(', ', expand = True)
# concatenate state fips with county fips
df1.ctyfips = df1.ctyfips.map("{:03}".format)
df1['fips'] = df1['stfips'].astype('str') + df1['ctyfips']
df1['period'] = df1['period'].str.strip('p').str.strip()


# reshape
df2 = df1[['stname', 'stfips', 'ctyname', 'ctyfips', 'fips', 'period', \
          'laborforce', 'unemployment']].copy()
df2['period'] = pd.to_datetime(df2['period'], format = '%b-%y').dt.strftime('%Y%m')
df2 = df2.pivot(index = ['stname', 'stfips', 'ctyname', 'ctyfips', 'fips'],\
                columns = 'period').reset_index(drop = False)
df2.columns = [(x[0] + '_' + x[1]).strip('_') for x in df2.columns]
df2['fips'] = df2['fips'].astype('int')
df2['ctyfips'] = df2['ctyfips'].astype('int64')
df2.sort_values(by=['fips'], inplace = True)
df2.reset_index(drop = True, inplace = True)
df2.rename({'stname': 'stabbr'}, axis = 1, inplace = True)
df2 = stfips.merge(df2, how = 'right', on = ['stfips', 'stabbr'])


# get rid of duplicate columns => if both occurs in df0 and df2, keep those in df2 (newer)
col_diff = list(df0.columns.difference(df2.columns))
col_diff = ['stname', 'stfips', 'ctyname', 'ctyfips', 'fips'] + col_diff
df0 = df0[col_diff]
# merge df0 an df2
fnl = df0.merge(df2, how = 'outer', on = ['stfips', 'ctyfips', 'fips', 'stname', 'stabbr', 'ctyname'])
fnl.rename({'neighbor1_2017': 'neighbor01_2017', 'neighbor2_2017': 'neighbor02_2017',\
            'neighbor3_2017': 'neighbor03_2017', 'neighbor4_2017': 'neighbor04_2017',
            'neighbor5_2017': 'neighbor05_2017', 'neighbor6_2017': 'neighbor06_2017',
            'neighbor7_2017': 'neighbor07_2017', 'neighbor8_2017': 'neighbor08_2017',
            'neighbor9_2017': 'neighbor09_2017'}, axis = 1, inplace = True)
fnl_col = list(fnl.columns[:6]) + sorted(list(fnl.columns[6:]))
fnl = fnl[fnl_col]


# output data
fnl.to_csv('~/Documents/GitHub/COVID_DataHub/Unemployment/unemployment_v3.csv', \
           index = False, na_rep = '')


# get data dictionary
df3 = pd.DataFrame(fnl.columns)
df3.columns = ['variable_name']
df3.to_csv('~/Documents/GitHub/COVID_DataHub/Unemployment/unemployment_dictionary_v3.csv', index = False)
