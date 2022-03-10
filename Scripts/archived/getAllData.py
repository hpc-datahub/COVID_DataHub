import requests
# import urllib2
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
state_array = ['Alabama',
'Alaska',
'Arizona',
'Arkansas',
'California',
'Colorado',
'Connecticut',
'Delaware',
'Florida',
'Georgia',
'Hawaii',
'Idaho',
'Illinois',
'Indiana',
'Iowa',
'Kansas',
'Kentucky',
'Louisiana',
'Maine',
'Maryland',
'Massachusetts',
'Michigan',
'Minnesota',
'Mississippi',
'Missouri',
'Montana',
'Nebraska',
'Nevada',
'New-Hampshire',
'New-Jersey',
'New-Mexico',
'New-York',
'North-Carolina',
'North-Dakota',
'Ohio',
'Oklahoma',
'Oregon',
'Pennsylvania',
'Rhode-Island',
'South-Carolina',
'South-Dakota',
'Tennessee',
'Texas',
'Utah',
'Vermont',
'Virginia',
'Washington',
'West-Virginia',
'Wisconsin',
'Wyoming']
fin_array = []
for a in state_array:
    fin_array.append(a.lower())


for a in fin_array:
    print(a)

url = "https://www.countyhealthrankings.org/app/alabama/2020/measure/factors/124/data"
r = Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
html = urlopen(r)
soup = BeautifulSoup(html, "html.parser")
print(soup)
table = soup.findAll("table", {"class":["measure-data-table", "sticky-enabled"]})
print(table)
# rows = table.findAll("tr")
# with open("editors.csv", "wt+", newline="") as f:
#     writer = csv.writer(f)
#     for row in rows:
#         csv_row = []
#         for cell in row.findAll(["td", "th"]):
#             csv_row.append(cell.get_text())
#         writer.writerow(csv_row)
# base_url = 'https://www.countyhealthrankings.org/sites/default/files/media/document/2020-County-Health-Rankings-'
# end_url = '%20Data%20-%20v1.xlsx'
# for i in state_array:
#     final_url = base_url + i + end_url
#     filedata = urllib2.urlopen(final_url)
#     dataToWrite = filedata.read()
#     with open('/Users/Data'+i+'_data.xlsx', 'wb') as f:
#         f.write(dataToWrite)
#     print(final_url)