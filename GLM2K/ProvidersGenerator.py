import json
import random

def generateComputerService():
    data = {
        "nameSer": "",
        "functionality": "",
        "features": [],
        "capabilities":[{"CPU":"","Core":0,"RAM":0,"HD":0}],
        "userRequirements": [{"executionTime":0,"delay":0,"availability":0,"cost":0}]
    }

    data["functionality"] = random.choice(["instantiate virtual machines", "for deploying and scaling web applications"])
    data["capabilities"][0]["CPU"] = random.choice(["i5", "i7"])
    #data["capabilities"][0]["CPU"] = random.choice(["i7"])
    #data["capabilities"][0]["Core"] = random.choice([2, 4, 8, 16, 32])
    data["capabilities"][0]["Core"] = random.choice([8, 16])
    #data["capabilities"][0]["RAM"] = random.choice([2, 4, 8, 16, 32])
    #data["capabilities"][0]["RAM"] = random.choice([8, 16, 32])
    data["capabilities"][0]["RAM"] = random.choice([8,64])
    data["capabilities"][0]["HD"] = 1 + random.randrange(512,2048)
    data["userRequirements"][0]["executionTime"] = 1 + random.randrange(1,5)
    data["userRequirements"][0]["delay"] = 1 + random.randrange(1,2)
    #data["userRequirements"][0]["availability"] = 1 + random.randrange(98,100)
    data["userRequirements"][0]["availability"] = 1 + round(random.uniform(99,99),3)
    data["userRequirements"][0]["cost"] = 1 + random.randrange(10,30)

    return data

def generateStorageService():
    data = {
        "nameSer": "",
        "functionality": "",
        "features": ["stores data", "retrives data"],
        "capabilities":[],
        "userRequirements": [{"executionTime":0,"delay":0,"availability":0,"cost":0}]
    }

    data["functionality"] = random.choice(["object storage", "persistent block storage volumes"])
    data["userRequirements"][0]["executionTime"] = 1 + random.randrange(1,5)
    data["userRequirements"][0]["delay"] = 1 + random.randrange(1,2)
    #data["userRequirements"][0]["availability"] = 1 + random.randrange(98,100)
    data["userRequirements"][0]["availability"] = 1 + round(random.uniform(99,99),3)
    data["userRequirements"][0]["cost"] = 1 + random.randrange(10,30)

    return data

def generateDatabaseService():
    data = {
        "nameSer": "",
        "functionality": "",
        "features": [],
        "capabilities":[],
        "userRequirements": [{"executionTime":0,"delay":0,"availability":0,"cost":0}]
    }

    data["functionality"] = random.choice(["Relational Database", "NoSQL Database"])
    data["userRequirements"][0]["executionTime"] = 1 + random.randrange(1,5)
    data["userRequirements"][0]["delay"] = 1 + random.randrange(1,2)
    #data["userRequirements"][0]["availability"] = 1 + random.randrange(98,100)
    data["userRequirements"][0]["availability"] = 1 + round(random.uniform(98.001,99.999),3)
    data["userRequirements"][0]["cost"] = 1 + random.randrange(10,30)

    return data

def generateService(serviceClass):
    switcher = {"compute":generateComputerService, "storage":generateStorageService, "database":generateDatabaseService}
    function = switcher.get(serviceClass)
    return function()

# Main


for numberOfProviders in range(50,51,1):
    data = []
   
    for indexProvider in range(numberOfProviders):
        providerData = {"provider": "P"+ str(indexProvider), "servicesClass": []}
    
        indexClass = 1
        for serviceClass in ["compute", "storage", "database"]:
             serviceClassData = {"nameCl": serviceClass+"-C"+str(indexClass), "services": []}
    
             #numberOfServices = random.randrange(5)
             numberOfServices = 25
             for indexService in range(numberOfServices):
                 serviceData = generateService(serviceClass)
                 serviceData["nameSer"] = "S"+str(indexService)+"-C"+str(indexClass)+"-P"+str(indexProvider)
                 serviceClassData["services"].append(serviceData)
             providerData["servicesClass"].append(serviceClassData)
    
             indexClass += 1
    
        data.append(providerData)
    
    data =  json.dumps(data, indent=5, sort_keys=False)


    nomeArq = 'ProvidersGKP'+ str(numberOfProviders) + '-'+ str(numberOfServices) + '.json'

    arqFinal = open(nomeArq,'w')
    arqFinal.write(data)
    arqFinal.close()   
#print(json.dumps(data))
