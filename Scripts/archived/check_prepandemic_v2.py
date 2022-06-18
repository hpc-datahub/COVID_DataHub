#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:51:46 2022
Latest update on Sat Jun 18 17:01 2022

@author: Xingyun Wu
"""

import pandas as pd
import re


############################
# Previous Prepandemic Data
############################

## read data
df00 = pd.read_csv('~/OneDrive - Johns Hopkins/HPC_own/HPC_datahub/prepandemic/Prepandemic_v2/Prepandemic_v2.csv')
df01 = pd.read_csv('~/OneDrive - Johns Hopkins/HPC_own/HPC_datahub/prepandemic/Prepandemic_v2/ACS.csv')
df02 = pd.read_csv('~/OneDrive - Johns Hopkins/HPC_own/HPC_datahub/prepandemic/Prepandemic_v2/water.csv')

# clean prepandemic_v2.csv
df00.columns
list(df00['Unnamed: 0']) == (df00.index.tolist()) # true, drop the index column
df00.drop(labels = 'Unnamed: 0', axis = 1, inplace = True)
df00
# clean ACS.csv
df01
df01.sort_values(by = 'FIPS', axis = 0, inplace = True)
df01.reset_index(drop = True, inplace = True)
df01
# clean water.csv
df02
df02.sort_values(by = 'FIPS', axis = 0, inplace = True)
df02.reset_index(drop = True, inplace = True)
df02

# read & clean dictionary
dict0 = pd.read_excel('~/OneDrive - Johns Hopkins/HPC_own/HPC_datahub/prepandemic/Prepandemic_v2/Prepandemic_Dictionary_v2.xlsx')
dict0.rename(columns = {'variable name': 'variable_name',\
                       'variable label': 'label',\
                       'column position': 'column',\
                       'documentation name': 'documentation'}, inplace = True)
dict0.columns 
# ['variable_name', 'label', 'column', 'source', 'documentation', 
# 'Unnamed: 5', 'Unnamed: 6']
list(dict0['Unnamed: 5']) 
# seems to be tentative column numbers at the bottom several rows, to be removed
list(dict0['Unnamed: 6']) # similar situation, to be removed
dict0.drop(labels = ['Unnamed: 5', 'Unnamed: 6'], axis = 1, inplace = True)
    

#############
# Comparison
#############

## check if df00 and df01 overlapped
l0 = [x for x in list(df00.columns) if x in list(df01.columns)]
l0 # ['FIPS', 'stname', 'stfips', 'ctyfips']
# Therefore, no real overlap 

## check if df00 and df02 overlapped
l1 = [x for x in list(df00.columns) if x in list(df02.columns)]
l1 # ['FIPS', 'stname', 'stfips', 'ctyfips']
# Therefore, no real overlap, variables should be added to prepandemic data file

## check how the data variables overlapped with the dictionary
## df00: prepandemic_v2.csv
l2 = [x for x in list(df00.columns) if x in list(dict0['variable_name'])]
l2 == list(df00.columns)
# false ==> check difference
l2 = [x for x in list(df00.columns) if x not in list(dict0['variable_name'])]
l2 # ['FIPS', 'ctyname_x']
## df01: ACS.csv
l3 = [x for x in list(df01.columns) if x in list(dict0['variable_name'])]
l3 == list(df01.columns)
# false ==> check difference
l3 = [x for x in list(df01.columns) if x not in list(dict0['variable_name'])]
l3 # ['FIPS', 'GEO_ID', 'NAME', 'S2501_C01_001E', 'S2501_C01_001M']
## df02: water.csv
l4 = [x for x in list(df02.columns) if x in list(dict0['variable_name'])]
l4 == list(df02.columns)
# false ==> check difference
l4 = [x for x in list(df02.columns) if x not in list(dict0['variable_name'])]
l4 # ['FIPS']

## check if df01 and df02 overlapped
# overlap
l5 = [x for x in list(df01.columns) if x in list(df02.columns)]
l5 # real overlap
'''
['FIPS', 'stname', 'ctyname', 'stfips', 'ctyfips', 'Drinking_Water_Violations',
 'Drinking_Water_Violations_Z-Score', 'PS-GWPop_x', 'PS-SWPop_x', 'PS-TOPop_x',
 'PS-WGWTo', 'PS-WFrTo', 'PS-Wtotl_x', 'DO-SSPop_x', 'DO-WFrTo_x', 'DO-PSDel_x',
 'DO-PSPCp_x', 'DO-WDelv _x']
'''
# difference
l6 = [x for x in list(df01.columns) if x not in list(df02.columns)]
l6 # ['GEO_ID', 'NAME', 'S2501_C01_001E', 'S2501_C01_001M']
l7 = [x for x in list(df02.columns) if x not in list(df01.columns)]
l7 # [] ==> all variables of df02 (Water.csv) are in df01 (ACS.csv)
# check whether values on the overlapped variables are identical
df03 = df02[df02['FIPS'].isin(df01['FIPS'])]
df03.reset_index(drop = True, inplace = True)
df04 = df01.drop(labels = l6, axis = 1)
df04.reset_index(drop = True, inplace = True)
df03.equals(df04) # false
# check difference
pd.concat([df03,df04]).drop_duplicates(keep=False) #empty
# suspect the self-contradictory results of difference checking is due to variable format
df04['DO-PSPCp_x'] = df04['DO-PSPCp_x'].astype('float64')
df03.equals(df04) # true
'''
conclusion:
1. df01 (ACS.csv) has all variables of df02 (water.csv), while having two extra variables
2. df01 (ACS.csv) donesn't have all counties, while df02 (water.csv) has
solution:
  (1) Check what the two extra variables in df01 are
          No clue. Not exist in prepandemic dictionary.
          In prepandemic dictionary, the only two variables from ACS.csv 
          are Drinking_Water_Violations and Drinking_Water_Violations_Z-Score,
          which also exist in water.csv and included in prepandemic dictionary too.
  (2) If the two variables are important, add to df01
          No need. Must not be important since not even in dictionary.
'''
# check whether the two collected ACS.csv variables are identicle to those in water.csv
df03.Drinking_Water_Violations.equals(df04.Drinking_Water_Violations)
# true
df03['Drinking_Water_Violations_Z-Score'].equals(df04['Drinking_Water_Violations_Z-Score'])
# true
# ACS.csv redundant and has less observations. 
# Use water.csv only for the same variables.

## check if all variables in water.csv are in prepandemic dictionary
l8 = [x for x in list(df02.columns) if x in list(dict0.variable_name)]
l8
l9 = [x for x in list(df02.columns) if x not in list(dict0.variable_name)]
l9 # ['FIPS']
# Basically all variable in water.csv are in prepandemic dictionary

## check if variables in prepandemic dictionary but not in the 3 data files
l10 = [x for x in list(dict0.variable_name) if x not in list(df00.columns)\
       if x not in list(df01.columns) if x not in list(df02.columns)]
l10 # ['fips']
# Need to standardize the fips variable name to lower case in data


##########
# Fix Bug
##########

## rename fips column 
# rename in df02 (water.csv)
df02.rename(columns = {'FIPS': 'scfips'}, inplace = True)
# rename in df00 (prepandemic_v2.csv)
df00.rename(columns = {'FIPS': 'scfips'}, inplace = True)
# rename in dict0 to standardize with pandemic data
dict0.index[dict0['variable_name'] == 'fips'].tolist() # [4]
dict0.loc[4, 'variable_name'] = 'scfips'

## merge df02 (water.csv) into df00 (prepandemic_v2.csv) on fips variables
# check existing fips variables in both data first
df00.columns[:10]
df00.rename(columns = {'ctyname_x': 'ctyname'}, inplace = True)
# save df00 data to prepandemic_v3.csv, df02 data to cached water_v3.csv
df00.to_csv('~/Documents/GitHub/COVID_DataHub/Prepandemic/prepandemic_v3.csv',\
            index = False)
df02.to_csv('~/OneDrive - Johns Hopkins/HPC_own/HPC_datahub/prepandemic/water_v3.csv',\
            index = False)

# df02.columns[:10]
# colKeys = list(df00.columns[:5])
# colKeys
# # merge
# df00.shape # (3142, 86)
# df02.shape # (3142, 18)
# fnl = df00.merge(df02, how = 'outer', on = colKeys)
# fnl.shape # (3143, 99) ==> get 1 more row, 86 + 18 - 5 = 99 correct
# # check the added row
# fnl.index[fnl['scfips'] == 35013].tolist() # [1802, 3142]
# fnl.iloc[1802,]
# fnl.iloc[3142,]
# # issue results from error in county name of 35013 in df02 (water.csv), redo merge
# colKeys.remove('ctyname')
# colKeys
# fnl = df00.merge(df02, how = 'outer', on = colKeys)
# fnl.shape # (3142, 100) ==> correct row number, 1 more column due to ctyname
# # remove redundant ctyname
# [x for x in list(fnl.columns) if 'ctyname' in x] # ['ctyname_x', 'ctyname_y']
# fnl.drop(labels = 'ctyname_y', axis = 1, inplace = True)
# fnl.rename(columns = {'ctyname_x': 'ctyname'}, inplace = True)
# fnl.columns
# # output
# fnl.to_csv('~/Documents/GitHub/COVID_DataHub/Prepandemic/prepandemic_v3.csv',\
#            index = False)

## read-in get_dict()
def get_dict(dt, dct):
    '''
    Auxiliary function to get column indices and date range
    Input:
        dt: a Pandas data frame for data
        dct: a Pandas data frame for dictionary to modify
    Output:
        rv: a Pandas data frame for dictionary
    '''
    
    trow = []
    for i in range(dct.shape[0]):
        if dct.loc[i, 'variable_name'] in dt.columns:
            trow.append(i)
    rv = dct.iloc[trow, :].copy()
    rv.reset_index(drop = True, inplace = True)
    
    for i in range(rv.shape[0]):
        print(i)
        # # added code on 6/18/2022 to ignore variables not in data
        # if rv.loc[i, 'variable_name'] not in list(dt.columns):
        #     print('Variable from dictionary not in data')
        #     toRm.append(toRm)
        #     continue
        # # proceed if variable from dictionary in data
        temp = re.findall('_yyyymm.*', rv.loc[i, 'variable_name'])
        if len(temp) > 0:
            tvar = '^' + re.sub('_yyyymm.*', '', rv.loc[i, 'variable_name']) + '_20'
            # tid = [i for i, s in enumerate(dt.columns) if tvar in s]
            tid = []
            tcol = list(dt.columns)
            for j in range(dt.shape[1]):
                if(bool(re.search(tvar, tcol[j]))):
                    tid.append(j)
        else:
            tvar = rv.loc[i, 'variable_name']
            tid = [dt.columns.get_loc(tvar)]
        
        # multiple items for this item
        if len(tid) > 1:
            print('Multiple columns for this item...')
            # get date range
            tdate = [re.findall('20[\d]+', x)[0] for x in dt.columns[tid]]
            # modify column indices and date range
            rv.loc[i, 'start_column'] = tid[0] + 1
            rv.loc[i, 'end_column'] = tid[-1] + 1
            rv.loc[i, 'start_date'] = tdate[0]
            rv.loc[i, 'end_date'] = tdate[-1]
        # single column for this item
        else:
            print('Single column for this item...')
            rv.loc[i, 'start_date'] = -1
            rv.loc[i, 'end_date'] = -1
            if len(tid) == 1:
                rv.loc[i, 'start_column'] = tid[0] + 1
                rv.loc[i, 'end_column'] = tid[0] + 1
            else:
                rv.loc[i, 'start_column'] = -1
                rv.loc[i, 'end_column'] = -1
  
    # sort rows by 'start_column'
    rv.sort_values(by = 'start_column', ascending = True, inplace = True)
    rv.reset_index(drop = True, inplace = True)
    
    return rv
    

## correct column numbers in prepandemic_dictionary_v2.csv
fdct = get_dict(df00, dict0)
# inspect
fdct
fdct.columns # redundant columns for column indices exist

# ## drop redundant variables due to overlapping ACS.csv and water.csv
# # locate and drop redundant overlapping variable 1 in df01 (ACS.csv) and df02 (water.csv)
# fdct.index[fdct['variable_name'] == 'Drinking_Water_Violations'].tolist() # [86, 87]
# fdct.loc[86:87, ['variable_name', 'documentation']]
# fdct.drop(axis = 0, index = 86, inplace = True)
# fdct.index[fdct['variable_name'] == 'Drinking_Water_Violations'].tolist() # [87]
# # locate and drop redundant overlapping variable 2 in df01 (ACS.csv) and df02 (water.csv)
# fdct.index[fdct['variable_name'] == 'Drinking_Water_Violations_Z-Score'].tolist() # [88, 89]
# fdct.loc[88:89, ['variable_name', 'documentation']]
# fdct.drop(axis = 0, index = 88, inplace = True)
# fdct.index[fdct['variable_name'] == 'Drinking_Water_Violations_Z-Score'].tolist() # [89]
# # reset index
# fdct.reset_index(drop = True, inplace = True)
# fdct.shape # (99, 9)

## keep useful column index variable only
fdct.start_column.equals(fdct.end_column) # True, only need one
fdct.drop(labels = ['column', 'end_column'], axis = 1, inplace = True)
fdct.rename(columns = {'start_column': 'column'}, inplace = True)
# drop dates as well because variables are time invariant
fdct.drop(labels = ['start_date', 'end_date'], axis = 1, inplace = True)
# rename 'documentation' column as 'original_document' so that not confusing
fdct.rename(columns = {'documentation': 'original_document'}, inplace = True)

## output
fdct.to_csv('~/Documents/GitHub/COVID_DataHub/Prepandemic/prepandemic_dictionary_v3.csv',\
           index = False)
# upload the corrected file to GitHub first, improve variable labels later

