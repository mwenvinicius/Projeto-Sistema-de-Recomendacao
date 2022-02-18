#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 15:28:20 2018

@author: julianaoc
"""

def greedyKnapSack(classesItems,costAPP,avaAPP,rtAPP):
    r = []
    z = []
    cbarra = costAPP
   
    for classe in classesItems:
        cbarra -= classe[0][1]
        
    
    if (cbarra > 0):
            for i, classe in enumerate(classesItems): 
                #print('i:', i,'\n\n')
                #print('Tam Classe: ',len(classe),'\n\n')
                for j, item in enumerate(classe):
                    if (j==0):
                        auxp = item[0]
                        auxw = item[1]
                    else: 
                        if (item[0]!= auxp and item[1] != auxw):
                            pbarra = item[0] - auxp
                            wbarra = item[1] - auxw
                            #print('pbarra: ',pbarra,'\n')
                            #print('wbarra: ',wbarra,'\n')
                            e = pbarra/float(wbarra)
                            r.append((i,j,pbarra,wbarra,e,item[2],item[3]))
                            auxp = item[0]
                            auxw = item[1]
      
                        
            r.sort(key=lambda x: x[4], reverse=True)
            sol = []
            
            print('R = ',r,'\n\n')   
            #print('cbarra = ',cbarra,'\n\n')   
            for elem in r:
                if (cbarra >= elem[3]):
                    cbarra -= elem[3]
                    #print('cbarra = ',cbarra,'\n\n')   
                    sol.append((elem[0],elem[1],elem[5],elem[6]))
                else: break
        
            z = []
            for i, classe in enumerate(classesItems):
                z.append((i,1,classe[0][2],classe[0][3],classe[0][0]))
            
            
            print('Sol = ',sol,'\n\n') 
            
            print('Z1 = ',z,'\n\n') 
            
            for itemS in sol:
                for itemZ in z:
                    if(itemS[0] == itemZ[0]):
                        z.remove(itemZ)
                        #print('Info: ',classesItems[itemS[0]][itemS[1]][0],'\n\n')
                        z.append((itemS[0],itemS[1],itemS[2],itemS[3],classesItems[itemS[0]][itemS[1]][0]))
                        
            print('Z2 = ',z,'\n')               
            result = 0
            if (len(z) > 0):
                for itemZ in z:
                    result += itemZ[4]
                    
    else: result = 0 

    return (result,z,cbarra)      
            

#classesItems = [[(25,7),(55,12),(76,26),(89,65)],[(47,12),(95,36)],[(35,8),(59,24),(71,40),(80,85)]]    

costAPP = 100
avaAPP = 0.80
rtAPP = 20
#classesItems = [[(25,7),(55,12),(89,35),(76,65)],[(47,12),(95,36)],[(35,8),(59,24),(71,40),(80,85)]]        
    
#classesItems = [[(0.25,7),(0.55,12),(0.89,26),(0.76,65)],[(0.47,12),(0.95,36)],[(0.35,8),(0.59,24),(0.71,40),(0.80,85)]]        
    
#classesItems = [[(0.25,(7,0.93,10)),(0.55,(12,0.93,10)),(0.89,26),(0.76,65)],[(0.47,12),(0.95,36)],[(0.59,8),(0.35,24),(0.71,40),(0.80,85)]]        

posMS = [3,7,11]

MS = [0,0,0,0,1,1,1,1,2,2,2,2]        
PR = ['P1','P2','P3','P4','P1','P2','P3','P4','P1','P2','P3','P4']
#Score = [0,0.25,0.66,0.69,0.42,0.36,0.75,0.38,0.31,0.22,0.75,0.71,0.38]
#Requirements = [(0,0.80,20),(15,0.83,5),(20,0.87,1),(25,0.90,2),(19,0.85,3),(26,0.88,5),(30,0.92,1),(23,0.85,3),(18,0.83,4),(20,0.87,4),(30,0.98,2),(27,0.96,2),(12,0.85,2)]


#Score = [0,0.25,0.66,0.69,0.42,0.36,0.75,0.38,0.31,0.23,0.75,0.79,0.38]
#Requirements = [(0,0.80,20),(15,0.83,5),(20,0.87,1),(25,0.90,2),(19,0.85,3),(26,0.88,5),(30,0.92,1),(23,0.85,3),(18,0.83,4),(23,0.87,4),(31,0.98,2),(25,0.96,2),(18,0.85,2)]


Score = [0.25,0.66,0.69,0.42,0.36,0.75,0.38,0.31,0.24,0.38,0.63,0.37]
Requirements = [(15,0.83,5),(20,0.87,1),(25,0.90,2),(19,0.85,3),(26,0.88,5),(30,0.92,1),(23,0.85,3),(18,0.83,4),(23,0.87,8),(31,0.98,6),(25,0.92,2),(18,0.85,5)]



#Score = [0.77,0.166,0.53,0.52,0.28,0.88,0.49,0.21,0.21,0.64,0.30,0.65]
#Requirements = [(25,0.90,2),(20,0.80,5),(30,0.87,1),(15,0.85,3),(30,0.88,5),(24,0.92,1),(18,0.85,3),(23,0.83,4),(27,0.87,4),(19,0.98,6),(20,0.85,3),(12,0.89,2)]



MatIn = [[] for x in range(len(posMS))]
                
                
for j, item in enumerate(MS):
    MatIn[item].append((Score[j],Requirements[j][0],Requirements[j][1],Requirements[j][2],PR[j]))
 
for k in range(len(MatIn)):    
    MatIn[k].sort(key=lambda x: x[1])

MatAll = MatIn

print('MatIn1: ',MatIn,'\n')

for i1, ms in enumerate(MatIn):
    j = 0
    while (j < (len(ms) - 1)):
        if (j < len(ms)-1):
            k = j + 1
            if (ms[k][1] >= ms[j][1] and ms[j][0] >= ms[k][0]):
                ms.remove(ms[k])
            else: j += 1    
                

for i1, ms in enumerate(MatIn):
    j = 0
    while (j < (len(ms) - 2) and  len(ms) >= 3):
        if (j < len(ms)-2):
            k = j + 1
            l = j + 2
            if(ms[j][1] < ms[k][1] and ms[k][1] < ms[l][1] and ms[j][0] < ms[k][0] and ms[k][0] < ms[l][0]):
                if ((ms[l][0] - ms[k][0])/(ms[l][1] - ms[k][1]) >= (ms[k][0] - ms[j][0])/(ms[k][1] - ms[j][1])):
                    ms.remove(ms[k])
                else: j += 1
            else: j += 1    

print('MatIn2: ',MatIn,'\n')

(ScTotal,DataList,Change) = greedyKnapSack(MatIn,costAPP,avaAPP,rtAPP)


print('Score: ',ScTotal,'\n')
print(' DataList: ',DataList,'\n')
print(' Change: ',Change,'\n')
