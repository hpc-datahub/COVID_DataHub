#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 23:07:07 2021

@author: Xingyun Wu
"""

import pandas as pd


# get FIPS and state names
fips = pd.read_csv('~/Documents/GitHub/COVID_DataHub/FIPS/state_territory_fips.csv')


# read data
df = pd.read_excel('~/Documents/ra/HPC_datahub/APM/ColorOfCoronavirus/APM/ColorOfCoronavirus_Data_File_ThroughMarch2_2021_TS_APMResearchLab_Revised-April16-2021.xlsx',\
                   sheet_name = 'B_DeathsReported_Trend')
df.columns = [x.strip() for x in df.columns]
    
# format the datetime column
df['Date'] = df['Date'].dt.strftime('%Y%m%d')

# reshape from long to wide
df = df.pivot(index = 'State', columns = 'Date')
df.reset_index(inplace = True)

# sort columns by date (originally by variable after reshape)
df.sort_index(axis = 1, level = 'Date', inplace = True)

# concate variable names with dates
df.columns = [(x[0] + '_' + x[1]).strip('_') for x in df.columns]

# merge fips and data
df.rename(columns = {'State': 'stname'}, inplace = True)
df = fips.merge(df, on = 'stname', how = 'right')

# output
df.to_csv('~/Documents/GitHub/COVID_DataHub/Pandemic/ApmColorOfCoronavirus.csv')
