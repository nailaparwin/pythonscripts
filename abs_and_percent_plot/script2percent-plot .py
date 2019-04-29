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


############ percentage ####################
test = np.loadtxt(input_file1)
test2 = np.loadtxt(input_file2)

filter_data_test1 = []
for row in test:
    if (row[0] >= 5 and row[0] < 50):
        filter_data_test1.append(row)

filter_data_test2 = []
for row in test2:
    if (row[0] >= 5 and row[0] < 50):
        filter_data_test2.append(row)

dt1 = pd.DataFrame(filter_data_test1)
dt2 = pd.DataFrame(filter_data_test2)

count = len(dt2.columns)


for i in range(1, count):
    dt2[i] = 100 * (dt1[1] - dt2[i]) / dt1[1]
dt2.to_excel('percentVals.xlsx', engine='xlsxwriter') 

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
    plt.plot(dt2[0], dt2[i], '-b')
    #plt.legend();
    plt.savefig(str(i) +'.png')
    plt.close()
os.chdir ("../")

