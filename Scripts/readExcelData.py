# Reading an excel file using Python 
import xlrd 
import os,glob
import csv

folder_path = '/Users/apoorvdayal/Desktop/RA-PublicHealth/Suru_Data/AllData'
allList = []
for filename in glob.glob(os.path.join(folder_path, '*.xlsx')):
  with open(filename, 'r') as f:
    print (filename)
    loc = (filename)
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_name("Ranked Measure Data") 
    # For row 0 and column 0 
    # print(sheet.cell_value(3,201))

    i=4
    allRows = sheet.nrows
    for i in range(3,allRows):
        curr_dictionary = {}
        curr_dictionary['county'] = sheet.cell_value(i,2)
        curr_dictionary['bool'] = sheet.cell_value(i,201)
        curr_dictionary['z'] = sheet.cell_value(i,202)
        # print(curr_dictionary)
        allList.append(curr_dictionary)
        
print(allList)
with open('tempData.csv', mode='w') as csv_file:
    fieldnames = ['county', 'bool', 'z']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for i in allList:
        # print(i)
        writer.writerow(i)