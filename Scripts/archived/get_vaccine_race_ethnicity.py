#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 06:51:08 2021

@author: Xingyun Wu
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import re


print('Program starts')

url = 'https://www.apmresearchlab.org/covid/vaccines-by-race'

# open the website with Chrome
driver = webdriver.Chrome('/Users/xywu/Documents/authenticator_driver/chromedriver')
driver.get(url)
# give it some time to load fully
time.sleep(15)

# check if a popup window for subscription exists => if yes, close it
driver.find_element_by_class_name('sqs-popup-overlay-close').click()

soup = BeautifulSoup(driver.page_source, 'html.parser')
t = soup.find_all('div')
t[9]
tt = t[9].find_all()


# scroll to the iframe containing the data table at the end of the page
iframe = driver.find_element_by_css_selector('#datawrapper-chart-avLfw')
driver.switch_to.frame('datawrapper-chart-avLfw')

# scroll the page down to the end (mimic human user)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

t = driver.find_elements_by_tag_name('iframe')
t = driver.find_elements_by_id('block-5cf7919c99b07749b57f')
t = driver.find_elements_by_class_name('sqs-block-content')
# 39, 40


t = driver.find_elements_by_tag_name('div')
# 145 to 150 ==> 145
for i in range(len(t)):
    print(i)
    time.sleep(2)
    print(t[i].text)


t = driver.find_elements_by_xpath('//*[@id="datawrapper-chart-7sC31"]')
driver.switch_to.frame(driver.find_element_by_id('datawrapper-chart-7sC31'))


driver.quit()

### Above doesn't work ###


# set url to scrape
url = 'https://datawrapper.dwcdn.net/7sC31/1/'

# open the website with Chrome
driver = webdriver.Chrome('/Users/xywu/Documents/authenticator_driver/chromedriver')
driver.get(url)

# parse
soup = BeautifulSoup(driver.page_source, 'html.parser')

# get update date
note = soup.find('i').text
dt = re.search(r'[\w]+[\s]*[\d]+, [\d]{4}', note).group()
print(dt)
dt = datetime.strptime(dt, '%B %d, %Y').strftime('%Y%m%d')
dt

# get data
data = []
table = soup.find('table')
rows = table.find_all('tr')
cols = [[], []]
for i in range(len(rows) + 1):
    if i == len(rows):
        data.append(cols)
        break
    items = rows[i].find_all('span')
    items = [x.text.strip() for x in items]
    if len(items) == 0:
        data.append(cols)
        cols = [[], []]
    else:
        if len(cols[1]) > 0:
            if items[1] == '':
                items[1] = -1
            else:
                items[1] = items[1].replace(',', '').replace('−', '-')
                items[1] = int(items[1])
        # append cleaned data to list
        cols[0].append(items[0])
        cols[1].append(items[1])

df = pd.DataFrame([row[1] for row in data], columns = data[0][0])
df.to_csv('~/Documents/ra/HPC_datahub/ColorOfVaccine/data_' + dt + '.csv', index = False)


driver.quit()
