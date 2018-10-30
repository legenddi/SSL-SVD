from numpy import *  
import numpy as np
import pandas as pd
from math import *
from loaddata import *
#print(mydata)
#print(mydata[915,])
#print(mydata.shape)
x=np.corrcoef(mydata)*0.5+0.5

def jaccard(v1,v2):
    x=np.where(v1>0,1,0)
    #print(x)
    y=np.where(v2>0,1,0)
    #print(y)
    up=np.double(np.bitwise_and(x,y).sum())
   # print(up)
    down=np.double(np.bitwise_or(x,y).sum())
  #  print(down)
    d1=(up/down)
    return d1

def con(vectorv):
    b=0
#    y=(vectorv.tolist())[0]
    y=vectorv
    x=np.array(y)
    a=x[x>0].size
    sum1=sum(y)
    avg=sum1/a
    for i in range(len(x)):
        if x[i]>0:
          b=b+np.square(x[i]-avg)
          con=b/a
        else:
          continue

    return con

def Com(vectorv):
    b=0
   # y=(vectorv.tolist())[0]
    y=vectorv
    x=np.array(y)
    s=x[x>0].size
    for i in range(len(x)):
        if x[i]>0:
          #  z=((mydata.T)[i,].tolist())[0]
            z=(mydata.T)[i,]
            n=np.array(z)
            a=n[n>0].size
            sum1=np.sum(z)
            avg=sum1/a
            b=b+np.square(x[i]-avg)
        else:
            continue
    if b==0:
        com=0
    else:
        com=s/b

    return com

#活跃度
def liveness(vectorv):
   # y=(vectorv.tolist())[0]
    y=vectorv
    x=np.array(y)
    a=x[x>0].size
    if a>50:
        r=1
    else:
        r=a/50
    return r

#综合计算可信度
#cofidence=liveness(vectorv)*(Com(vectorv)+con(vectorv))



def matrixmeans(self):
    k=0
    s=np.sum(mydata)
    b=mydata.shape[0]
    for i in range(b):
      v1=mydata[i,]
#      y=(v1.tolist())[0]
#      x=np.array(y)
      x=np.array(v1)
      a=x[x>0].size
      k=k+a
#     print(x)
#      print(a)
    avg=s/k
    return avg
avgm=matrixmeans(mydata)
#print(avgm)



def Integrity(vectorv):
    y=vectorv
    x=np.array(y)
    a=x[x>0].size
    sum1=sum(y)
    avgb=sum1/a
    sum2=0
    sum3=0
    sum4=0
    for i in range(len(x)):
        if x[i]>0:
            #z=((mydata.T)[i,].tolist())[0]
            z=(mydata.T)[i,]
            n=np.array(z)
            a=n[n>0].size
            sum1=np.sum(z)
            avgi=sum1/a
            sum2=sum2+(x[i]-avgb)*(avgi-avgm)
            sum3=sum3+np.square(x[i]-avgb)
            sum4=sum4+np.square(avgi-avgm)
    if sum2==0:
      Inte=0;
    else:
      num=(np.sqrt(sum3))*(np.sqrt(sum4))
      Inte=sum2/num
    return Inte



if __name__ == "__main__":
    l=list()
    W=list()
    In=[]
    Co=[]
#    print(mydata.shape[0])
    a=mydata.shape[0]
    for i in range(a):
        v1=mydata[i,]
#  c=liveness(v1)*(Com(v1)+con(v1))
        c=liveness(v1)*(Com(v1)+con(v1))
        I=Integrity(v1)
        In.append(I)
        Co.append(c)
    for i in range(a):
        v1=mydata[i,]
        for j in range(a):
         if (mydata2[i,j]==0):  
            if (Co[j]<0.1 and In[j]<0 and x[i,j]<0.6) :   #step1:选取必不产生信任标签
          #  if (mydata2[i,j]==1):
                list1=[i+1,j+1,mydata2[i,j],Co[j],In[j],x[i,j]]
                v2=mydata[j,]
                J=jaccard(v1,v2)
          #     s=0.9*J+0.1*x[i,j]
                if J<0.5:
                 list1.append(J)
                #print(list1)
                 l.append(list1)
            else:
                list2= [i+1,j+1,mydata2[i,j],Co[j],In[j],x[i,j]]
                v2=mydata[j,]
                J=jaccard(v1,v2)
        #       s=0.9*J+0.1*x[i,j]
                list2.append(J)
                #print(list1)
                W.append(list2)           
    columns1=['trustor','trustee','trust lable','volatility','Integrity','Pearson','jaccard']
    test1=pd.DataFrame(columns=columns1,data=l)
    test1.to_csv('csv')    

    columns1=['trustor','trustee','trust lable','volatility','Integrity','Pearson','jaccard']
    test2=pd.DataFrame(columns=columns1,data=W)
    test2.to_csv('csv')    

