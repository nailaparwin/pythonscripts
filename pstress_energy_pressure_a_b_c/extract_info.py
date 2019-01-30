####################################################################
# code to extract length of vectors, total energy (TOTEN), and     #
# external pressure from the OUTCAR files.                         #
####################################################################

# There are multiple folders. code will go through each folder one by
# one. read the outcar file and produce an excel sheet for each outcar
# file. the name of excel sheet will be same as the name of folder.
#####################################################################

import os
import pandas as pd
import xlsxwriter


x=0
#y loop runs for each folder, folder names end with 0,5,10,15,20,...100
# so we are running a loop that will multiply each number with 5 except the first one
# because the first folder is zero
for y in range(21):
    if y == 0:
        folder = "files_" + str(y)
    else:
        folder ="files_" + str(y*5)

    # go inside each folder and read outcar file
    print(os.getcwd()," ",folder)
    os.chdir(folder)
    searchfile = open("OUTCAR", "r")

    # flag to indicate
    leng_flag='false'

    # holds the maximum number of iteration. for 1(1) 1(2) 1(3)...1(15) it will consider 1(15) only.
    maxnum = ""

    # holds the total enery
    toten = ""

    # length of vectors
    a = ""
    b = ""
    c = ""

    # holds external pressure
    pressure = ""

    # holds the unit of pressure. no need
    unit = ""

    #create a new excel file, the name of file is same as the name of folder
    writer = pd.ExcelWriter(folder + '.xlsx', engine='xlsxwriter')

    # create a data set, provide header of each column
    df = pd.DataFrame(columns=('Iteration', 'Energy', 'Pressure','a','b','c'))

    # screen output
    print ("Iterator TotalEnergy Length of Vectors Pressure")

    # iterate each line of outcar file
    for line in searchfile:

        # extracts the number of current iteration
        if "Iteration" in line: 
            x = line.split(" ")
            if x[6] != "":
                maxnum = int(x[6][:-1])
            else:
                #print(x)
                maxnum = int(x[7][:-1])
        
        # finds the total free energy. if free energy found append a line in data set, because if we see the order of required info
        # this information is last among all. first we will get pressure then lenght of vectors and then total energy. so print after this.
        elif "free  energy   TOTEN" in line:
            ev = line.split(" ")
            #print(ev)
            if ev[15] != "":
                toten = ev[15]
            else:
                toten = ev[16]
            #print(ev)
            #print (maxnum , toten)
            print (maxnum, toten, a, b, c, pressure)

            # appends a new line in data set
            df = df.append([{'Iteration':maxnum,'Energy':toten,'Pressure':pressure,'a':a,'b':b,'c':c}])

        # finds the time taken to run the complete iteration
        # but currently it is not added in excel file.
        elif "Total CPU time used (sec):" in line:   
            ev = line.split(" ")
            print("Total CPU time used (sec): ", ev[-1])

        # finds the length of vectors in outcar file. IN outcar file length of vector is given on the next line after the text "length of vector"
        # appears so in this iteration we turn the flag true. and in next iteration if flag is true reads the values and make it false.
        elif "length of vectors" in line:   
            leng_flag='true'
        elif leng_flag == 'true':
            leng_flag = 'false'
            ev = line.split(" ")
            a = ev[5]
            b = ev[7]
            c = ev[9]
            
            #print ("length of vectors =", ev[5], ev[7], ev[9])

        # finds the external pressure
        elif "external pressure" in line:
            ev = line.split("=")
            p_str = ev[1]
            parse = p_str.split("kB")
            pressure = parse[0]
        
            #print ("external pressure = ", pressure)
            

    # close excel file        
    searchfile.close()

    # go outside the directory
    os.chdir("../")

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

