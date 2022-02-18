import json
import random


def generateLinks(outLink,inLink):
    data = {
        "out": "",
        "in": "",
        "availability": 0.0,
        "delay":0,
        "cost": 0
    }

    data["out"] = outLink
    data["in"] = inLink
    #data["availability"] = 1 + round(random.uniform(98,99),3)
    data["availability"] = 100
    data["delay"] = 1 + random.randrange(1,2)
    data["cost"] = 1 + random.randrange(1,10)

    return data


def generateNewLink(outLink,inLink,ava,delay,cost):
    data = {
        "out": "",
        "in": "",
        "availability": 0.0,
        "delay":0,
        "cost": 0
    }

    data["out"] = outLink
    data["in"] = inLink
    data["availability"] = ava
    data["delay"] = delay
    data["cost"] = cost

    return data

def generateLinksEqual(outLink,inLink,linkdata):
    
    
    #newdata = copy.deepcopy(linkdata)
    
    #print('linkdata = ',linkdata,'\n')
    #newdata["out"] = outLink
    #newdata["in"] = inLink
   
    ava = linkdata["availability"]
    delay = linkdata["delay"]
    cost = linkdata["cost"]
    
    newdata = generateNewLink(outLink,inLink,ava,delay,cost)
    
    return newdata


def greaterThan(outLink,inLink):
    maior = False
    numOut = ""
    numIn = ""
    for i in range(len(outLink)):
       if (outLink[i] in ["0","1","2","3","4","5","6","7","8","9"]):
           numOut += outLink[i]
           
    for i in range(len(inLink)):
       if (inLink[i] in ["0","1","2","3","4","5","6","7","8","9"]):
           numIn += inLink[i]       
        
    if (int(numOut) > int(numIn)):
        maior = True
    return maior


def search(inLink,outLink,linkData):
    data = []
    for data in linkData:
        if (data["out"] == inLink and data["in"] == outLink):
            return data
    
    return data

def generateNameProviders(numofProviders):
    
    providers = []
    for indexProvider in range(numofProviders):
       namePrvd = "P"+ str(indexProvider)
       providers.append(namePrvd)
       
    return providers




# Main

numofProviders = [500]

for number in numofProviders:
    numTotalLinks = number*(number-1)
    data = []
       
    listofProviders = generateNameProviders(number)
    #print('listofProviders = ',listofProviders,'\n')
        
    for outLink in  listofProviders:
       for inLink in listofProviders:
          if (outLink != inLink and greaterThan(outLink,inLink)): 
             linkData = search(inLink,outLink,data)
             #print('linkData = ',linkData,'\n')   
             if(linkData != {}):  
               #print('Passei por aqui -- 1')  
               newData = generateLinksEqual(outLink,inLink,linkData)
               data.append(newData) 
          else: 
             if(outLink != inLink):
               linkData = generateLinks(outLink,inLink)
               data.append(linkData)
          #print('data = ',data,'\n')      
        

    data =  json.dumps(data, indent=5, sort_keys=False)

    nomeArq = 'linksProviders'+ str(number) + '.json'

    arqFinal = open(nomeArq,'w')
    arqFinal.write(data)
    arqFinal.close()   

