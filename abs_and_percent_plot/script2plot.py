###########################################
# This code assigns a head row 
###########################################
#   Required Input File
##########################################


input_file1 = '1-Total_DOS_66x66x66_Area=3.dat'
input_file2 = '2-B0_Di-vacancy_partial_dos_20_20_20.dat'

count = 0

#######################main
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import os


test = np.loadtxt(input_file1)
np.savetxt(input_file1+'.csv', test)

test2 = np.loadtxt(input_file2)
np.savetxt(input_file2+'.csv', test2)

#print (test[:,1])
df1 = pd.DataFrame(test)
df2 = pd.DataFrame(test2)
count = len(df2.columns)

################ subtraction only ############
#df2[1] = df1[1] - df2[1]
for i in range(1, count):
    df2[i] = df1[1] - df2[i]
df2.to_excel('subVal.xlsx', engine='xlsxwriter') 


######### absolute values ###############
sub_val= df2.applymap(abs)
sub_val.to_excel('absoluteVal.xlsx', engine='xlsxwriter')

############ percentage ####################
test2 = np.loadtxt(input_file2)
df3 = pd.DataFrame(test2)
count = len(df3.columns)


for i in range(1, count):
    df3[i] = 100 * abs(df1[1] - df3[i]) / df1[1] 

df3.to_excel('percentVal.xlsx', engine='xlsxwriter') 

################plot###################

os.mkdir("subplot")
dr = os.getcwd()
dr = dr + "/subplot"
os.chdir(dr)

for i in range(1, count):
    plt.figure(i)
    plt.title("B0_Di-vacancy_partial_dos")
    plt.xlabel("x")
    plt.ylabel("y- y" + str(i));
    plt.plot(df2[0], df2[i], '-g')
    plt.legend();
    plt.savefig(str(i) +'.png')
    plt.close()
os.chdir ("../")

################plot###################

os.mkdir("absplot")
dr = os.getcwd()
dr = dr + "/absplot"
os.chdir(dr)

for i in range(1, count):
    plt.figure(i)
    plt.title("B0_Di-vacancy_partial_dos")
    plt.xlabel("x")
    plt.ylabel("abs(y- y" + str(i) + ")");
    plt.plot(sub_val[0], sub_val[i], '-r')
    #plt.legend();
    plt.savefig(str(i) +'.png')
    plt.close()
os.chdir ("../")

################plot###################

os.mkdir("percentplot")
dr = os.getcwd()
dr = dr + "/percentplot"
os.chdir(dr)

for i in range(1, count):
    plt.figure(i)
    plt.title("B0_Di-vacancy_partial_dos")
    plt.xlabel("x")
    plt.ylabel("100 * (y- y" + str(i) + ") / y");
    plt.plot(df3[0], df3[i], '-b')
    #plt.legend();
    plt.savefig(str(i) +'.png')
    plt.close()
os.chdir ("../")
