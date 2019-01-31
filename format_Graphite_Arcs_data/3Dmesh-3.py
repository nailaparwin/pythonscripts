################################################
#
# Program to organize data
#      Required Input
#
#################################################
# use one or more filenames here

files = ['graphite_vasp_2Dmesh_coh_300K-30meV-1ph.csv','graphite_vasp_2Dmesh_coh_300K-30meV-mph.csv']




#########################################
# Final version of code 
# To format data for making plots
# 2nd update for -1 values
# 3rd update to remove first column auto
# 4th update to run for multiple files
########################################
import csv
import openpyxl
import string
import sys




# we will use this list to create multiple sub lists of self.totals 
class ThreeDmesh(object):



    def __init__(self, filename):
        self.filename = filename
        self.resultfile=""
        self.Q = []
        self.deltaE = []
        self.totals = [] #self.totals is three column list which contains all data Q, self.deltaE, total
        self.depth = []
            
    def writef(self):
        
        # create a csv output file
        fh = open(self.resultfile +".csv", "w")

        #insert a new fieldname because self.Q list does not contain a col for self.deltaE values(the header column)
        firstcol = 0
        self.Q[:0]=[firstcol]  #technique to appends an item in the beginning of list
        fieldnames =  self.Q
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
                

        for v in range(len(self.deltaE)):
            #writer.writerow({self.Q[0]:self.deltaE[v],self.Q[1]:self.depth[0][v], self.Q[2]:self.depth[1][v], .....})
            #instead of writing a long object we can create a dynamic object that creates its all properties at run time
            # first col contains a different property self.deltaE so it is defined outside loop
            # rest of the properties are defined in a single loop becasue all other lists have same name "self.depth"
            #outer loop should run equal to the no. of total rows.
            obj = {}
            obj[self.Q[0]]=self.deltaE[v]
            for num in range(len(self.Q)-1):
          
                obj[self.Q[num+1]]= self.depth[num][v]
             
            writer.writerow(obj)

    #it iterate over each file one by one
    def call_runConverter(self):
        no_of_files_to_convert = len(self.filenames)
        #print(no_of_files_to_convert)
        for x in range(no_of_files_to_convert):
            self.runConverter(x)
            self.writef()
            self.csv_to_xlsx()

    #def runConverter(self,x):

    # main procedure #
    # The main logic is that "totals" contains all data of Q, deltaE and totals. "Q" contains only distinct values of Q.
    # "deltaE" cotains only distinct values of deltaE. while "depth" contains sub lists of totals for each value of Q 
    def runConverter(self):
        #print ("in runConverter")
        #filename = self.filenames[x]
        filename = self.filename
        self.resultfile = filename
        Q_count = 1
        final_Q_count = 0
        with open(filename ,"r") as f:  
            reader = csv.reader(f, delimiter=',')     
            for line in reader:
                #file contains many blank cells. to ignore all blank cells and pick only data columns       
                ignore_spaces_list = []
                if len(line)!=0:
                    if line[0].startswith(' #'):
                        #ignore
                        a = "comment"
                    else:
                        for i in line:
                            if len(i) != 0:
                                tmp = i.strip()
                                if tmp[0].isdigit():
                                    ignore_spaces_list.append(float(i))

############ addition here for -1 values ################################
                                elif tmp[0] == '-':
                                    ignore_spaces_list.append(float(i))
#############################

                        #print("igl ", ignore_spaces_list)
                        if len(ignore_spaces_list) > 0:
                            self.totals.append(ignore_spaces_list)
                        flag = True
                        #append new values of Q in list only if it already not exists
                        if len(ignore_spaces_list) > 0:
                            for j in self.Q:
                                if j == ignore_spaces_list[0]:
                                    Q_count = Q_count + 1 # to count total no. of similar Q values
                                    flag = False
                            if flag == True:
                                final_Q_count = Q_count # Q_count will change in each iteration so grap its value in a new variable 
                                self.Q.append(ignore_spaces_list[0]) # if value is unique, add it to the list
                                
                                Q_count = 1
                                #print("final_Q_count", final_Q_count) #just to make sure that all lists have equal lenghts.


                        flag = True
 
                       #append new values of self.deltaE in list only if it already not exists
                        if len(ignore_spaces_list) > 0:
                            for j in self.deltaE:
                                if j == ignore_spaces_list[1]:                                   
                                    flag = False
                            if flag == True:                               
                                self.deltaE.append(ignore_spaces_list[1]) # add if a new value of deltaE
                                
                                
                                

        #print all self.Q values
        #for itr in self.Q:
            #print(itr)
        #print all self.deltaE values
        #for itr in self.deltaE:
            #print(itr)
        #print (len(self.deltaE))
        #for itr in self.totals:
            #print(itr)
        



        #create multiple arrays inside self.depth array. one for each value of Q. it will hold total values. populate each self.depth sub array 
        # with the help of self.totals array. lenght of each sub array depends upon the length of self.deltaE values.
        count = 0
        for i in range(len(self.Q)):
            self.depth.append([])
            #print (len(self.deltaE))
            for j in range(len(self.deltaE)):
                self.depth[i].append(self.totals[count][2])
                count = count + 1
        #for itr in range(len(self.depth)):
            #print(self.depth[itr],"\n")
                



    def csv_to_txt(self):
        inFile= open(resultfile, 'r')
        outFile= open("out.txt", 'w')


        for line in inFile:
            
            outFile.write(line)
            outFile.write('\n')

        outFile.close()
        inFile.close()



    def csv_to_xlsx(self):
        f = open(self.resultfile+".csv")
        wb = openpyxl.Workbook()
        ws = wb.active
        reader = csv.reader(f, delimiter=',')
        for i in reader:
            try:
                i[0:] = [float(x) for x in i[0:]]
                ws.append(i)
            except ValueError:
                ws.append(i)

        f.close()
        wb.save(self.resultfile + ".xlsx")
        #os.remove(filename)
  


if __name__ == "__main__":

 
    #files = ['graphite_vasp_2Dmesh_coh_300K-130meV-mph.csv']
    for allfiles in range(len(files)):
        obj = ThreeDmesh(files[allfiles])
        #obj.call_runConverter()
        obj.runConverter()
        obj.writef()
        obj.csv_to_xlsx()
        #obj.csv_to_txt()

