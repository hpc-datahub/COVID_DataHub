#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 05:35:55 2021

@author: Xingyun Wu
"""

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
#from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time
import re

print('Program starts')

url = 'https://covid.cdc.gov/covid-data-tracker/#vaccinations'

driver = webdriver.Chrome('/Users/xywu/Documents/authenticator_driver/chromedriver')
driver.get(url)

# make the thread sleep to let the page load fully
print('Wait time starts')
time.sleep(60)
print('Wait time finished. Start scraping...')


# parse
#driver.implicitly_wait(120)
#wait = WebDriverWait(driver, 10)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# check time of update
time_update = soup.find('div', attrs={'class':'general_note'}).text
time_update = time_update.split(':', 1)[1].strip()
print(time_update)
# save the time of data update (instead of data posted)
time_update = time_update.split('.')[0]
time_update = re.sub('\s+', ' ', time_update)
time_update = time_update.strip('ET').strip()
time_update = datetime.strptime(time_update, '%B %d, %Y %H:%M%p').strftime('%Y%m%d')

# see whether updated today
today = datetime.today()
today = today.strftime("%Y%m%d")
if time_update == today:
    print(today)
    # extract information from soup
    table = soup.find('table')
    table_rows = table.find_all('tr')
    info = []
    for i in range(len(table_rows)):
        tr = table_rows[i]
        if i == 0:
            th = tr.find_all('th')
            row = [tr.text for tr in th]
        else:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
        info.append(row)
    # output
    df = pd.DataFrame(info[1:], columns=info[0])
    filename = '~/Documents/ra/HPC_datahub/vaccine/temp_data/vaccine_distribution-'+today+'.csv'
    df.to_csv(filename, index=False)
    print('Vaccine data saved.')
else:
    print('Not yet updated today.')


driver.quit()
