# -*- coding: utf-8 -*-
"""
Python script to streamline HPC COVID-19 Data Hub
Part 1: state-level data

Author: Xingyun Wu

Initial date: 12/6/2021
Previous update: 1/31/2022 (merge data)
Latest update: 3/2/2022 (major) --> 3/9/2022 (final)
"""

import pandas as pd
import re


###########
# Initiate
###########

# the path of HPC data hub GitHub data files
filedir1 = '/Users/xywu/Documents/GitHub/COVID_DataHub/Pandemic/'
# the path of HPC summer 2021 data files
filedir2 = '/Users/xywu/Documents/ra/HPC/HPC_datahub_summer2021/script_result/'
# the path of release 5 files
filedir3 = '/Users/xywu/Documents/ra/HPC/HPC_datahub/release5/'
# the path of updated HPC summer 2021 data files
filedir4 = '/Users/xywu/Documents/ra/HPC/HPC_datahub/release5/update_data/'



##################
# Data Processing
##################

#==============
# Step 1: data
#==============
## read-in the existing data

# cases & deaths
cdcDeaths = pd.read_csv(filedir4 + 'Deaths_by_State.csv') # updated
apmCases = pd.read_csv(filedir1 + 'ApmColorOfCoronavirus.csv')
# medical
medicalCovidtracking = pd.read_csv(filedir1 + 'medical_covidtracking.csv',
                                   low_memory = False)
# policy
cdcPolicy = pd.read_csv(filedir2 + 'State_Policy.csv') # don't update due to change of raw data
existPolicy = pd.read_csv(filedir1 + 'policy.csv')
# vaccination
cdcVac = pd.read_csv(filedir4 + 'Age_of_Vaccination.csv') # updated
apmVac = pd.read_csv(filedir2 + 'Color_of_Vaccination.csv')


#===============================================
# Step 2: get the dataframes ready to be merged
#===============================================
## merge the state-level data together

# cdcDeaths
# merge the New York and New York City rows
cdcDeaths[cdcDeaths['stname'] == 'New York City'] # row id == 33
cdcDeaths.iloc[33, 0] = 'New York'
cdcDeaths[cdcDeaths['stname'] == 'New York']
cdcDeaths = cdcDeaths.groupby(cdcDeaths.stname, as_index = False).sum()
# remove Puerto Rico from cdcDeaths
cdcDeaths[cdcDeaths['stname'] == 'Puerto Rico'] # row id == 39
cdcDeaths.drop(39, axis = 0, inplace = True)
# add prefix to the data
cdcDeaths.columns = ['stname'] + ['cdc_' + x for x in cdcDeaths.columns[1:]]

# apmCases
# drop the 'all states' row
apmCases[apmCases['stname'] == 'ALL STATES'] # row id == 0
apmCases.drop(0, axis = 0, inplace = True)
# add prefix
apmCases.columns = list(apmCases.columns[:3]) +\
    ['apm_cases_' + x for x in apmCases.columns[3:]]

# medical_covidtracking
medicalCovidtracking = medicalCovidtracking[['stname', 'stabbr', 'stfips'] + \
                                            list(medicalCovidtracking.columns[3:])]
# drop the US territories rows
medicalCovidtracking.drop([51, 52, 53, 54, 55], inplace = True)
# add prefix
medicalCovidtracking.columns = list(medicalCovidtracking.columns[:3]) +\
    ['medical_covidtracking_' + x for x in medicalCovidtracking.columns[3:]]

# cdc policy
# drop Puerto Rico from the data
cdcPolicy[cdcPolicy['stname'] == 'Puerto Rico'] # row id == 39
cdcPolicy.drop(39, axis = 0, inplace = True)
# add prefix
cdcPolicy.columns = ['stname', 'stfips'] + ['cdc_policy_' + x for x in cdcPolicy.columns[2:]]

# existing policy data on GitHub
# add prefix
existPolicy.columns = list(existPolicy.columns[:3]) + \
    ['policy_' + x for x in existPolicy.columns[3:]]

# cdc vaccination
cdcVac.rename(columns = {'location': 'stabbr'}, inplace = True)
# add prefix
cdcVac.columns = list(cdcVac.columns[:3]) + \
    ['cdc_vac_' + x for x in cdcVac.columns[3:]]

# apm vaccination
apmVac.rename(columns = {'location': 'stabbr'}, inplace = True)
# add sign for population varialbes and remove the 'v' in column names
apmVac.rename(columns = {'all': 'all_population', 'black': 'black_population',\
                         'white': 'white_population', 'asian': 'asian_population',\
                         'latino': 'latino_population', 'indig': 'indig_population',\
                         'other': 'other_population'}, inplace = True)
apmVac.columns = list(apmVac.columns)[:10] + [re.sub('v', '', x) for x in list(apmVac.columns)[10:]]
# add prefix
apmVac.columns = list(apmVac.columns[:3]) + \
    ['apm_vac_' + x for x in apmVac.columns[3:]]


#====================
# Step 3: dictionary
#====================

# load existing pandemic dictionary
pandemicDict = pd.read_csv(filedir1 + 'pandemic_dictionary.csv')

# ApmColorOfCoronavirus (existing)
apmCasesDict = pandemicDict[pandemicDict['file'] == 'ApmColorOfCoronavirus.csv'].copy()
apmCasesDict.reset_index(drop = True, inplace = True)
# check state-id variables
apmCasesDict['variable name']
# store state-id variables before removing for full dictionary
dct = apmCasesDict.iloc[:3, :]
dct = dct.assign(source = ['https://www2.census.gov/geo/docs/reference/state.txt'] * 3)
dct = dct.assign(file = '')
# remove state-id variables
apmCasesDict.drop(axis = 0, index = [0, 1, 2], inplace = True)
# add prefix
apmCasesDict.loc[:, 'variable name'] = ['apm_cases_' + x for x in list(apmCasesDict['variable name'])]

# medical_covidtracking (existing)
# variables in existing pandemic dictionary
medicalCovidtrackingDict = pandemicDict[pandemicDict['file'] == 'medical_covidtracking.csv'].copy()
# variable names in medical_covidtracking data
mcTmp = list(medicalCovidtracking.columns)
mcTmp = [re.sub('_20\d{6}', '', x) for x in mcTmp[3:]]
mcLst = list(set(mcTmp))
mcLst = [x + '_yyyymmdd' for x in mcLst]
mcDict = pd.DataFrame(mcLst, columns = ['variable name'])
mcDict['vn_original'] = [re.sub('medical_covidtracking_', '', x) for x in list(mcDict['variable name'])]
# merge the updated variable names to existing variables in pandemic dictionary
mcDict = pd.merge(left = mcDict, right = medicalCovidtrackingDict, how = 'right',\
                  left_on = 'vn_original', right_on = 'variable name')
# keep the selected variables only in dictionary
mcDict.drop(columns = ['vn_original', 'variable name_y'], inplace = True)
mcDict.rename(columns = {'variable name_x': 'variable name'}, inplace = True)
mcDict.sort_values('start column', inplace = True)

# existing policy data (existing)
policyDict = pandemicDict[pandemicDict['file'] == 'policy.csv'].copy()
policyDict.reset_index(drop = True, inplace = True)
# drop the state-id variables
policyDict['variable name']
policyDict.drop(axis = 0, index = [0, 1], inplace = True)
# add prefix
policyDict.loc[:, 'variable name'] = ['policy_' + x for x in list(policyDict['variable name'])]

# cases by group (new)
cdcDeathsDict = pd.read_excel(filedir2 + 'Deaths_by_State_Dictionary.xlsx')
# drop the state-id variables
cdcDeathsDict['variable name']
cdcDeathsDict.drop(axis = 0, index = 0, inplace = True)
# fix inconsistence between column names in data and column names in dictionary
cdcDeathsDict.loc[:, 'variable name'] = [re.sub('_yymm', '_yyyymm', x) for x in list(cdcDeathsDict['variable name'])]
# add prefix
cdcDeathsDict.loc[:, 'variable name'] = ['cdc_' + x for x in list(cdcDeathsDict['variable name'])]

# cdc policy (new)
cdcPolicyDict = pd.read_excel(filedir2 + 'State_Policy_Dictionary.xlsx')
# drop the state-id variables
cdcPolicyDict['variable name']
cdcPolicyDict.drop(axis = 0, index = [0, 1], inplace = True)
# add prefix
cdcPolicyDict['variable name'] = ['cdc_policy_' + x for x in list(cdcPolicyDict['variable name'])]

# cdc vaccination (new)
cdcVacDict = pd.read_excel(filedir2 + 'Age_of_Vaccination_Dictionary.xlsx')
# drop state-id variables
cdcVacDict['variable name'] # 'location' is actually 'stabbr'
cdcVacDict.drop(axis = 0, index = [0, 1, 2], inplace = True)
# add prefix
cdcVacDict['variable name'] = ['cdc_vac_' + x for x in list(cdcVacDict['variable name'])]

# apm vaccination (new)
apmVacDict = pd.read_excel(filedir2 + 'Color_of_Vaccination_Dictionary.xlsx')
# drop state-id variables
apmVacDict['variable name']
apmVacDict.drop(axis = 0, index = [0, 1, 2], inplace = True)
# modify variable names according to edits to apmVac
apmVacDict.loc[:, 'variable name'] = [x + '_population' for x in list(apmVacDict['variable name'])[:7]] +\
    [re.sub('v', '', x) for x in list(apmVacDict['variable name'])[7:]]
# add prefix
apmVacDict['variable name'] = ['apm_vac_' + x for x in list(apmVacDict['variable name'])]


#=========================================
# Step 4: merge the seperate data objects
#=========================================
# by stname, stfips, and stabbr

# define keys for merging
colKeys = ['stname', 'stabbr', 'stfips']

## Tentatively take out CDC provisional deaths data because of needs to further inspect its raw data
# # 1. start from cdcDeaths data
# cdcDeaths.columns
# # take-out state-id variable(s) for coherence check
# l0 = list(cdcDeaths.columns)[1:]
# l0 = [re.sub('_20\d{4}', '', x) for x in l0]
# l0 = set(l0)
# l1 = list(cdcDeathsDict['variable name'])
# l1 = [re.sub('_yyyymm', '', x) for x in l1]
# l1 = set(l1)
# # check coherence of data and dictionary
# l0 == l1 # True, good to proceed
# # hard-copy to df and dct
# df = cdcDeaths.copy()
# dct = pd.concat([dct, cdcDeathsDict], join = 'outer', copy = True)
# # check dimension
# print('Dimension of df = {} * {}, dimension of dictionary = {} * {}'.\
#       format(df.shape[0], df.shape[1], dct.shape[0], dct.shape[1]))

# 2. merge apmCases
apmCases.columns
l0 = list(apmCases.columns)[3:]
l0 = [re.sub('_20\d{6}', '', x) for x in l0]
l0 = set(l0)
l1 = list(apmCasesDict['variable name'])
l1 = [re.sub('_yyyymmdd', '', x) for x in l1]
l1 = set(l1)
# check consistency
l0 == l1 # true
# merge data and append dictionary
# df = df.merge(apmCases, on = 'stname', how = 'outer')
df = apmCases.copy()
dct = pd.concat([dct, apmCasesDict], join = 'outer', copy = True)
# check dimension
print('Dimension of df = {} * {}, dimension of dictionary = {} * {}'.\
      format(df.shape[0], df.shape[1], dct.shape[0], dct.shape[1]))

# 3. merge medical_covidtracking
medicalCovidtracking.columns
l0 = list(medicalCovidtracking.columns)[3:]
l0 = set([re.sub('_20\d{6}', '', x) for x in l0])
l1 = list(mcDict['variable name'])
l1 = set([re.sub('_yyyymmdd', '', x) for x in l1])
# check consistency
l0 == l1 # false
print('Length of l0 = {}, length of l1 = {}'.format(len(l0), len(l1)))
# not consistent, keep the selected variables in dictionary only
l1 = [x + '_20' for x in list(l1)]
lid = [0, 1, 2]
for i in range(len(l1)):
    tvar = l1[i]
    tid = [i for i, s in enumerate(medicalCovidtracking.columns) if tvar in s]
    lid += tid
print('{} out of {} variables to be kept'.format(len(set(lid)), medicalCovidtracking.shape[1]))
lid = sorted(list(set(lid)))
medicalCovidtracking = medicalCovidtracking.iloc[:, lid]
# merge data and append dictionary
df = df.merge(medicalCovidtracking, on = colKeys, how = 'outer')
dct = pd.concat([dct, mcDict], join = 'outer', copy = True)
# check dimension
print('Dimension of df = {} * {}, dimension of dictionary = {} * {}'.\
      format(df.shape[0], df.shape[1], dct.shape[0], dct.shape[1]))

# 4. merge cdc policy
cdcPolicy.columns 
l0 = list(cdcPolicy.columns)[2:]
l1 = list(cdcPolicyDict['variable name'])
l0 == l1
# merge data and append dictionary
df = df.merge(cdcPolicy, on = ['stname', 'stfips'], how = 'outer')
dct = pd.concat([dct, cdcPolicyDict], join = 'outer', copy = True)
# check dimension
print('Dimension of df = {} * {}, dimension of dictionary = {} * {}'.\
      format(df.shape[0], df.shape[1], dct.shape[0], dct.shape[1]))

# 5. merge existing policy data on GitHub
existPolicy.columns
l0 = list(existPolicy.columns)[3:]
l1 = list(policyDict['variable name'])
l0 == l1 # false
print('Length of l0 = {}, length of l1 = {}'.format(len(l0), len(l1)))
# select variables in dictionary only
existPolicy = existPolicy[list(existPolicy.columns)[:3] + l1]
# merge data and append dictionary
df = df.merge(existPolicy, on = colKeys, how = 'outer')
dct = pd.concat([dct, policyDict], join = 'outer', copy = True)
# check dimension
print('Dimension of df = {} * {}, dimension of dictionary = {} * {}'.\
      format(df.shape[0], df.shape[1], dct.shape[0], dct.shape[1]))

# 6. merge cdc vaccination
cdcVac.columns
l0 = list(cdcVac.columns)[3:]
l0 = set([re.sub('_20\d{6}', '', x) for x in l0])
l1 = list(cdcVacDict['variable name'])
l1 =  set([re.sub('_yyyymmdd', '', x) for x in l1])
l0 == l1 # true
# merge
df = df.merge(cdcVac, on = colKeys, how = 'outer')
dct = pd.concat([dct, cdcVacDict], join = 'outer', copy = True)
# check dimension
print('Dimension of df = {} * {}, dimension of dictionary = {} * {}'.\
      format(df.shape[0], df.shape[1], dct.shape[0], dct.shape[1]))

# 7. merge apm vaccination
apmVac.columns
l0 = list(apmVac.columns)[3:]
l0 = set([re.sub('20\d{6}', '', x) for x in l0])
l1 = list(apmVacDict['variable name'])
l1 = set([re.sub('yyyymmdd', '', x) for x in l1])
l0 == l1 # true
# merge
df = df.merge(apmVac, on = colKeys, how = 'outer')
dct = pd.concat([dct, apmVacDict], join = 'outer', copy = True)
# check dimension
print('Dimension of df = {} * {}, dimension of dictionary = {} * {}'.\
      format(df.shape[0], df.shape[1], dct.shape[0], dct.shape[1]))

# check whether redundant keys
lid = []
for i in range(len(colKeys)):
    tvar = colKeys[i]
    tid = [i for i, s in enumerate(df.columns) if tvar in s]
    lid.append(tid)
print(lid)
# no redundant keys, proceed
# reorder the 'stfips' and 'stabbr' columns to the front
cols = colKeys + [x for x in df.columns if x not in colKeys]
df = df.reindex(columns = cols)
print(df.shape)

# to column names, replace space with underscore
dct.rename(columns = {'variable name': 'variable_name', 'start column': 'start_column',\
                      'end column': 'end_column', 'start date': 'start_date',\
                      'end date': 'end_date'}, inplace = True)
dct.columns
# reset dct index
dct.reset_index(drop = True, inplace = True)

# output first
df.to_csv(filedir3 + 'state_level_data.csv', index = False)
dct.to_csv(filedir3 + 'state_level_dictionary_raw.csv', index = False)

# remove objects from environment to save memory
del [df, dct, apmCases, apmCasesDict, apmVac, apmVacDict, cdcDeaths,\
     cdcDeathsDict, cdcPolicy, cdcPolicyDict, cdcVac, cdcVacDict, colKeys,\
     cols, existPolicy, i, l0, l1, lid, mcDict, mcLst, mcTmp, medicalCovidtracking,\
     medicalCovidtrackingDict, pandemicDict, policyDict, tid, tvar]


#============================
# Step 6: get column indices
#============================

## auxiliary function to get column indices
def get_dict(dt, dct):
    '''
    Auxiliary function to get column indices and date range
    Input:
        dt: a Pandas data frame for data
        dct: a Pandas data frame for dictionary to modify
    Output:
        rv: a Pandas data frame for dictionary
    '''
    
    rv = dct.copy()
    
    for i in range(rv.shape[0]):
        print(i)
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
    
    # return
    return rv


# read the saved data and dictionary
df = pd.read_csv(filedir3 + 'state_level_data.csv', low_memory = False)
sDict = pd.read_csv(filedir3 + 'state_level_dictionary_raw.csv')

# get column indices
sDict = get_dict(df, sDict)

# record previous files' name in an additional column and replace 'file'
sDict['filename_in_release4'] = sDict['file'].copy()
sDict['filename_in_release4'].replace(to_replace = {'State_Policy.csv': '',\
                                                    'Age_of_Vaccination.csv': '',\
                                                     'Color_of_Vaccination.csv': ''},\
                                      inplace = True)

# adjust the column names for users
sDict.rename(columns = {'file': 'field', 'source': 'link'}, inplace = True)
sDict['field'].fillna(value = 'state identifier', inplace = True)

# source
sDict['source'] = sDict['field'].copy()
sDict['source'].replace(to_replace = {'state identifier': 'Census',\
                                      'Age_of_Vaccination.csv': 'CDC',\
                                      'ApmColorOfCoronavirus.csv': 'APM',\
                                      'Color_of_Vaccination.csv': 'APM',\
                                      'Deaths_by_State.csv': 'CDC',\
                                      'State_Policy.csv': 'CDC',\
                                      'medical_covidtracking.csv': 'Covid Tracking',\
                                      'policy.csv': 'BU'},\
                       inplace = True)
sDict.loc[sDict.link == 'https://github.com/govex/COVID-19/tree/master/data_tables', 'source'] = 'GovEx'
sDict.loc[sDict.link == 'https://www.census.gov/newsroom/press-kits/2020/population-estimates-detailed.html', 'source'] = 'Census'
sDict.loc[sDict.link == 'https://www.census.gov/geographies/reference-files/2018/demo/popest/2018-fips.html', 'source'] = 'Census'

# mark variables' fields
sDict['field'].replace(to_replace = {'Age_of_Vaccination.csv': 'vaccination',\
                                     'ApmColorOfCoronavirus.csv': 'cases and deaths',\
                                     'Color_of_Vaccination.csv': 'vaccination',\
                                     'Deaths_by_State.csv': 'cases and deaths',\
                                     'State_Policy.csv': 'policy',\
                                     'medical_covidtracking.csv': 'medical',\
                                     'policy.csv': 'policy'},\
                       inplace = True)

# reorder columns
sDict = sDict[['variable_name', 'label', 'field', 'source', 'link', \
               'start_column', 'end_column', 'start_date', 'end_date',\
               'filename_in_release4']]

# output
sDict.to_csv(filedir3 + 'state_data_dictionary.csv', index = False)

