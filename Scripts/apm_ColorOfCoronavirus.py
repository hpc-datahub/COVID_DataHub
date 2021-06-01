#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 23:07:07 2021

@author: Xingyun Wu
"""

import pandas as pd
import numpy as np


## read data
# cumulative death count
df1 = pd.read_excel('~/Documents/ra/HPC_datahub/APM/ColorOfCoronavirus/APM/ColorOfCoronavirus_Data_File_ThroughMarch2_2021_TS_APMResearchLab_Revised-April16-2021.xlsx',\
                   sheet_name = 'B_DeathsReported_Trend')
df1.columns = [x.strip() for x in df1.columns]
# population data from pre-pandemic data
df2 = pd.read_csv('~/Documents/GitHub/COVID_DataHub/Prepandemic/Prepandemic_v2.csv')
# FIPS and state names
fips = pd.read_csv('~/Documents/GitHub/COVID_DataHub/FIPS/state_territory_fips.csv')


## process df1 (state-level death counts)
# format the datetime column
df1['Date'] = df1['Date'].dt.strftime('%Y%m%d')
# mark 'N' as na
df1.replace('N', np.nan, inplace = True)
df1.replace('N!', np.nan, inplace = True)
# fill na with 0
df1.fillna(value = 0, inplace = True)
# change data type from float to int
df1.iloc[:, 2:9] = df1.iloc[:, 2:9].astype('int')
# row sum of death counts before dropping unneeded columns
df1['totalDeathBy'] = df1.iloc[:, 2:9].sum(axis = 1)
# drop unneeded columns
df1.drop(labels = ['Indigenous', 'Pacific Islander', 'Other', 'Unknown'], axis = 1, inplace = True)
# re-order columns before reshape
df1 = df1[['State', 'Date', 'totalDeathBy', 'White', 'Black', 'Latino', 'Asian']]
# sort by state and date before reshape
df1.sort_values(by = ['State', 'Date'], axis = 0, ascending = True, inplace = True)
# reshape from long to wide
df1 = df1.pivot(index = 'State', columns = 'Date')
df1.reset_index(inplace = True)
# sort columns by date (originally by variable after reshape)
#df1.sort_index(axis = 1, level = 'Date', inplace = True)
# concate variable names with dates
df1.columns = [(x[0] + '_' + x[1]).strip('_') for x in df1.columns]
df1.rename(columns = {'State': 'stname'}, inplace = True)


## process df2 (county-level population from pre-pandemic data to state-level)
# drop index column
df2.drop(labels = 'Unnamed: 0', axis = 1, inplace = True)
# get population count for each race
df2 = df2[['FIPS', 'stname', 'stfips', 'ctyname_x', 'ctyfips', 'tot_2018',\
           'hispanic_2018', 'nhwhite_2018', 'nhblack_2018', 'nhasian_2018']].copy()
df2['hispanic_cnt'] = round(df2['tot_2018'] * df2['hispanic_2018'], 0).astype('int')
df2['nhwhite_cnt'] = round(df2['tot_2018'] * df2['nhwhite_2018'], 0).astype('int')
df2['nhblack_cnt'] = round(df2['tot_2018'] * df2['nhblack_2018'], 0).astype('int')
df2['nhasian_cnt'] = round(df2['tot_2018'] * df2['nhasian_2018'], 0).astype('int')
# group by state to merge county-level data into state-level
df3 = df2.groupby(by = ['stname', 'stfips']).sum()
# reset index to put the indices back into the data table
df3.reset_index(inplace = True)
# drop redundant columns and clarify/simplify the column names
df3.drop(labels = ['FIPS', 'ctyfips', 'hispanic_2018', 'nhwhite_2018',\
                   'nhblack_2018', 'nhasian_2018'], axis = 1, inplace = True)
df3.columns = ['stname', 'stfips', 'total_2018', 'hispanic_2018',\
               'nhwhite_2018', 'nhblack_2018', 'nhasian_2018']


# merge fips and data
final = fips.merge(df3, on = ['stfips', 'stname'])
final = final.merge(df1, on = 'stname', how = 'right')
list(final.columns)

# output
final.to_csv('~/Documents/GitHub/COVID_DataHub/Pandemic/ApmColorOfCoronavirus.csv')
