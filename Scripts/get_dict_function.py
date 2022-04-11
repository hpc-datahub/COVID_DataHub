#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:46:24 2022

@author: Xingyun Wu
"""

import re


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
