###############################################################################################
# Program to rearrange data -- all odd indexed values first and even indexed values in last
###############################################################################################
#
#
#     Required Input
#
input_file = "G0_POSCAR-original"
output_file = input_file+"_format1.txt"
#
#
###############################################################################################


import pandas
import math

#############################################
# Write only heading rows into output file

fdf = pandas.read_csv(input_file, header=None)
fdf = fdf.head(8)

data_file = open(output_file, "w")
for index, row in fdf.iterrows():
    data_file.write(row[0] + "\n")



###############################################
# Write all odd rows first 

df = pandas.read_csv(input_file, skiprows=8, header=None, sep='\s+')

rows=[]
columns = [0, 1, 2]
for index, row in df.iterrows():
    
    isEven = (index % 2) == 0
    #print(row[0], isEven)
    
    if not(isEven):
        rows.append(row)

# Write all even rown in the last
for index, row in df.iterrows():
    
    isEven = (index % 2) == 0
    #print(row[0], isEven)
    
    if isEven:
        rows.append(row)

# Create output file
df_out = pandas.DataFrame(rows, columns=columns)

for index, row in df_out.iterrows():
    
    data_file.write('%22.16f' % float(row[0])+ " " + '%22.16f' % float(row[1]) + " " + '%22.16f' % float(row[2]) + "\n")
data_file.close()















