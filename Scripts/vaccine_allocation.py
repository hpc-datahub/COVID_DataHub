#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 23:26:23 2021
Python script to read and process CDC's weekly updated vaccine allocation data

@author: Xingyun Wu
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

# set update date
dt = '20210309'

# set data file directory
file_dir = '~/Documents/HPC_datahub/vaccine/history_raw/COVID-19_Vaccine_Distribution_Allocations_by_Jurisdiction_-_'

def read_data(filedir, brand, update_date):
    df1 = pd.read_csv(file_dir + brand + '_' + update_date + '.csv')
    df1.columns = [x.lower() for x in df1.columns]
    print(df1.shape)
    
    # parse the stars as notations
    notes = []
    for i in range(df1.shape[0]):
        temp = df1.loc[i, 'jurisdiction']
        temp_stars = re.findall('[\*]+', temp)
        temp_notes = np.zeros(shape = 4, dtype = int)
        for j in range(len(temp_stars)):
            temp_notes[len(temp_stars[j]) - 1] += 1
            print(i, temp_stars[j], temp_notes)
        notes.append(temp_notes)
    
    # create a data frame for notations
    df2 = pd.DataFrame(data = np.array(notes), columns = ['no_pfizer_because_ultra_cold_requirement',\
                                               'receive_dose1_dose2_simultaneously',\
                                               'sovereign_nation_supplement', \
                                               'federal_entities'])
    
    # combine two data frames
    df1 = df1.join(df2, how = 'outer')
    df1 = df1.drop(columns = 'federal_entities')
    if brand in ['Moderna', 'Janssen']:
        df1 = df1.drop(columns = 'no_pfizer_because_ultra_cold_requirement')
    cols = df1.columns
    
    # reshape from long to wide
    df1['jurisdiction'] = df1['jurisdiction'].str.replace('[^\w\s]', '')
    df1 = df1.pivot(index = 'jurisdiction', columns = 'week of allocations')

    return df1, cols


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
    
    # standardize column names for doses
    temp_col = colname[0]
    if temp_col == '1st dose allocations':
        temp_col = 'allocation_dose1'
    elif temp_col == '2nd dose allocations':
        temp_col = 'allocation_dose2'
    
    # set return value
    if temp_col == 'no_pfizer_because_ultra_cold_requirement':
        rv = temp_col + '_' + temp_date
    else:
        rv = brand + '_' + temp_col + '_' + temp_date

    # return the output
    return rv


## process Pfizer data
pfizer, pfizer_cols = read_data(file_dir, 'Pfizer', dt)
# modify column names of dataframe
pfizer.columns = [edit_colname(x, 'pfizer') for x in pfizer.columns]
pfizer.insert(loc = 0, column = 'jurisdiction', value = pfizer.index)
pfizer.index = range(pfizer.shape[0])
# reorder the columns according to date
pfizer = pfizer[sorted(pfizer.columns)]

## process Moderna data
moderna, moderna_cols = read_data(file_dir, 'Moderna', dt)
# modify column names of dataframe
moderna.columns = [edit_colname(x, 'moderna') for x in moderna.columns]
moderna.insert(loc = 0, column = 'jurisdiction', value = moderna.index)
moderna.index = range(moderna.shape[0])
# reorder the columns according to date
moderna = moderna[sorted(moderna.columns)]

## Janssen
dt = '20210311'
janssen, janssen_cols = read_data(file_dir, 'Janssen', dt)
# modify column names of dataframe
janssen.columns = [edit_colname(x, 'janssen') for x in janssen.columns]
janssen.insert(loc = 0, column = 'jurisdiction', value = janssen.index)
janssen.index = range(janssen.shape[0])
# reorder the columns according to date
janssen = janssen[sorted(janssen.columns)]


## merge two dataframes
df = pfizer.merge(moderna, left_on='jurisdiction', right_on='jurisdiction')
df = df.merge(janssen, left_on='jurisdiction', right_on='jurisdiction')


## output to csv file
df.to_csv('~/Documents/GitHub/COVID_Datahub/Pandemic/vaccine_allocation.csv', index=False)

