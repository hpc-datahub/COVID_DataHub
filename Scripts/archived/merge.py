# Reading an excel file using Python 
import xlrd 
import os,glob
import csv

loc = '/Users/apoorvdayal/Desktop/RA-PublicHealth/Suru_Data/temps.xlsx'
allList = []
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_name("temp") 
sheet2 = wb.sheet_by_name("water") 
print(wb.sheet_names())
allRows = sheet.nrows
allRows2 = sheet2.nrows
l1 = []
l2 = []
for i in range(1,allRows):
    l1.append(sheet.cell_value(i,0))
    curr_dictionary['PS-GWPop'] = sheet.cell_value(i,7)
    curr_dictionary['PS-SWPop'] = sheet.cell_value(i,8)
    curr_dictionary['PS-TOPop'] = sheet.cell_value(i,9)
    curr_dictionary['PS-WSWTo'] = sheet.cell_value(i,12)
    curr_dictionary['PS-WFrTo'] = sheet.cell_value(i,16)
    curr_dictionary['PS-Wtotl'] = sheet.cell_value(i,18)
    curr_dictionary['DO-SSPop'] = sheet.cell_value(i,19)
    curr_dictionary['DO-WFrTo'] = sheet.cell_value(i,22)
    curr_dictionary['DO-PSDel'] = sheet.cell_value(i,24)
    curr_dictionary['DO-PSPCp'] = sheet.cell_value(i,25)
    curr_dictionary['DO-WDelv'] = sheet.cell_value(i,26)
    print(curr_dictionary)
    allList.append(curr_dictionary)

finDictionList = []
for i in range(1,allRows2):
    curr_dictionary = {}
    curr_dictionary['FIPS'] = sheet2.cell_value(i,5)
    l2.append(sheet2.cell_value(i,5))
    curr_dictionary['Drinking_Water_Violations'] = sheet2.cell_value(i,6)
    curr_dictionary['Drinking_Water_Violations_Z-Score'] = sheet2.cell_value(i,7)
    finDictionList.append(curr_dictionary)
    
finList = []
# print(len(l1))
# print("****")
# print(len(l2))
for i in range(0,len(l1)):
    if l1[i] in l2:
        finList.append(l1[i])
print(len(finList))

# for i in range(1,allRows):
#     curr_dictionary = {}
#     if sheet.cell_value(i,0) in finList:
#         curr_dictionary['FIPS'] = sheet.cell_value(i,0)
#         curr_dictionary['PS-GWPop'] = sheet.cell_value(i,7)
#         curr_dictionary['PS-SWPop'] = sheet.cell_value(i,8)
#         curr_dictionary['PS-TOPop'] = sheet.cell_value(i,9)
#         curr_dictionary['PS-WSWTo'] = sheet.cell_value(i,12)
#         curr_dictionary['PS-WFrTo'] = sheet.cell_value(i,16)
#         curr_dictionary['PS-Wtotl'] = sheet.cell_value(i,18)
#         curr_dictionary['DO-SSPop'] = sheet.cell_value(i,19)
#         curr_dictionary['DO-WFrTo'] = sheet.cell_value(i,22)
#         curr_dictionary['DO-PSDel'] = sheet.cell_value(i,24)
#         curr_dictionary['DO-PSPCp'] = sheet.cell_value(i,25)
#         curr_dictionary['DO-WDelv'] = sheet.cell_value(i,26)
#         print(curr_dictionary)
resultArray = []
for i in range(1,allRows2):
    if finDictionList[i]['FIP'] in finList:
        temp = finDictionList[i]['FIP']
        for i in range(1,allRows1):
            if temp = 
        curr_dictionary['PS-GWPop'] = sheet.cell_value(i,7)
        curr_dictionary['PS-SWPop'] = sheet.cell_value(i,8)
        curr_dictionary['PS-TOPop'] = sheet.cell_value(i,9)
        curr_dictionary['PS-WSWTo'] = sheet.cell_value(i,12)
        curr_dictionary['PS-WFrTo'] = sheet.cell_value(i,16)
        curr_dictionary['PS-Wtotl'] = sheet.cell_value(i,18)
        curr_dictionary['DO-SSPop'] = sheet.cell_value(i,19)
        curr_dictionary['DO-WFrTo'] = sheet.cell_value(i,22)
        curr_dictionary['DO-PSDel'] = sheet.cell_value(i,24)
        curr_dictionary['DO-PSPCp'] = sheet.cell_value(i,25)
        curr_dictionary['DO-WDelv'] = sheet.cell_value(i,26)

        