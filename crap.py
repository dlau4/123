#Genetic Algorithm - Lisa Benison, Dennis Lau

import random, heapq
import numpy as np

#opens files and sets initial values - taken from David Bassen's PNN
execfile('in_out_csv.py') # creates "csv" object
execfile('pnn_bassen_v1_3t.py') # defines pnn class
case0 = np.array(csv.nestedToFlt(csv.In('case0.csv')))
case1 = np.array(csv.nestedToFlt(csv.In('case1.csv')))
total = np.array(csv.nestedToFlt(csv.In('totaldat.csv')))
gt = csv.listToFlt(sum(csv.In('resp.csv'),[]))
h0 = 58.0/102
h1 = 44.0/102

#created random chromosomes and deletes corresponding sigmas&features
def GA(case0,case1,total):
  x=0
  length=len(case0[0])-1
  totalFeat=len(case0[0])
  listBinFeat=[]
  sigmas = [ 0.1829679 ,  0.19631946,  0.22316691,  0.12173029,  0.10264953,
      0.14917592,  0.1608155 ,  0.22299027,  0.10591388 ]
  #randomly generates binary feature
  while x<totalFeat:
    binDel= random.randrange(0,2,1)
    listBinFeat.insert(0,binDel)
    x+=1
    #print  binDel
    if binDel==0:
      #print "the column that gets deleted",length
      case0=np.delete(case0,(length),1)
      case1=np.delete(case1,(length),1)
      total=np.delete(total,(length),1)
      del sigmas[length]
    length=length-1
  p = pnn(case0,case1,sigmas,h0,h1,total)
  result = p.classify()
  binary = [int(round(x)) for x in result]
  accuracy=getAccuracy(binary)
  return listBinFeat,accuracy

def getAccuracy(binary):
  count=0
  for i in range(len(binary)):
    if binary[i]==gt[i]:
      count=count+1
  accuracy = (count/float(len(binary)))*100
  return accuracy

  
#attempt at selection round two - missing random binary feature
def GAPart2(loop,case0,case1,total):
  loop.reverse()
  #print loop
  length=len(case0[0])-1
  totalFeat=len(case0[0])
  sigmas = [ 0.1829679 ,  0.19631946,  0.22316691,  0.12173029,  0.10264953,
      0.14917592,  0.1608155 ,  0.22299027,  0.10591388 ]
  #for loop in listBin:
   # print loop
  for x in loop:
      #print x
      if x==0:
        #print "the column that gets deleted",length
        case1=np.delete(case1,(length),1)
        case0=np.delete(case0,(length),1)
        total=np.delete(total,(length),1)
        del sigmas[length]
      length=length-1
  p = pnn(case0,case1,sigmas,h0,h1,total)
  result = p.classify()
  binary = [int(round(x)) for x in result]
  #accuracy 
  loop.reverse()
  accuracy=getAccuracy(binary)
  return accuracy

#crossover at random index on list (not a string)
def singleCrossOver(string1,string2):
  cut=random.randrange(1,len(string1)-1)
  part1=string1[0:cut]
  part2=string2[cut:]
  part12= part1+part2
  part3=string2[0:cut]
  part4=string1[cut:]
  part34= part3+part4
  return part12, part34


def main():
  acc=[]
  listBin=[]
  
  for loop in range(5):
    output=GA(case0,case1,total)
    acc.append(output[1])
    listBin.append(output[0])
  #print acc
  #print listBin
  max2= heapq.nlargest(2,acc)
  crossover=singleCrossOver(listBin[acc.index(max2[0])],listBin[acc.index(max2[1])])
  for delete in range(2):
    randomNum=random.randrange(0,len(acc),1)
    listBin.pop(randomNum)
    acc.pop(randomNum)
  listBin.extend(crossover)
  print listBin
  for loop in crossover:
    acc.append(GAPart2(loop,case0,case1,total))
  print acc







main()


