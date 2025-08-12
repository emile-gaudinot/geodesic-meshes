"""
Convert csv files to txt files that GMSH can read
"""

import csv


def conversion(nameWithoutExtension):
    fileCsv = open(nameWithoutExtension + '.csv')
    csvreader = csv.reader(fileCsv)
    header = next(csvreader)
    fileTxt = open(nameWithoutExtension + '.txt', 'w')
    nbPts = 1
    for row in csvreader:
        if row != []:  # last line is empty
            line = row[0]
            coos = []
            i = 0
            for j in range(3):
                word = ''
                while line[i] != '\t':
                    word += line[i]
                    i += 1
                coos.append(float(word))
                i += 1
            # we have retrieved the coordinates
            fileTxt.write('//+\n')
            fileTxt.write('Point(' + str(nbPts) + ') = {' + str(coos[0]) + ', ' +
                          str(coos[1]) + ', ' + str(coos[2]) + ', 1.0};\n')
            nbPts += 1
    fileCsv.close()
    fileTxt.close()


name = 'resultline'
for i in range(1, 10):
    nameWithoutExtension = name + str(i)
    conversion(nameWithoutExtension)
