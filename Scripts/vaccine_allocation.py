#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 23:26:23 2021
Moved from Jupyter Notebook to inspect and implement code consistently

@author: Xingyun Wu
"""

import pandas as pd
from datetime import datetime


# read data
file_dir = '/Users/xywu/Documents/HPC_datahub/vaccine/COVID-19_Vaccine_Distribution_Allocations_by_Jurisdiction_-_'
pfizer = pd.read_csv(file_dir + 'Pfizer.csv')
pfizer = pfizer.pivot(index = 'Jurisdiction', columns = 'Week of Allocations', \
             values = ['1st Dose Allocations', '2nd Dose Allocations'])
moderna = pd.read_csv(file_dir + 'Moderna.csv')
moderna = moderna.pivot(index = 'Jurisdiction', columns = 'Week of Allocations', \
             values = ['1st Dose Allocations', '2nd Dose Allocations'])


# define an auxiliary function to extrace date from a column name
def edit_colname(colname, brand):
    '''
    Parameters
        colname: a string of column name

    Returns: 
        rv: a string of vaccine allocation date if it's a data column
            none if it's a jurisdiction or region code column
    '''
    temp_date = colname[1]
    temp_date = datetime.strptime(temp_date, '%m/%d/%Y').strftime('%Y%m%d')
    # first dose or second dose
    temp_dose = colname[0]
    if temp_dose == '1st Dose Allocations':
        temp_dose = 'dose1'
    elif temp_dose == '2nd Dose Allocations':
        temp_dose = 'dose2'
    rv = temp_date + '_allocation_' + brand + '_' + temp_dose

    # return the output
    return rv

# modify column names of dataframe
pfizer.columns = [edit_colname(x, 'pfizer') for x in pfizer.columns]
pfizer.insert(loc = 0, column = 'jurisdiction', value = pfizer.index)
pfizer.index = range(pfizer.shape[0])
moderna.columns = [edit_colname(x, 'moderna') for x in moderna.columns]
moderna.insert(loc = 0, column = 'jurisdiction', value = moderna.index)
moderna.index = range(moderna.shape[0])


## reorder the columns
# pfizer
dts_pfizer = sorted(set([x.split('_')[0] for x in pfizer.columns[1:]]))
col_pfizer = [x + '_allocation_pfizer_dose' + y for x in dts_pfizer for y in ['1', '2']]
col_pfizer = [pfizer.columns[0]] + col_pfizer
pfizer = pfizer[col_pfizer]
# moderna
dts_moderna = sorted(set([x.split('_')[0] for x in moderna.columns[1:]]))
col_moderna = [x + '_allocation_moderna_dose' + y for x in dts_moderna for y in ['1', '2']]
col_moderna = [moderna.columns[0]] + col_moderna
moderna = moderna[col_moderna]


## merge two dataframes
df = pfizer.merge(moderna, left_on='jurisdiction', right_on='jurisdiction')


## remove the US territory and federal entities rows
list(df.jurisdiction)
to_rm = ['American Samoa', 'American Samoa**', 'Federal Entities', 'Guam', \
         'Guam**', 'Mariana Islands', 'Mariana Islands**', 'Marshall Islands',\
         'Marshall Islands*', 'Micronesia', 'Micronesia*', 'Palau', 'Palau*',\
         'Puerto Rico', 'U.S. Virgin Islands']
to_rm_id = [df.index[df['jurisdiction']==x].tolist()[0] for x in to_rm]
df['jurisdiction'][to_rm_id]
df = df.drop(to_rm_id, axis=0)
# combine separated rows
df['jurisdiction'] = df['jurisdiction'].str.replace('[^\w\s]', '')
df = df.groupby('jurisdiction',as_index=False).agg('sum')


## output to csv file
df.to_csv('/Users/xywu/Documents/HPC_Datahub/vaccine/vaccine_allocation.csv', index=False)

