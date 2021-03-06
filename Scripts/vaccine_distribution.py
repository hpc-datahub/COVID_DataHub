#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 23:15:52 2021

@author: Xingyun Wu
"""

import os
import re
import pandas as pd

# load the previous data and save a backup
file_dir = '/Users/xywu/Documents/HPC_datahub/vaccine/'
orig_df = pd.read_csv(file_dir + 'vaccine_distribution.csv')
orig_df.to_csv(file_dir + 'vaccine_distribution_last_week.csv', index=False)

# extract target filenames
data_dir = file_dir + 'temp_data'
file_all = os.listdir(data_dir)
# get rid of '.DS_Store' in the folder if any
try:
    file_all.remove('.DS_Store')
except ValueError:
    pass
# extract dates
dts = []
for i in range(len(file_all)):
    temp_file = file_all[i].split('-')
    temp_date = re.sub('\..*', '', temp_file[1])
    dts.append(int(temp_date))
dts

# reorder the filename list
dts_order = [dts.index(x) for x in sorted(dts)]
file_lst = [file_all[dts_order[x]] for x in range(len(dts_order))]

# read all data into a list of dataframes
df_lst = []
for i in range(len(file_lst)):
    df_lst.append(pd.read_csv(file_dir + 'temp_data/' + file_lst[i]))

# rename columns
dts = sorted(dts)
for i in range(len(dts)):
    temp_colnames = [df_lst[i].columns[0]] + [str(dts[i])+'_'+df_lst[i].columns[x] \
                                              for x in range(1, df_lst[i].shape[1])]
    df_lst[i].columns = temp_colnames

# join the seperate dataframes into one dataframe
df = df_lst[0]
for i in range(1, len(df_lst)):
    df = df.merge(right=df_lst[i], on='State/Territory/Federal Entity', how='outer')
# check
#print(df.shape)
#df.columns
    
# modify column names to lower case and replace spaces with udnerscore


# remove the jurisdictions outside of the 50 continent states
# identify the rows outside of the 50 continent states
to_rm = ['American Samoa', 'Bureau of Prisons', 'Dept of Defense', \
         'Federated States of Micronesia', 'Guam', 'Indian Health Svc',\
         'Marshall Islands', 'Northern Mariana Islands', 'Puerto Rico',\
         'Republic of Palau', 'Veterans Health', 'Virgin Islands']
# remove
to_rm_id = [df.index[df['State/Territory/Federal Entity']==x].tolist()[0] for x in to_rm]
df = df.drop(to_rm_id,  axis=0)

# rename df columns
col1 = [str.replace(x.lower(), ' ', '_') for x in list(df.columns)]
m = re.compile('(\d+)(.*)')
col2 = [m.search(x).group(1) + '_distribution' + m.search(x).group(2) \
            for x in col1[1:]]
df.columns = [col1[0]] + col2
    

# merge with previous data
final = orig_df.merge(right=df, on='state/territory/federal_entity', how='outer')


# output file
final.to_csv(file_dir + '/' + 'vaccine_distribution.csv', index=False)

