#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 22:05:36 2022
Python script to streamline HPC COVID-19 Data Hub
Part 2: county-level data

Author: Xingyun Wu

Initial date: 2/25/2022
Latest update: 3/1/2022 (major) --> 3/9/2022 (final)

@author: wyx
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

# state-county fips
stateFips = pd.read_csv(filedir1 + '../FIPS/state_territory_fips.csv')
fips = pd.read_csv(filedir1 + '../FIPS/state_county_fips.csv')
fips = fips[fips['stfips'] <= 56]
fips.rename(columns = {'fips': 'scfips'}, inplace = True)
fips = stateFips.merge(fips, on = ['stfips', 'stname'], how = 'right')
del stateFips

# existing pandemic dictionary
pDict = pd.read_csv(filedir1 + 'pandemic_dictionary.csv')
pDict.rename(columns = {'variable name': 'variable_name', 'start column': 'start_column',\
                        'end column': 'end_column', 'start date': 'start_date',\
                        'end date': 'end_date'}, inplace = True)

# get dictionary for state & county id variables
idDict = pDict.iloc[:5].copy()
idDict = idDict.append(idDict.iloc[4, :])
idDict.reset_index(drop = True, inplace = True)
idDict.loc[5, 'variable_name'] = 'stabbr'
idDict.loc[5, 'label'] = 'State abbreviation'
# reorder rows
cols = pd.DataFrame(list(fips.columns), columns = ['variable_name'])
idDict = cols.merge(idDict, on = 'variable_name', how = 'outer')
idDict['file'] = ''


#=================================
# Step 2: function for dictionary
#=================================

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
    
    return rv


#======================
# Step 3: process data
#======================

# JHU CSSE cases & deaths
# read data
csse = pd.read_csv(filedir1 + 'casesAndDeaths.csv')
csse = fips.merge(csse, on = ['stfips', 'stname', 'ctyfips', 'ctyname', 'scfips'], how = 'outer')
#csse.to_csv(filedir4 + '../county_casesAndDeaths.csv', index = False)
# dictionary
csseDict = pDict[pDict['file'] == 'casesAndDeaths.csv'].copy()
csseDict.drop(axis = 0, index = [0, 1, 2, 3, 4], inplace = True)
#csseDict = get_dict(csse, csseDict)
    

## CDC deaths by county
# read data
cdCty = pd.read_csv(filedir4 + 'Deaths_by_County.csv')
cdCty.rename(columns = {'stname': 'stabbr', 'ctyfips': 'scfips', 'startdate': 'death_startdate'}, inplace = True)
# merge with fips
cdCty = fips.merge(cdCty, on = ['stabbr', 'ctyname', 'scfips'], how = 'outer')
print('Data got {} rows after merge. Standard number of rows should be {}'.format(cdCty.shape[0], fips.shape[0]))
print(cdCty[cdCty['stfips'].isnull()][['stabbr', 'ctyname']])
# re-read data and correct ctyname errors
cdCty = pd.read_csv(filedir4 + 'Deaths_by_County.csv')
cdCty.rename(columns = {'stname': 'stabbr', 'ctyfips': 'scfips', 'startdate': 'death_startdate'}, inplace = True)
# 1st correction
trow = cdCty.index[(cdCty['stabbr'] == 'AK') & (cdCty['ctyname'] == 'Wade Hampton Census Area')]
print(cdCty.iloc[trow, :].to_string())
cdCty.drop(axis = 0, index = trow, inplace = True)
cdCty.reset_index(drop = True, inplace = True)
# 2nd correction
trow = cdCty.index[(cdCty['stabbr'] == 'IL') & (cdCty['ctyname'] == 'La Salle County')]
print(cdCty.iloc[trow, :].to_string())
cdCty.loc[trow, 'ctyname'] = list(fips[fips['scfips'] == 17099]['ctyname'])[0]
# 3rd correction
trow = cdCty.index[(cdCty['stabbr'] == 'LA') & (cdCty['ctyname'] == 'La Salle Parish')]
print(cdCty.loc[trow, :].to_string())
cdCty.loc[trow, 'ctyname'] = list(fips[fips['scfips'] == 22059]['ctyname'])[0]
# 4th correction
trow = cdCty.index[(cdCty['stabbr'] == 'NM') & (cdCty['ctyname'] == 'Dona Ana County')]
print(cdCty.loc[trow, :].to_string())
cdCty.loc[trow, 'ctyname'] = list(fips[fips['scfips'] == 35013]['ctyname'])[0]
# 5th correction
trow = cdCty.index[(cdCty['stabbr'] == 'SD') & (cdCty['ctyname'] == 'Shannon County')]
print(cdCty.loc[trow, :].to_string())
cdCty.drop(axis = 0, index = trow, inplace = True)
cdCty.reset_index(drop = True, inplace = True)
# merge
cdCty = fips.merge(cdCty, on = ['stabbr', 'ctyname', 'scfips'], how = 'outer')
csse = csse.merge(cdCty, on = list(idDict.variable_name), how = 'outer')
# output data
csse.to_csv(filedir3 + 'county_casesAndDeaths.csv', index = False)
# dictionary
cdCtyDict = pd.read_excel(filedir2 + 'Deaths_by_County_Dictionary.xlsx')
cdCtyDict.rename(columns = {'variable name': 'variable_name', 'start column': 'start_column',\
                            'end column': 'end_column', 'start date': 'start_date',\
                            'end date': 'end_date'}, inplace = True)
print(cdCtyDict)
print(cdCty.columns)
cdCtyDict.loc[0, 'variable_name'] = 'death_startdate'
cdCtyDict.loc[5, 'variable_name'] = list(cdCty.columns)[8]
cdCtyDict.loc[6, 'variable_name'] = list(cdCty.columns)[9]
cdCtyDict.drop(axis = 0, index = [1, 2, 3], inplace = True)
dcDict = pd.concat([idDict, csseDict, cdCtyDict], axis = 0, join = 'outer')
dcDict.reset_index(drop = True, inplace = True)
dcDict.loc[:, 'file'] = ['county_casesAndDeaths.csv'] * dcDict.shape[0]
dcDict = get_dict(csse, dcDict)
# remove data objects from environment to save memory
del [csse, csseDict, trow, cdCty, cdCtyDict]


## CDC vaccination by county
# read data
vacCty = pd.read_csv(filedir4 + 'Vaccinations_by_County.csv', low_memory = False)
# check data with 'UNK" for unknown state/county
unk0 = vacCty[vacCty['stname'] == 'UNK']
unk1 = vacCty[(vacCty['scfips'] == 'UNK') & (vacCty['stname'] != 'UNK')]
print('{} rows of unknown state, \n{} rows of known state but unknown county, \n{} states with unknown-county records:'.\
      format(unk0.shape[0], unk1.shape[0], len(set(unk1.stname))))
print(', '.join(sorted(list(set(unk1.stname)))))
# remove rows with unknown state or county
print('{} rows in cdcVacCty BEFORE removal of rows with unknown state/county'.format(vacCty.shape[0]))
vacCty = vacCty[(vacCty['stname'] != 'UNK') & (vacCty['scfips'] != 'UNK')]
print('{} rows in cdcVacCty AFTER removal of rows with unknown state/county'.format(vacCty.shape[0]))
# format adjustment
vacCty['scfips'] = pd.to_numeric(vacCty['scfips'])
vacCty['date'] = vacCty['date'].astype('str', copy = True)
vacCty.rename(columns = {'stname': 'stabbr'}, inplace = True)
# merge fips and cdcVacCty
vacCty = fips.merge(vacCty, on = ['stabbr', 'ctyname', 'scfips'], how = 'outer')
# reshape to wide
vacCty = pd.pivot_table(vacCty, index = ['stfips', 'stabbr', 'stname',\
                                               'ctyfips', 'ctyname', 'scfips'],\
                    columns = 'date', values = 'dose1_')
vacCty.reset_index(drop = False, inplace = True)
vacCty.columns = list(vacCty.columns)[:6] +\
    ['dose1_' + x for x in list(vacCty.columns)[6:]]
# output
vacCty['stfips'] = vacCty['stfips'].astype('int')
vacCty['ctyfips'] = vacCty['ctyfips'].astype('int')
vacCty['scfips'] = vacCty['scfips'].astype('int')
vacCty.to_csv(filedir3 + 'county_vaccination.csv', index = False)
# ditionary
cols = list(set([re.sub('_\d{8}', '', x) for x in list(vacCty.columns)[6:]]))
# only one item to add to dictionary
vacDict = idDict.append(idDict.iloc[5, :])
vacDict.reset_index(drop = True, inplace = True)
vacDict.loc[6, 'variable_name'] = cols[0] + '_yyyymmdd'
vacDict.loc[6, 'label'] = 'People with at least one dose administered'
vacDict.loc[6, 'source'] = 'https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh'
vacDict['file'] = ['county_vaccination.csv'] * vacDict.shape[0]
vacDict = get_dict(vacCty, vacDict)
# remove data from environment to save memory
del [vacCty, cols, unk0, unk1]


# Take out medical data from GovEx: non-time-series data for actually time-varying items
# ## medical_govex
# # read data
# medicalGovex = pd.read_csv(filedir1 + 'medical_govex.csv')
# medicalGovex.rename(columns = {'fips': 'scfips'}, inplace = True)
# # reorder columns
# cols = list(idDict.variable_name) + [x for x in list(medicalGovex.columns) if x not in list(idDict.variable_name)]
# medicalGovex = medicalGovex[cols]
# # dictionary
# mgDict = pDict[pDict['file'] == 'medical_govex.csv']
# mgDict = pd.concat([idDict, mgDict], axis = 0, join = 'outer')
# mgDict.reset_index(drop = True, inplace = True)
# print('{} variables in data, and {} variables in dictionary'.\
#       format(medicalGovex.shape[1], mgDict.shape[0]))
# # keep variables in dictionary only
# medicalGovex = medicalGovex[list(mgDict['variable_name'])]
# mgDict = get_dict(medicalGovex, mgDict)
# # output
# medicalGovex.to_csv(filedir3 + 'county_medical.csv', index = False)
# mgDict['file'] = 'county_medical.csv'
# # remove data from environment to save memory
# del [medicalGovex, cols]


## mobility_descartes
# read data
mdData = pd.read_csv(filedir1 + 'mobility_descartes.csv')
mdData.drop(axis = 1, columns = 'Unnamed: 0', inplace = True)
mdData.rename(columns = {'fips': 'scfips'}, inplace = True)
# check items
cols = set([re.sub('_\d{8}', '', x) for x in list(mdData.columns)])
print(cols)
print('{} rows in mobility_descartes before merging with fips'.format(mdData.shape[0]))
# merge with fips to get stabbr
mdData = fips.merge(mdData, on = ['stfips', 'stname', 'ctyfips', 'ctyname', 'scfips'], how = 'outer')
print('{} rows in mobility_descartes after merging with fips'.format(mdData.shape[0]))
# add descartes prefix to variable names
mdData.columns = list(mdData.columns)[:6] + ['descartes_' + x for x in list(mdData.columns)[6:]]
# output data
#mdData.to_csv(filedir4 + '../county_mobilityDescartes.csv', index = False)
# dictionary
mdDict = pDict[pDict['file'] == 'mobility_descartes.csv'].copy()
mdDict.loc[:, 'variable_name'] = ['descartes_' + x for x in list(mdDict.variable_name)]
mdDict = pd.concat([idDict, mdDict], axis = 0, join = 'outer')
mdDict.reset_index(drop = True, inplace = True)
#mdDict = get_dict(mdData, mdDict)
#mdDict['file'] = 'county_mobilityDescartes.csv'
# remove data from environment to save memory
del cols


# mobility_unacast
# read data
muData = pd.read_csv(filedir1 + 'mobility_unacast.csv')
muData.drop(axis = 1, columns = 'Unnamed: 0', inplace = True)
muData.rename(columns = {'fips': 'scfips'}, inplace = True)
# check existint items
cols = set([re.sub('_\d{8}', '', x) for x in list(muData.columns)])
print(cols)
print('{} rows in mobility_unacast before merging with fips'.format(muData.shape[0]))
muData = fips.merge(muData, on = ['stfips', 'stname', 'ctyfips', 'ctyname', 'scfips'],\
                    how = 'outer')
print('{} rows in mobility_unacast after merging with fips'.format(muData.shape[0]))
cols = set([re.sub('_\d{8}', '', x) for x in list(muData.columns)])
print(cols)
# sort columns
cols = list(muData.columns)[:6] + sorted(list(muData.columns)[6:])
muData = muData[cols]
# add unacast prefix
muData.columns = list(muData.columns)[:6] + ['unacast_' + x for x in list(muData.columns)[6:]]


## merge mobility_descarted and mobility_unacast
muData = mdData.merge(muData, on = list(idDict.variable_name), how = 'outer')
muData.to_csv(filedir3 + 'county_mobility.csv', index = False)
# dictionary
muDict = pDict[pDict['file'] == 'mobility_unacast.csv'].copy()
muDict.loc[:, 'variable_name'] = ['unacast_' + x for x in list(muDict.variable_name)]
# correct a mis-specified variable in muDict
muDict.reset_index(drop = True, inplace = True)
muDict.loc[0, 'variable_name'] = 'unacast_county_population_2018'
# append two dictionaries
muDict = pd.concat([mdDict, muDict], axis = 0, join = 'outer')
muDict.reset_index(drop = True, inplace = True)
# get column indices
muDict = get_dict(muData, muDict)
muDict['file'] = 'county_mobility.csv'


#===========================
# Step 3: append dictionary
#===========================

# fdct = pd.concat([dcDict, vacDict, mgDict, muDict], axis = 0, join = 'outer')
fdct = pd.concat([dcDict, vacDict, muDict], axis = 0, join = 'outer')
fdct.reset_index(drop = True, inplace = True)

# adjust the column names for users
fdct.rename(columns = {'source': 'link'}, inplace = True)
# source
fdct['source'] = fdct['file'].copy()
fdct['source'].replace(to_replace = {'county_casesAndDeaths.csv': 'Census',\
                                     'county_medical.csv': 'GovEx',\
                                     'county_mobility.csv': 'Unacast',\
                                     'county_vaccination.csv': 'CDC'},\
                       inplace = True)
fdct.loc[fdct.link == 'https://www.census.gov/geographies/reference-files/2018/demo/popest/2018-fips.html', 'source'] = 'Census'
fdct.loc[fdct.link == 'https://github.com/CSSEGISandData/COVID-19', 'source'] = 'CSSE'
fdct.loc[fdct.link == 'https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-in-the-United-St/kn79-hsxy', 'source'] = 'CDC'
fdct.loc[fdct.link == 'https://github.com/descarteslabs/DL-COVID-19', 'source'] = 'Descartes'

# mark variables' fields
fdct['field'] = fdct['file'].copy()
fdct['field'].fillna(value = 'state or county identifier', inplace = True)
fdct['field'].replace(to_replace = {'county_casesAndDeaths.csv': 'cases and deaths',\
                                    'county_medicalGovex.csv': 'medical',\
                                    'county_mobility.csv': 'mobility',\
                                    'county_vaccination.csv': 'vaccination'},\
                       inplace = True)

# file names in release 4 if existed
fdct['filename_in_release4'] = fdct['file'].copy()
fdct['filename_in_release4'].replace(to_replace = {'county_casesAndDeaths.csv': 'casesAndDeaths.csv',\
                                                   'county_vaccination.csv': '',\
                                                   'county_mobility.csv': 'mobility_unacast.csv'},\
                                      inplace = True)
fdct.loc[fdct.link == 'https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-in-the-United-St/kn79-hsxy', 'filename_in_release4'] = ''
fdct.loc[fdct.source == 'Descartes', 'filename_in_release4'] = 'mobility_descartes.csv' 
    
# reorder columns
fdct = fdct[['variable_name', 'label', 'file', 'field', 'source', 'link', \
             'start_column', 'end_column', 'start_date', 'end_date',\
             'filename_in_release4']]

# output
fdct.to_csv(filedir3 + 'county_data_dictionary.csv', index = False)


