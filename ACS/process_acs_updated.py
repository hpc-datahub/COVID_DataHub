# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 09:39:18 2022

Process ACS data

@author: xywu
"""

# updated on 2023-02-22, Yifeng Wan
# for Year 2018, 2019, 2020, 2021
# py3.10.8, pandas==1.5.3

import pandas as pd
import re
import os


#============
# initialize
#============

# specify working directory
# workdir = './'

# state/county name and fips codes, see ChangeLog.txt
fips = pd.read_csv(os.path.join(os.path.dirname(__file__), 'FIPS/state_county_fips_updated.csv'))
fips.rename(columns = {'fips': 'scfips'}, inplace = True)

print(fips.shape)

# alternative for fips code: latest FIPS from Census Bureau
# fips = pd.read_excel(workdir + 'all_geocodes_v2020.xlsx', skiprows = [0, 1, 2, 3])

# existing prepandemic data
# pre_data = pd.read_csv('')


#==============
# poverty data
#==============

## initiate with empty dictionary
pov_lst = {}

# pre_fips_change_years, 2018 and 2019
for yr in [2018, 2019, 2020, 2021]:
    pov = pd.read_csv(os.path.join(os.path.dirname(__file__), 'acs_poverty_5year_est_s1701/ACSST5Y' + str(yr) + '.S1701-Data.csv'), skiprows = [0], low_memory = False)
    pov[['ctyname', 'stname']] = pov['Geographic Area Name'].str.split(',', expand = True)
    pov['stname'] = pov['stname'].str.strip()
    pov['ctyname'] = pov['ctyname'].str.strip()
    # select variables
    idvar = ['stname', 'ctyname']
    tvar = ['Estimate!!Percent below poverty level!!Population for whom poverty status is determined',
            'Estimate!!Percent below poverty level!!Population for whom poverty status is determined!!AGE!!65 years and over']
    pov = pov[idvar + tvar].copy()
    pov.rename(columns = {tvar[0]: 'povprop_' + str(yr),
                          tvar[1]: 'oldprop_' + str(yr)}, inplace = True)
    # add to dictionary
    pov_lst[str(yr)] = pov

# merge data from different waves
# fips + 2018
pov = pd.merge(left = fips, right = pov_lst['2018'], how = 'outer', \
               on = ['stname', 'ctyname'])
print(pov.shape, pov.columns)
# fips + 2018 + 2019
pov = pd.merge(left = pov, right = pov_lst['2019'], how = 'outer', \
               on = ['stname', 'ctyname'])
print(pov.shape, pov.columns)
# fips + 2018 + 2019 + 2020
pov = pd.merge(left = pov, right = pov_lst['2020'], how = 'outer', \
               on = ['stname', 'ctyname'])
print(pov.shape, pov.columns)
# fips + 2018 + 2019 + 2020 + 2021
pov = pd.merge(left = pov, right = pov_lst['2021'], how = 'outer', \
               on = ['stname', 'ctyname'])
print(pov.shape, pov.columns)

# print(pov.loc[pov['stname']=='Alaska', 'scfips'].unique())
# print(pov.loc[pov['stname']=='Alaska', 'ctyname'].unique())
# print(pov.loc[pov['ctyname']=='Valdez-Cordova Census Area'])
# print(pov.loc[pov['ctyname']=='Chugach Census Area'])
# print(pov.loc[pov['ctyname']=='Copper River Census Area'])

# output to check
pov.to_csv(os.path.join(os.path.dirname(__file__), 'pov18to21_updated.csv'), index = False)


#=============
# income data
#=============

## initiate with empty dictionary
inc_lst = {}

# iterate through waves
for yr in [2018, 2019, 2020, 2021]:
    # read data
    inc = pd.read_csv(os.path.join(os.path.dirname(__file__), 'acs_income_5year_est_s1901/ACSST5Y' + str(yr) + '.S1901-Data.csv'), skiprows = [0], low_memory=False)
    # split county-state column into separate columns
    inc[['ctyname', 'stname']] = inc['Geographic Area Name'].str.split(',', expand = True)
    inc['stname'] = inc['stname'].str.strip()
    inc['ctyname'] = inc['ctyname'].str.strip()
    # select variables
    idvar = ['stname', 'ctyname']
    tvar = [#'Estimate!!Households!!Total',\
            'Estimate!!Households!!Total!!Less than $10,000',\
            'Estimate!!Households!!Total!!$10,000 to $14,999',\
            'Estimate!!Households!!Total!!$15,000 to $24,999',\
            'Estimate!!Households!!Total!!$25,000 to $34,999',\
            'Estimate!!Households!!Total!!$35,000 to $49,999',\
            'Estimate!!Households!!Total!!$50,000 to $74,999',\
            'Estimate!!Households!!Total!!$75,000 to $99,999',\
            'Estimate!!Households!!Total!!$100,000 to $149,999',\
            'Estimate!!Households!!Total!!$150,000 to $199,999',\
            'Estimate!!Households!!Total!!$200,000 or more']
    inc = inc[idvar + tvar].copy()
    inc.columns = [re.sub(r'Estimate!!Households!!Total!!', '', x) \
                   for x in list(inc.columns)]
    tvar = [re.sub(r'Estimate!!Households!!Total!!', '', x) for x in tvar]
    # print(inc.shape)
    # check one row
    # print(inc.loc[25, :])
    # check whethe proportions add up to 1: yes, just some rounding errors, good to proceed
    # 1816  New Mexico  Rio Arriba County, missing data row
    # print(set(inc.iloc[:, 2:].sum(axis = 1)))
    # replace income values with group sequence in column names
    inc.columns = idvar + ['hincgroup' + str(x) + '_' + str(yr) for x in range(1, len(tvar) + 1)]
    # append to list
    inc_lst[str(yr)] = inc


## merge data from different waves
# fips + 2018
inc = pd.merge(left = fips, right = inc_lst['2018'], how = 'outer', \
               on = ['stname', 'ctyname'])
print(inc.shape, inc.columns)
# fips + 2018 + 2019
inc = pd.merge(left = inc, right = inc_lst['2019'], how = 'outer', \
               on = ['stname', 'ctyname'])
print(inc.shape, inc.columns)
# fips + 2018 + 2019 + 2020
inc = pd.merge(left = inc, right = inc_lst['2020'], how = 'outer', \
               on = ['stname', 'ctyname'])
print(inc.shape, inc.columns)
# fips + 2018 + 2019 + 2020 + 2021
inc = pd.merge(left = inc, right = inc_lst['2021'], how = 'outer', \
               on = ['stname', 'ctyname'])
print(inc.shape, inc.columns)

# output to check
inc.to_csv(os.path.join(os.path.dirname(__file__), 'inc18to21_updated.csv'), index = False)

#=======================================
# archived code for ArcGIS alternatives
#=======================================

# # read data
# dt = pd.read_csv(workdir + 'Population_and_Poverty_Status_2015-2019/COUNTIES_2.csv')

# # select variables
# list(dt.columns)
# # tentatively leave out the state/county names, only use FIPS code to merge ('NAME', 'GEO_PARENT_NAME')
# idvar = ['STATEFP', 'COUNTYFP', 'GEOID']
# tvar = [#'POP_DENSITY', \
#         'Percentage of people whose income in the past 12 months is below the poverty level - 65 years and over',\
#         'Percentage of people whose income in the past 12 months is below the poverty level']
# dt = dt[idvar + tvar]
# # rename columns
# dt.rename(columns = {'STATEFP': 'stfips', 'COUNTYFP': 'ctyfips', 'GEOID':'scfips', \
#                      #'POP_DENSITY': 'pop_density_2019',\
#                      'Percentage of people whose income in the past 12 months is below the poverty level - 65 years and over': 'oldprop_2019', \
#                      'Percentage of people whose income in the past 12 months is below the poverty level': 'povprop_2019'},
#           inplace = True)

# # read previous pre-pandemic data
# pre_data = pd.read_csv(workdir + 'Prepandemic/prepandemic_v3.csv')

# # rename previous poverty variables
# pre_data.rename(columns = {'oldprop': 'oldprop_2018', 'povprop': 'povprop_2018'},
#                 inplace = True)

# # merge poverty variables
# pre_data = pd.concat([pre_data, dt], keys = ['stfips', 'ctyfips', 'scfips'])
# pre_data.columns
