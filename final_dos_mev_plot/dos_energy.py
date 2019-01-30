############################################################################################################
# This code generates three files
# 1. It combines data from two different input files in file 1
# 2. It takes only even indexed rows from file 1 and write them to a new file, file 2
# 3. It takes first 31 rows from file 1 and after that only even indexed rows and write them in file 3
###########################################################################################################
# output files are in .txt and .xlsx format. 
###########################################################################################################
#
#
#                     Required Input Files
#
input_file1="1_RPDOS_W16_207_40_15_2_95_22.dat"
input_file2="1_W16_final-dos_Ei%3d300-130-30meV_dE%3d1.5-1.5-0.75meV_Ecut%3d207meV_Ec%3d95_22meV_W%3d1-0.txt"
no_of_lines = 320
output_file1= "1_W16_0.75meV"
output_file2= "2_W16_1.5meV"
output_file3= "3_W16_combined"
#
###########################################################################################################


import pandas
import math


df1 = pandas.read_csv(input_file1, header=None, delimiter=r"\s+")
df2 = pandas.read_csv(input_file2, header=None, delimiter=r"\s+")
df2 = df2.head(no_of_lines)


x = df1[0].values
y = df1[1].values
z = df2[2].values


# combine data from two different files and write in a new file
df_out = pandas.DataFrame(list(zip(x, y, z)))


data_file = open(output_file1+".txt", "w")
for index, row in df_out.iterrows():
    
    data_file.write('%26.22f' % float(row[0])+ " " + '%30.22f' % float(row[1]) + " " + '%30.22f' % float(row[2]) + "\n")
data_file.close()


#to save file in excel format
writer = pandas.ExcelWriter(output_file1+'.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df_out.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()






#read only even no. of rows from file


file= output_file1+".xlsx"
df = pandas.read_excel(file)

rows = []
columns = [0,1,2]

#print(df.columns)
x = df[0].values
for index, row in df.iterrows():
    #f,w = math.modf(row[0])
    isEven = (index % 2) == 0
    #print(row[0],f,w, isEven)
    if isEven:
        rows.append(row)

df_odd = pandas.DataFrame(rows, columns=columns)

data_file = open(output_file2+".txt", "w")
for index, row in df_odd.iterrows():
    
    data_file.write('%26.22f' % float(row[0])+ " " + '%30.22f' % float(row[1]) + " " + '%30.22f' % float(row[2]) + "\n")
data_file.close()


#to save file in excel format
writer = pandas.ExcelWriter(output_file2+'.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df_odd.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()



#read first 31 lines and then only even indexes

file= output_file1+".xlsx"
df = pandas.read_excel(file)

rows = []
columns = [0,1,2]

#print(df.columns)
x = df[0].values
for index, row in df.iterrows():
    if index < 31:
        rows.append(row)
    
for index, row in df.iterrows():
    if index >= 31 and (index%2)==0:
        rows.append(row)
    
df_all = pandas.DataFrame(rows, columns=columns)


data_file = open(output_file3+".txt", "w")
for index, row in df_all.iterrows():
    
    data_file.write('%26.22f' % float(row[0])+ " " + '%30.22f' % float(row[1]) + " " + '%30.22f' % float(row[2]) + "\n")
data_file.close()


#to save file in excel format
writer = pandas.ExcelWriter(output_file3+'.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df_all.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
