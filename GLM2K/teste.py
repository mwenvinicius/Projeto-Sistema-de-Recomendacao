#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 10:50:51 2018

@author: julianaoc
"""

MS = [0,0,0,0,0,0,0,1,1,1]
PR = [1,3,2,5,4,7,6,8,9,10]
Score = [0.80,0.80,0.83,1,0.83,0.83,0.83,0.83,1.0,0.8]
Cost = [52,52,69,79,79,79,79,52,69,79]

#MatIn = [[(0,0,0) for x in range(9)] for x in range(3)]

MatIn = [[] for x in range(2)]

for i, item in enumerate(MS):
    MatIn[item].append((Score[i],Cost[i],PR[i]))
    

print(MatIn)


for i in range(len(MatIn)):    
    MatIn[i].sort(key=lambda x: x[1])
    
    
print(MatIn)    
    
for i, ms in enumerate(MatIn):
    j = 0
    while (j < (len(ms) - 1)):
        if (j < len(ms)-1):
            k = j + 1
            if (ms[k][1] >= ms[j][1] and ms[j][0] >= ms[k][0]):
                ms.remove(ms[k])
            else: j += 1    
                
print('Primeira Redução: ', MatIn)   

for i, ms in enumerate(MatIn):
    j = 0
    while (j < (len(ms) - 2) and  len(ms) >= 3):
        if (j < len(ms)-2):
            k = j + 1
            l = j + 2
            if ((ms[l][0] - ms[k][0])/(ms[l][1] - ms[k][1]) >= (ms[k][0] - ms[j][0])/(ms[k][1] - ms[j][1])):
                ms.remove(ms[k])
            else: j += 1    
                
print('Segunda Redução: ', MatIn)   