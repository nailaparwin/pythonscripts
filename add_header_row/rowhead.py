###########################################
# This code assigns a head row 
###########################################
#   Required Input File
##########################################


input_file = 'partial_dos.dat'
output_file = 'partial_dos.csv'

import pandas as pd
import csv
import os
data = pd.read_csv(input_file, sep=" ", header=None)
data = data.dropna(axis='columns',how='all')
#data.to_excel('out.xlsx', engine='xlsxwriter') 
data.to_csv('out.csv', sep=',', header=False, index=False)


fout = open (output_file,'w')
with open('out.csv') as in_file:
   reader = csv.reader(in_file)
   result = [[item for item in row if item != ''] for row in reader]

count = len(result[1])

for i in range(1,count+1):
    fout.write(str(i) + ",")
fout.write("\n")

for rlist in result:
    for r in rlist:
        fout.write(r + ",")
    fout.write("\n")
fout.close()
in_file.close()
os.remove('out.csv')
