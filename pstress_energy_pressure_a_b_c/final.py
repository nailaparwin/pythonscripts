
####################################################################
# code to extract last entry of length of vectors, energy  and     #
# pressure from all excel files. It will create a new excel file   #
# pstress_0_100.xlsx. This file is the final output                #
####################################################################



import os
import pandas as pd
import xlsxwriter


# create an excel file -------- final output
writer = pd.ExcelWriter('pstress_0_100.xlsx', engine='xlsxwriter')

# create a data set, provide header of each column for final output file
df_w = pd.DataFrame(columns=('PSTRESS', 'Energy', 'Pressure','a','b','c'))

#y loop runs for each file, file names end with 0,5,10,15,20,...100
# so we are running a loop that will multiply each number with 5 to create 
# file names according to pstress values
for y in range(21):
    filename ="files_" + str(y*5)

    # read excel file
    df_r = pd.read_excel(filename + '.xlsx')
    # consider last row only 
    df_new = df_r.iloc[-1,:]
    
    # appends a new line in data set
    df_w = df_w.append([{'PSTRESS': y*5,'Energy':df_new['Energy'],'Pressure':df_new['Pressure'],'a':df_new['a'],'b':df_new['b'],'c':df_new['c']}])

 

# Convert the dataframe to an XlsxWriter Excel object.
df_w.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()






