#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:23:13 2018

@author: julianaoc
"""


from unicodedata import name
from flask import Flask
#from flask import jsonify

#from random import randint

import time
#import timeit
import json
import itertools

import criaJSON

#from collections import Counter

app = Flask(__name__)


prvd=['./JSON-ApproachGKP-7GG/ProvidersGKP50-10.json']

#prvd=['./JSON-ApproachGKP-7GG/ProvidersGKP50-10.json']

linksPrvd=['./JSON-ApproachGKP-7GG/linksProviders50.json']


application = [
    './JSON-ApproachGKP-7GG/Application1-ability.json']
    #'./JSON-ApproachGKP-7GG/Application2-ability.json',
    # './JSON-ApproachGKP-7GG/Application3-ability.json',
    # './JSON-ApproachGKP-7GG/Application4-ability.json',
    # './JSON-ApproachGKP-7GG/Application5-ability.json',
    # './JSON-ApproachGKP-7GG/Application1-rt.json',
    # './JSON-ApproachGKP-7GG/Application2-rt.json',
    # './JSON-ApproachGKP-7GG/Application3-rt.json',
    # './JSON-ApproachGKP-7GG/Application4-rt.json',
    # './JSON-ApproachGKP-7GG/Application5-rt.json',
    # './JSON-ApproachGKP-7GG/Application1-cost.json',
    # './JSON-ApproachGKP-7GG/Application2-cost.json',
    # './JSON-ApproachGKP-7GG/Application3-cost.json',
    # './JSON-ApproachGKP-7GG/Application4-cost.json',
    # './JSON-ApproachGKP-7GG/Application5-cost.json',
    # './JSON-ApproachGKP-7GG/Application1-acr.json'
    # './JSON-ApproachGKP-7GG/Application2-acr.json',
    # './JSON-ApproachGKP-7GG/Application3-acr.json',
    # './JSON-ApproachGKP-7GG/Application4-acr.json',
    # './JSON-ApproachGKP-7GG/Application5-acr.json'
   # ]

#application = ['./JSON-ApproachGKP-7GG/Application1-cost.json']
#application = ['./JSON-ApproachGKP-7GG/Application1-cost.json','./JSON-ApproachGKP-7GG/Application2-cost.json','./JSON-ApproachGKP-7GG/Application3-cost.json','./JSON-ApproachGKP-7GG/Application4-cost.json','./JSON-ApproachGKP-7GG/Application5-cost.json']
#application = ['./JSON-ApproachGKP-7GG/Application4-ability.json','./JSON-ApproachGKP-7GG/Application5-ability.json','./JSON-ApproachGKP-7GG/Application2-rt.json','./JSON-ApproachGKP-7GG/Application2-cost.json','./JSON-ApproachGKP-7GG/Application4-cost.json','./JSON-ApproachGKP-7GG/Application5-acr.json']

#application = ['./JSON-ApproachGKP-7GG/Application1-cost.json','./JSON-ApproachGKP-7GG/Application2-cost.json','./JSON-ApproachGKP-7GG/Application3-cost.json','./JSON-ApproachGKP-7GG/Application4-cost.json','./JSON-ApproachGKP-7GG/Application5-cost.json','./JSON-ApproachGKP-7GG/Application1-acr.json','./JSON-ApproachGKP-7GG/Application2-acr.json','./JSON-ApproachGKP-7GG/Application3-acr.json','./JSON-ApproachGKP-7GG/Application4-acr.json','./JSON-ApproachGKP-7GG/Application5-acr.json']
interationApp=[
    './JSON-ApproachGKP-7GG/APP1-iterations-1.json',
    './JSON-ApproachGKP-7GG/APP2-iterations-1.json',
    './JSON-ApproachGKP-7GG/APP3-iterations-1.json',
    './JSON-ApproachGKP-7GG/APP4-iterations-1.json',
    './JSON-ApproachGKP-7GG/APP5-iterations-1.json'
    ]


##################################### METODOS JSON PARA PROVIDERS  e APPLICATIONS ##################################################



#### Conta o número de iterações até encontrar uma resposta
count = 0

####### Listas de informacoes
listaTeste = []
listaCandGeral = []
listaCandEsp = []

##########################
def search(linkOut,linkIn,linkPr):
    if (linkOut == linkIn):
        linkCost = 0
        linkAva = 1
        linkDelay = 0
    else:    
        for link in linkPr:
            if (link['out'] == linkOut and link['in'] == linkIn):
                linkCost = link['cost']
                linkAva = link['availability']/100
                linkDelay = link['delay']
    return (linkCost,linkAva,linkDelay)
  
    
def checkResult(solution, costAPP, avaAPP, rtAPP,dataLinks):
  
  cost = 0  
  ava = 1
  rt = 0
  result = 0

  for j,item in enumerate(solution):
    result += item[6]
    cost += item[2]
    ava *= item[3]
    rt += item[4]
    if (j < len(solution)-1):
        (linkCost,linkAva,linkDelay) = search(item[5],solution[j+1][5],dataLinks)
        cost += linkCost
        ava *= linkAva
        rt += linkDelay
  
 
  
  #if (result > costAPP or ava < avaAPP/100 or rt > rtAPP):
  #  result = 0    
              
  return (result,cost,ava,rt)             



def calcAva(z):
    ava = 1
    for item in z:
        ava *= item[3]
    
    return ava    

def calcRT(z):
    rt = 0
    
    for item in z:
        rt += item[4]
    
    return rt


######Greedy Algorithm

def greedyKnapSack(classesItems, costAPP,avaAPP,rtAPP,dataLinks):
    r = []
    z = []
    #cost = 0
    cbarra = costAPP
   
    for classe in classesItems:
        cbarra -= classe[0][1]
        
    
    if (cbarra > 0):
            for i, classe in enumerate(classesItems): 
                for j, item in enumerate(classe):
                    if (j==0):
                        auxp = item[0]
                        auxw = item[1]
                    else: 
                        if (item[0]!= auxp and item[1] != auxw):
                            pbarra = item[0] - auxp
                            wbarra = item[1] - auxw
                            e = pbarra/float(wbarra)
                            r.append((i,j,pbarra,wbarra,e,item[1],item[2],item[3],item[4]))
                            auxp = item[0]
                            auxw = item[1]
      
                        
            r.sort(key=lambda x: x[4], reverse=True)
            sol = []
              
            for elem in r:
                if (cbarra >= elem[3]):
                    cbarra -= elem[3]
                    sol.append((elem[0],elem[1],elem[5],elem[6],elem[7],elem[8]))
                else: break
        
            z = []
            for i, classe in enumerate(classesItems):
                z.append((i,1,classe[0][1],classe[0][2],classe[0][3],classe[0][4],classe[0][0]))
            
        
            
            for itemS in sol:
                for itemZ in z:
                    ava = calcAva(z)
                    rt = calcRT(z)
                    if(itemS[0] == itemZ[0]):
                        aux = [x for x in z]
                        aux.remove(itemZ)
                        aux.insert(itemZ[0],(itemS[0],itemS[1],itemS[2],itemS[3],itemS[4],itemS[5],classesItems[itemS[0]][itemS[1]][0]))
                        avaAux = calcAva(aux)
                        rtAux = calcRT(aux)
                        
                        if (avaAux >= ava and rtAux <= rt):
                            z.remove(itemZ)
                            z.insert(itemZ[0],(itemS[0],itemS[1],itemS[2],itemS[3],itemS[4],itemS[5],classesItems[itemS[0]][itemS[1]][0]))
                            ava = avaAux
                            rt = rtAux
                    
                    
            result = 0
            if (len(z) > 0):
                (result,cost,ava,rt) = checkResult(z, costAPP, avaAPP, rtAPP,dataLinks)
                
        
                 
    else: result = 0 

     
    return (result,z,cost,ava,rt,cbarra) 

#################### OS 3 métodos a seguir estão relacionados com a descoberta de serviços candidatos


##### Este método verifica se um serviço do provedor atende os requisitos funcionais de um serviçode um microserviço
##### Até o momento verificamos apenas requsitos funcionais relacionados a serviços de inst6ancias de máquinas virtuais    
    
def minCapabilities(capabilitiesSr,capabilitiesPr):
   
    if (not capabilitiesPr and not capabilitiesSr):
        adequate = True
    else:
        #print(capabilitiesSr,'\n',capabilitiesPr)
        if (capabilitiesPr[0]['CPU'] >= capabilitiesSr[0]['CPU'] and capabilitiesPr[0]['Core'] >= capabilitiesSr[0]['Core'] and capabilitiesPr[0]['RAM'] >= capabilitiesSr[0]['RAM'] and capabilitiesPr[0]['HD'] >= capabilitiesSr[0]['HD']):
            adequate = True
        else: adequate = False
    
    return adequate

######## Este método descobri quais serviços de uma classe de um provedor atedem os requesitos funcionais de um serviço


def discovery(service,provider):
    lista = []
    for pr in provider['servicesClass']:
       if (service['nameCl'] == pr['nameCl']):
           for srPr in pr['services']:
               if (service['functionality'] == srPr['functionality']):
                   if (minCapabilities(service['capabilities'], srPr['capabilities'])):
                           lista.append(srPr)
                        
    return lista

##### Retorna a lista de serviços candidatos em todos os provedores para hospedar um microserviço

@app.route('/apps/app/<nameApp>/microservices/servicoscandidatos',methods=['GET'])
def servicosCandidatosMS(microservice,dataPrvd):
   candidatesPrSr = []
  
   
   listaTeste = []
   for pr in dataPrvd:
       candidateSr = []
       for sr in microservice['services']: 
           discovList = discovery(sr,pr)
           if (discovList != [{}] and discovList != []):
               candidateSr.append((sr['nameSr'],discovList))
           else: 
               candidateSr.clear()
               break
         
       if (candidateSr != []):
           total = 0
           qtdALlSerPrvd.append((pr['provider'],microservice['nameMS'], len(candidateSr)))
           for listaSr in candidateSr:
               total += len(listaSr)
           listaTeste.append((pr['provider'], total))
           candidatesPrSr.append((pr['provider'],microservice['nameMS'],candidateSr))     
   #print('Candidates: ',candidatesPrSr,'\n\n')    
   return (candidatesPrSr,listaTeste)



#################################

###### Dado uma lista de serviços candidatos e um requerimento, este método encontra o valor máximo do requerimento dado  na lista de serviços candidatos   
###### Requerimentos = avauilability e cost    

def maximum(srL,req):
    reqMax = 0
    for sr in srL:
        if (sr['userRequirements'][0][req] > reqMax):
            reqMax = sr['userRequirements'][0][req]
    
    return reqMax        
    
###### Dado uma lista de serviços candidatos e um requerimento, este método encontra o valor mínimo do requerimento dado  na lista de serviços candidatos   
###### Requerimentos = avauilability e cost        

def minimum(srL,req):
    reqMin = 100000
    for sr in srL:
        if (sr['userRequirements'][0][req] < reqMin):
            reqMin = sr['userRequirements'][0][req]
            
    return reqMin        


###### Dado uma lista de serviços candidatos e um requerimento, este método encontra o valor máximo do requerimento dado  na lista de serviços candidatos   
###### Requerimento = responseTime = delay + executionTime    

def maximumRespTime(srL,req1,req2):
    reqMax = 0
    for sr in srL:
        responseTime = sr['userRequirements'][0][req1] + sr['userRequirements'][0][req2]
        if (responseTime > reqMax):
            reqMax = responseTime
    
    return reqMax        
    
###### Dado uma lista de serviços candidatos e um requerimento, este método encontra o valor mínimo do requerimento dado  na lista de serviços candidatos   
###### Requerimento = responseTime = delay + executionTime       

def minimumRespTime(srL,req1,req2):
    reqMin = 10000
    for sr in srL:
        responseTime = sr['userRequirements'][0][req1] + sr['userRequirements'][0][req2]
        if ( responseTime < reqMin):
            reqMin =  responseTime

    return reqMin

######################### Corresponde a Scaling Phase do algoritmo SAW#########
#### Os valores dos requerimentos são normalizados. Os requerimentos availability e cost são positivos (quanto maior, maior a qualidade). 
#### O responseTime é negativo(quanto maior menor a qualidade)    

def saw1(adqSrlist):
    vAllSr = []
   
    for srL in adqSrlist:
        aRqMax = maximum(srL[1],'availability')
        aRqMin = minimum(srL[1],'availability')
        
        rtRqMax = maximumRespTime(srL[1],'executionTime','delay')
        rtRqMin = minimumRespTime(srL[1],'executionTime','delay')
        
        cRqMax = maximum(srL[1],'cost')
        cRqMin = minimum(srL[1],'cost')
        
        vSr = []
        for sr in srL[1]:
            if (aRqMax == aRqMin):
                aSr = 1.0
            else: aSr = round((sr['userRequirements'][0]['availability'] - aRqMin) / (aRqMax - aRqMin),3)
            
            if (rtRqMax == rtRqMin):
                rtSr = 1.0
            else: rtSr = round((rtRqMax - (sr['userRequirements'][0]['executionTime'] + sr['userRequirements'][0]['delay'])) / (rtRqMax - rtRqMin),3)
            
            if (cRqMax == cRqMin):
                cSr = 1.0
            else: cSr = round((sr['userRequirements'][0]['cost'] - cRqMin) / (cRqMax - cRqMin),3)
            vSr.append((aSr,rtSr,cSr))
        
        vAllSr.append(vSr)
     
    return vAllSr

############################## Corresponde a Weighting Phase do algoritmo SAW#########
##### Retorna a lista de combinações onde é calculado o score para cada um dos serviços. 
##### O score é baseado resultado da Scaling Phase do SAW e no peso de cada um dos requerimentos    

def saw2(adqSrlist, vReq, weights):
    scoreAllList = []
    for candReq,candSr in zip(vReq, adqSrlist):
        scoreSrList = []
        for srReq,Sr in zip(candReq,candSr[1]):
            score = 0
            for i in range(len(srReq)):
                score += round((srReq[i] * weights[i]),3)
            scoreSrList.append((Sr,score))   
        scoreAllList.append(scoreSrList) 
         
    return scoreAllList    

 

    
#######

def avbComb(flow,prob):
    av = 1
    for serv in flow:
        sr = serv[0][0]
        av *= (sr['userRequirements'][0]['availability']/100)
        
    av *= prob
    av *= serv[1][0]['ava']/100
   
    av = round((av*100),2)
    return av

#######

def rtComb(flow,prob):
    rt = 0
    for serv in flow:
        sr = serv[0][0]
        rt += sr['userRequirements'][0]['executionTime'] + sr['userRequirements'][0]['delay']
    rt *= prob  
    rt += serv[1][0]['delay']
    return rt  



##### retorna o custo de uma combinação
    
def costComb(flow,prob):
    cost = 0
    for serv in flow:
        sr = serv[0][0]
        cost += sr['userRequirements'][0]['cost']
    cost *= prob
    cost += serv[1][0]['cost']    
    return cost    

########### retorna o score da combinação
    
def calcScore(flow,probability):
    
    score = 0
    for eachMS in flow:
       score += eachMS[0][1]
    score *= probability
    
    return score

#####
def calcNumServ(nameServ):
   numofSr = ""
  
   for i in range(len(nameServ)):
       if (nameServ[i] in ["0","1","2","3","4","5","6","7","8","9"]):
           #print('cMS = ',nameMS[i],'\n') 
           numofSr += nameServ[i] 

   return int(numofSr)



###########
def maxMin(lista,posTuple):
    aux = []
    
    
    for elem in lista:
        aux.append(elem[1][posTuple])
        
    maxPos = max(aux);    
    minPos = min(aux);
   
    return(maxPos,minPos)

########
def calcScoreMS(reqsList,maxMinCost,maxMinAva,maxMinRT,priorities):
    
    normatizationLista = []
    for elem in reqsList:
        if (maxMinCost[0] - maxMinCost[1] > 0):
            normCost = round((maxMinCost[0] - elem[1][0])/(maxMinCost[0] - maxMinCost[1]),3)
        else: normCost = 1.0   
        if (maxMinAva[0] - maxMinAva[1] > 0):
            normAva = round((elem[1][1] - maxMinAva[1])/(maxMinAva[0] - maxMinAva[1]),3)
        else: normAva = 1.0
        if (maxMinRT[0] - maxMinRT[1] > 0):
            normRT = round((maxMinRT[0] - elem[1][2])/(maxMinRT[0] - maxMinRT[1]),3)
        else: normRT = 1.0    
        
        normatizationLista.append((normCost,normAva,normRT))
    
    finalLista = []
    for reqs in normatizationLista:
        sc = reqs[0]*priorities[0] + reqs[1]*priorities[1] + reqs[1]*priorities[1]
        finalLista.append((reqs,sc))

    return(finalLista)





######## retorna uma lista com todas as combianções onde o custo atendem a cota do microservice.

def combinationsSr(serCadPrv,nameMS,namePr,costAPP,avbtyAPP,rspTmAPP,seqFlow,priorities):
    combList = []
    
    combs = list(itertools.product(*serCadPrv))
    
    #print('Combinacoes Candidatas: ',combs) 
    combReqsList = []
    for comb in combs:
        costMS = 0
        avlbtyMS = 1
        respTmMS  = 0
       # scoreMS = 0
        for eachTerm in seqFlow:
          avlbty = 0
          cost = 0
          respTm = 0
          score = 0
        
          for eachFlow in eachTerm[1]:
            flow = []
            probability = eachFlow[1]
            for eachServ in eachFlow[2]:
                numofMS = calcNumServ(eachServ[0][-1]) - 1
                flow.append((comb[numofMS],eachServ[1])) #obter os servicos candidatos de um fluxo.
            cost += costComb(flow,probability)
            avlbty += avbComb(flow,probability)
            respTm += rtComb(flow,probability)
            score += calcScore(flow,probability)
          
          costMS += cost
          avlbtyMS *= round((avlbty/100),2)
          respTmMS += respTm
          combReqsList.append((comb,(costMS,avlbtyMS,respTmMS)))
        
        
    maxMinCost = maxMin(combReqsList,0)
    maxMinAva = maxMin(combReqsList,1)
    maxMinRT = maxMin(combReqsList,2)
    scReqsListMS = calcScoreMS(combReqsList,maxMinCost,maxMinAva,maxMinRT,priorities)
        
    avbtyAPP = round(avbtyAPP/100,2)
       
    for combReq,scoreReq in zip(combReqsList,scReqsListMS):
        if (combReq[1][0] <= costAPP and combReq[1][1] >= avbtyAPP and combReq[1][2] <= rspTmAPP):
          combList.append(((nameMS,namePr,combReq[0],combReq[1][0],combReq[1][1],combReq[1][2]),round(scoreReq[1],3)))
          #print('Combinacoes Candidatas: ',combList) 
    
      
    return (combList)     
     


#########
def calcNumofPrvds(nameLinks):
   numofPrvd = ""
  
   for i in range(1,len(nameLinks)):
       if (nameLinks[i] in ["0","1","2","3","4","5","6","7","8","9"] and nameLinks[i-1] != "-"):
           numofPrvd += nameLinks[i]
           
   return int(numofPrvd) 

    

########## METODO PRINCIPAL: A PARTIR DESTE MÉTODO TODOS OS OUTROS SÃO ATIVADOS PARA SELECIONAR OS PROVEDORES PARA CADA UM DOS MICROSERVIÇOS DE UMA APP
########## ESTE MÉTODO RECEBE O NOME DA APP PARA QUAL SE DESEJA FAZER A SELEÇÃO DOS PROVEDORES, ALÉM DISSO ELE UTILIZA OS JSON com informações da APP e dos PROVIDERS
   
#@app.route('/apps/app/<nameApp>',methods=['GET'])
def cloudsSelection(nameApp,dataPrvd):
 
   app = [ app for app in dataAMS if (app['app'] == nameApp['app']) ]
   
   combMSPr = []
   
   for ms in app[0]['microservices']:
       combListSr = []
       combAvgList = []
       combPr = []
       listaTesteEsp = []
       
       srCandMS = servicosCandidatosMS(ms,dataPrvd)
       
       listaCandGeral.append((ms['nameMS'],srCandMS[1]))
       
######       
       iteMS =  [item['terms'] for item in iteApp[0]['iterationsMS']  if (item['microservice'] == ms['nameMS'])]    
       termsApp = [(term['nameTerm'],[term['sequences']]) for term in iteMS[0]]   
       seqFlow = [(term[0],[(flow['nameseq'],flow['probability'],[(seq['service'],seq['linksInput']) for seq in flow['dataSeq']])  for flow in term[1][0]]) for term in termsApp ]

#######  
       
       for srCad in srCandMS[0]:
           
           combListSr = []
           
           if (srCad[2]):
              vReq = saw1(srCad[2])
              scAllList = saw2(srCad[2], vReq,app[0]['weights'])
             
             
              combListSr = combinationsSr(scAllList,srCad[1],srCad[0],app[0]['cost'],app[0]['availability'],app[0]['responseTime'],seqFlow,app[0]['weights'])
              
              #print('Combinacoes Candidatas: ',combListSr) 
         
              if(len(combListSr)>0):
                #contTeste += 1
                qtdAllCombPrvd.append((srCad[0],ms['nameMS'],len(combListSr)))
                combAvgList = list(combListSr)
             
           
           if (combAvgList):
              combPr.append(combAvgList)       
       listaCandEsp.append((ms['nameMS'],listaTesteEsp))
          
       if (combPr):
         combMSPr.append(combPr)
      
   return (combMSPr, app[0]['cost'],app[0]['availability'],app[0]['responseTime'],app[0]['weights'])
     



#### descobrindo o nome do arquivo de interação
def dicoveryName(nameApp):
    nameInte = ""
    for i in range(len(nameApp)):
        if(nameApp[i] == '-'):
            nameInte = './JSON-ApproachGKP-7GG/APP'+ nameApp[i-1] + '-iterations-1.json'
  
    return nameInte


######### Principal


for nameApp in application:
    inteApp = dicoveryName(nameApp)
    for inte in interationApp:
        if (inte == inteApp):
            nameInte = inte  # Para verificar se o nome gerado existe mesmo na lista de nomes de arquivos.
    
    with open(nameApp) as json_data_file:
        dataAMS = json.load(json_data_file) # Abrir os arquivos de aplicação. 
        # dataAMS é uma lista de apps (q são dicionarios) onde cada dicionario possui uma lista que representa seus microserviços.

    with open(nameInte) as json_data_file:
        iteApp = json.load(json_data_file) # Abrir os arquivos de interação.
    


    for app  in dataAMS: # Ele vai passar em cada aplicação que são dicionários.
        for namePrvd,nameLinks in zip(prvd,linksPrvd):
            timeList = []
            listsAPP = []
            rd = []
            i = 0
            qtdALlSerPrvd = []
            qtdAllCombPrvd = []
            
            with open(namePrvd) as json_data_file:
                dataPrvd = json.load(json_data_file)
            with open(nameLinks) as json_data_file:
                dataLinks = json.load(json_data_file)    
        
            for i in range(10):
                print(i)

                totalComb = []
        
                
                inicio = time.time() 
                totalComb = cloudsSelection(app,dataPrvd)
          
                i += 1
                
        
                posMS = []
                for comb in totalComb[0]:
                    total = 0
                    for eachComb in comb:
                        total += len(eachComb)
                    if totalComb[0].index(comb) == 0:
                        posMS.append(total)
                    else: 
                        posMS.append(posMS[-1] + total)
              
        
                MS = [totalComb[0].index(comb) for comb in totalComb[0]  for eachComb in comb for i in range(len(eachComb))]
                PR = [eachComb[0][0][1] for comb in totalComb[0] for eachComb in comb for i in range(len(eachComb))]
                Score = [eachComb[0][1] for comb in totalComb[0] for eachComb in comb for i in range(len(eachComb))]
                Cost = [eachComb[0][0][3] for comb in totalComb[0] for eachComb in comb for i in range(len(eachComb))]
                Requirements = [(eachComb[0][0][3],eachComb[0][0][4],eachComb[0][0][5]) for comb in totalComb[0] for eachComb in comb for i in range(len(eachComb))]
                
#                print('MS: ',MS,'\n\n')
#                print('PosMS: ',posMS,'\n\n')
#                print('PR: ',PR,'\n\n')
#                print('Score: ',Score,'\n\n')
#                print('Cost: ',Cost,'\n\n')
                
            
                N = len(Score)
                
                totalCost = totalComb[1]
                
                MatIn = [[] for x in range(len(posMS))]
            
            
                for j, item in enumerate(MS):
                    MatIn[item].append((Score[j],Requirements[j][0],Requirements[j][1],Requirements[j][2],PR[j]))
             
                for k in range(len(MatIn)):    
                    MatIn[k].sort(key=lambda x: x[0])
        
                MatAll = MatIn
                
                for i1, ms in enumerate(MatIn):
                    j = 0
                    while (j < (len(ms) - 1)):
                        if (j < len(ms)-1):
                            k = j + 1
                            if (ms[k][0] >= ms[j][0] and ms[j][1] >= ms[k][1]):
                                ms.remove(ms[k])
                            else: j += 1    
            

                for i1, ms in enumerate(MatIn):
                    j = 0
                    while (j < (len(ms) - 2) and  len(ms) >= 3):
                        if (j < len(ms)-2):
                            k = j + 1
                            l = j + 2
                            if(ms[j][0] < ms[k][0] and ms[k][0] < ms[l][0] and ms[j][1] < ms[k][1] and ms[k][1] < ms[l][1]):
                                if ((ms[l][0] - ms[k][0])/(ms[l][1] - ms[k][1]) >= (ms[k][0] - ms[j][0])/(ms[k][1] - ms[j][1])):
                                    ms.remove(ms[k])
                                else: j += 1
                            else: j += 1    
        
                costAPP = totalComb[1]
                avaAPP =  totalComb[2]
                rtAPP = totalComb[3]
                (scoreTotal,DataList,Cost,Ava,RT,Change) = greedyKnapSack(MatIn,costAPP,avaAPP,rtAPP,dataLinks)
        
                
                fim = time.time()
                FinalTime = int(round(fim - inicio,3)*1000)
                timeList.append(FinalTime)
                
                finalCost = totalCost - Change
                
                rd.append((scoreTotal,DataList,finalCost,Change))
        
                
                '''
                if (scoreTotal > 0):
                    print('Nome Provedor: ',namePrvd,' Nome APP: ',app['app'],'\n\n')
                    print('Score total: ',scoreTotal,'\n\n')
                    print('Result: ', DataList,'\n\n')
                    print('Availability: ',Ava,' RT: ',RT,'\n')
                    print('Budget: ', totalCost,'FinalCost: ', Cost,' Change:', Change, '\n\n')
                    print('Iteracao nro: ',i,' FinalTime: ',FinalTime,'\n\n')   
                else: print('Solução não encontrada')
                '''
                # Grava em Arquivo os resultados obtidos: 
                '''
                if (i == 1):   
                    nomeArq = 'resultData' + app['app']  + '.txt'
                    with open(nomeArq, 'a') as arq2:
                      arq2.write('Set of Provider: ')
                      arq2.write(namePrvd)
                      arq2.write('\n\n')
                      arq2.write('Dados Resultados: ')
                      arq2.write('\n\n')
                      text = 'ScoreTotal'+'\t\t'+'Cost'+'\t\t'+'Ava'+'\t\t'+'RT'
                      arq2.writelines(text)
                      arq2.write('\n\n')
                      dataLine = str(scoreTotal) +  str(Cost) + str(Ava) + str(RT)
                      arq2.writelines(dataLine)
                      arq2.write('\n')
                      text = 'Item'+'\t\t'+'Score'+'\t\t'+'Cost'+'\t\t'+'Ava'+'\t\t'+'RT'+'\t\t'+'\t\t'+'MS'+'\t\t'+'Prvd'
                      arq2.writelines(text)
                      arq2.write('\n\n')
                      for data in DataList:
                          lineResult = str(data[1])+'\t\t'+str(data[6])+'\t\t'+str(data[2])+'\t\t'+str(data[3])+'\t\t'+str(data[4])+'\t\t'+str(data[0])+'\t\t'+str(data[5])
                          arq2.writelines(lineResult)
                          arq2.write('\n')
                    arq2.close()
                '''
                Lista = [scoreTotal,Cost,Ava,RT]
                if (i == 1): criaJSON.resultData(namePrvd,DataList,Lista,app['app'])

        # Grava em Arquivo Mat de serviços candidatos.
            '''
            nomeArq = 'allCandServData' + app['app']  + '.txt'
            with open(nomeArq, 'a') as arq1:
                arq1.write('Provider: ')
                arq1.write(namePrvd)
                arq1.write('\n\n')
                for k in range(len(MatAll)):
                    arq1.writelines(str(MatAll[k]))
                    arq1.write('\n')
            arq1.close()
            '''
            criaJSON.allCandServData(namePrvd,MatAll,app['app'])
	# Grava em Arquivo mat de serviços candidatos
            '''
            nomeArq = 'candServData' + app['app']  + '.txt'
            with open(nomeArq, 'a') as arq1:
                arq1.write('Provider: ')
                arq1.write(namePrvd)
                arq1.write('\n\n')
                for k in range(len(MatIn)):
                    arq1.writelines(str(MatIn[k]))
                    arq1.write('\n')
            arq1.close()
            print(MatIn)
            '''
            criaJSON.candServData(namePrvd, MatIn, app['app'])
        # Grava em Arquivo o tempo
            '''nomeArq = 'executionTime' + app['app']  +  '.txt'
            with open(nomeArq, 'a') as arq3:
                arq3.write('Provider: ')
                arq3.write(namePrvd)
                arq3.write('\n\n')
                for tm in timeList:
                    arq3.writelines(str(tm))
                    arq3.write('\n')
            arq3.close()'''
            criaJSON.executionTime( namePrvd, timeList, app['app'] )
        
        # Imprimir a lista dos 30 tempos de execução
            # print(timeList)
