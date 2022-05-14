from genericpath import isfile
import json
import datetime as dt
from dateutil import rrule
import random
from horarios import *
from arquivo import *


def loadFile(nome):
    # Carrega os dados de um arquivo json.
    """ print(isfile(nome))
    print(nome) """
    if isfile(nome) == True:
        with open(nome, "r", encoding="utf-8") as data_file:
            dados = json.load(data_file) # envia os dados já presentes no arquivo json.
    else:
        dados = [] # Caso o arquivo não exista é enviado uma lista.
    return dados


def openFiles( app ):
    Files = []
    for i in app["MicroServices"]:
        nameFile = (f'{app["NameApp"]}_MS{i["MS"]}_{i["Prvd"]}.json')
        oneFile = loadFile(nameFile)
        
        if len(oneFile) == 0:
            # Se o arquivo estiver vazio (foi criado agora), então deve ser declarado os dados iniciais.
            oneFile.append({
                "NameFile": nameFile,
                "NameAPP": app["NameApp"],
                "NameOfMicroService": i['MS'],
                "Provider": i['Prvd'],
                "Availability": i['Ava'],
                "Cost": i['Cost'],
                "ResponseTime": i['RT'],
                "Monitoring": [] 
            })

        Files.append( oneFile ) 
    
    return Files


def saveFinalFile(nameARQ, lido):
    # Função que salva os dados em um arquivo JSON.
    data = json.dumps(lido, indent=5, sort_keys=False)
    arqFINAL = open(nameARQ,'w')
    arqFINAL.write(str(data))
    arqFINAL.close()


def saveFiles(Files):
    for i in Files:
        saveFinalFile(i[0]["NameFile"], i)


