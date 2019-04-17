#program to find total running time after every 500 time steps.
import pandas
import math

#start will remain same, length can be changed to get more or less records
input_file="out.txt"
start=1
length=14

#Iteration's sum after every 1000 steps. value 1000 can be replaced with some other value.
arr=[]
for x in range(0,length):
 arr.append((start+x)*500)
#arr1=start*30
#arr2=(start+1)*30
#arr3=(start+2)*30
#arr4=(start+3)*30
#arr5=(start+4)*30
#arr6=(start+5)*30

#arr=[210,240,270,300,330]
#arr=[arr1,arr2,arr3,arr4,arr5,arr6]

def read(n):
    df1 = pandas.read_csv(input_file, header=None, delimiter=r"\s+")
    df1 = df1.head(n)
    x = df1[3].values
    #print (x) 
    itemcount = 0
    sumofitems = 0
    for i in x:
        itemcount = itemcount + 1
        item = i
        item = i[:-1]
        #print (item)
        sumofitems = sumofitems + float(item)
    print ("No.ofSteps=",itemcount, "Time=", sumofitems)
    #print (sumofitems)
    

#read(arr[0])
#read(arr[1])
#read(arr[2])
#read(arr[3])
#read(arr[4])
#read(arr[5])

for x in range(0,length):
    read(arr[x])









