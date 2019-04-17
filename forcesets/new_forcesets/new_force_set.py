############################################################################
# This program takes input (1) no. of cases (2) displacement file (disp.yaml)
# and (3) outcar fileS for all cases and prepare an output file FORCE_SET
# which contains total no. of atoms, displacement and position of atoms for
# all cases
#############################################################################

import os
import yaml

cases = 2   # change this value acc. to requirements
atoms = []   # store no.of atoms for all cases 
disp_list=[] # store displacement for all cases
natom = 2

# this function creates output file 
def createfile(filename):
    data_file = open(filename, "w")
    return data_file


# this function writes data and next line character in file
def writefile(df, txt):
    df.write(str(txt)+"\n")


# this function read disp.yaml to find out no. of atoms and displacements.    
def readyaml():

    with open("phonopy_disp.yaml") as f:
        data = yaml.load(f)

    for i in data['displacements']:
        disp_list.append(i['displacement'])
        atoms.append(i['atom'])




# read disp.yaml file, create output file
# write total no. of atoms, total no. of cases and a blank line in output file
readyaml()
df = createfile("FORCE_SETS")
writefile(df, natom)
writefile(df, cases)
writefile(df, "")


# for each case run this loop
# write no. of atoms for each case in file (from atoms array)
# write displacement for each case in file (from disp_list array)
for i in range(1, cases+1):
    writefile(df, atoms[i-1])
    itm_list=""
    for itm in disp_list[i-1]:
        
        if itm_list=="": # dont add space for the first time
            itm_list= str(itm)
        else:
            itm_list = itm_list +"  " + str(itm)

    writefile(df, itm_list)
    values=[]
    #goto folder 1 to access outcar file for case 1 (do this for all cases)
    path = os.getcwd()
    os.chdir(path +"/"+ str(i))
    f = open("OUTCAR")
    line=""

    # mention the start and end of lines, to read from outcar
    # start "POSITION"
    # end "total drift":
    while "POSITION" not in line:
        line = f.readline()

    line = f.readline()
    while "total drift:" not in line:
        line = f.readline()
        line = line.strip("\n")
        values.append(line)

    for j in range(len(values)-2): #skip two last characters from each line ie newline

        line = values[j].split(" ")
        tmp =[]
        for k in line:
            if k != "":
                tmp.append(k)
        writefile(df, '%10.6f' % float(tmp[3]) + " " + '%12.6f' % float(tmp[4]) + " " + '%12.6f' % float(tmp[5]))
    writefile(df, "")
    # go one level down, to the root folder
    os.chdir(path + "/" + str(i) + "/..")
                                                                                                                                                       

