"""
Transform a .csv file of point clouds with tabs into a standard .csv file with commas
"""

import csv


def conversion(nameWithoutExtension):
    fileCsv = open(nameWithoutExtension + '.csv')
    csvreader = csv.reader(fileCsv)
    fileTxt = open(nameWithoutExtension + 'SansTabulation.csv', 'w')
    for row in csvreader:
        if row != []:  # last line is empty
            line = row[0]
            newLine = ''
            i = 0
            for j in range(3):
                word = ''
                while line[i] != '\t':
                    word += line[i]
                    i += 1
                newLine += word
                if j != 2:
                    newLine += ','
                i += 1

            # we have retrieved the coordinates
            fileTxt.write(newLine)
            fileTxt.write('\n')

    fileCsv.close()
    fileTxt.close()
  
name = 'resultline1'
conversion(name)
