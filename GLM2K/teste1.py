#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 09:20:49 2019

@author: julianaoc
"""

listaLista = [[(0.25,(7,0.93,10)),(0.55,(12,0.93,10)),(0.89,26),(0.76,65)],[(0.47,12),(0.95,36)],[(0.59,8),(0.35,24),(0.71,40),(0.80,85)]]

for i, classe in enumerate(listaLista): 
    for j, item in enumerate(classe):
        print('i: ',i,' j: ',j,' item: ',item,'\n')