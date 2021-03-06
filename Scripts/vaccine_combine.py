#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 01:11:13 2021

@author: Xingyun Wu
"""

import pandas as pd


data_dir = '/Users/xywu/Documents/HPC_datahub/vaccine/'


## allocation data
vaccine_alct = pd.read_csv(data_dir + 'vaccine_allocation.csv', thousands=',')
# combine city data into corresponding state
states = ['New York', 'Pennsylvania', 'Illinois']
cities = ['New York City', 'Philadelphia', 'Chicago']
cities_id = [vaccine_alct.index[vaccine_alct['jurisdiction']==x].\
             tolist()[0] for x in cities]
for i in range(len(cities)):
    vaccine_alct.iloc[cities_id[i], 0] = states[i]
vaccine_alct = vaccine_alct.groupby('jurisdiction',as_index=False).agg('sum')


## distribution data
vaccine_dist = pd.read_csv(data_dir + 'vaccine_distribution.csv')
ny_id = vaccine_dist.index[vaccine_dist['state/territory/federal_entity']==\
                           'New York State'].tolist()[0]
vaccine_dist.iloc[ny_id, 0] = 'New York'


# combine allocation data and distribution
df = vaccine_alct.merge(vaccine_dist, how='outer', left_on='jurisdiction',\
                        right_on='state/territory/federal_entity')
    
# drop redundant state-name column
df = df.drop('state/territory/federal_entity', axis=1)

# output
df.to_csv(data_dir + 'vaccine.csv', index=False)

