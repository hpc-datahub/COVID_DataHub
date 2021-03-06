# Reading an excel file using Python 
import xlrd 
import os,glob
import csv

loc = '/Users/apoorvdayal/Desktop/RA-PublicHealth/Suru_Data/usco2015v2.0.csv'
loc2 = '/Users/apoorvdayal/Desktop/RA-PublicHealth/Suru_Data/uscoCpy.csv'
# allRows = sheet.nrows
# for i in range(2,allRows):
allList = []
# print(curr_dictionary)
# for a in colNames:
#     print(columns[a])
with open(loc) as csv_file:
    csvFile = csv.reader(csv_file, delimiter=',')
    for row in csvFile:
        print(row[4])
        curr_dictionary = {}
        curr_dictionary['FIPS'] = row[4]
        curr_dictionary['PS-GWPop'] = row[7]
        curr_dictionary['PS-SWPop'] = row[8]
        curr_dictionary['PS-TOPop'] = row[9]
        curr_dictionary['PS-WSWTo'] = row[12]
        curr_dictionary['PS-WFrTo'] = row[16]
        curr_dictionary['PS-Wtotl'] = row[18]
        curr_dictionary['DO-SSPop'] = row[19]
        curr_dictionary['DO-WFrTo'] = row[22]
        curr_dictionary['DO-PSDel'] = row[24]
        curr_dictionary['DO-PSPCp'] = row[25]
        curr_dictionary['DO-WDelv'] = row[26]
        print(curr_dictionary)
        allList.append(curr_dictionary)


with open('temp.csv', mode='w') as csvfile:
    colNames = ['FIPS','PS-GWPop','PS-SWPop','PS-TOPop','PS-WSWTo','PS-WFrTo','PS-Wtotl','DO-SSPop',
'DO-WFrTo','DO-PSDel','DO-PSPCp','DO-WDelv']
    writer = csv.DictWriter(csvfile, fieldnames=colNames)
    writer.writeheader()
    for i in allList:
        # print(i)
        writer.writerow(i)