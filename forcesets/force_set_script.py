############################################################################
# Program to generate a FORCE_SET file
# This program takes three input 
#(1) no. of cases 
#(2) displacement file (disp.yaml)
#(3) outcar files 
# and prepare an output file FORCE_SET which contains total no. of atoms, displacement and position of atoms 
# 
#############################################################################
#
#
#          Required Input
#
cases = 2   # change this value acc. to requirements
#
#####################################Dont change any thing after this########
import os


atoms = []   # used to store no.of atoms for all cases 
disp_list=[] # used to store displacement for all cases


# function to create output file 
def createfile(filename):
    data_file = open(filename, "w")
    return data_file


# function to write data and next line character in file
def writefile(df, txt):
    df.write(str(txt)+"\n")


# function to read disp.yaml ---to find out no. of atoms and displacements.    
def readyaml():
    fh = open("disp.yaml")
    line = fh.readline()
    line = line.strip("\n")
    line = line.split(" ")  
    # first line contains total no. of atoms, read and store them in var natom      
    natom = line[2] 
    line = fh.readline()       # skip one line containing extra/unwanted text
    for i in range(cases):     # run this loop for each case
        line = fh.readline()   # this line contains atom for given case
        line = line.strip("\n")
        line = line.split(" ")
        l=[]
        for itr in line:       # skip all spaces from line 
            if itr != "":
                l.append(itr)
        
        atoms.append(l[2])     # store no. of atom for a given case in atoms array
        
        line = fh.readline()   # skip line  contains #direction heading
        line = fh.readline()   # skip line  contains direction values
        line = fh.readline()   # skip line  contains #displacement heading
        line = fh.readline()   # read displacement, contains displacement values
        line = line.split(" ")
    
        displacement = ""
        for j in range(len(line)-1): # skip spaces and extra characters from line
            if line[j] != '' and line[j] != ']' and line[j] != '[':
                
                displacement = displacement + line[j]      
        displacement = displacement.split(",")
        # store displacement for a given case in disp_list array
        disp_list.append([displacement[0], displacement[1], displacement[2]]) 
        
    return natom # return total no. of atoms



# read disp.yaml file, create output file
# write total no. of atoms, total no. of cases and a blank line in output file
natom = readyaml()
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
            itm_list=itm
        else:
            itm_list = itm_list +"  " + itm
    
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
