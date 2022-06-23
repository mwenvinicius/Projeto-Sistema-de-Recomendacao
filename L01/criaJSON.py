from genericpath import isfile
import json

def carregar(nome):
    # Carrega os dados de um arquivo json.
    if isfile(nome):
        with open(nome, "r", encoding="utf-8") as data_file:
            dados = json.load(data_file) # envia os dados já presentes no arquivo json.
    else:
        dados = [] # Caso o arquivo não exista é enviado uma lista.
    return dados


def salvar(nameARQ, lido):
    # Função que salva os dados em um arquivo JSON.
    data = json.dumps(lido, indent=5, sort_keys=False)
    arqFINAL = open(nameARQ,'w')
    arqFINAL.write(str(data))
    arqFINAL.close()


def executionTime( namePrvd, timeList, app ):
    nameARQ = "Execution-Time.json"
    lido = carregar(nameARQ)
    data = {
        "App": str(app),
        "Provider":str(namePrvd),
        "TimeList":timeList
    }
    lido.append(data)

    salvar(nameARQ, lido)


def candServData(namePrvd, MatIn, app):
    nameARQ = "Cand-Serv-Data.json"
    lido = carregar(nameARQ)
    data = {
        "App": str(app),
        "Provider": str(namePrvd),
        "Features": [] 
    }

    lista = []
    for i in MatIn:
        for j in i:
            lista.append( {
                    "Score": str(j[0]),
                    "Cost": str(j[1]),
                    "Availability": str(j[2]),
                    "ResponseTime": str(j[3]),
                    "Provider": str(j[4])
                }
            )

    data["Features"] = lista
    lido.append(data)

    salvar(nameARQ, lido)



def allCandServData(namePrvd,MatAll,app):
    nameARQ = "All-Cand-Serv-Data.json"
    lido = carregar(nameARQ)
    data = {
        "App": str(app),
        "Provider":str(namePrvd),
        "MatAll":[]  
    }

    lista = []
    for i in MatAll:
        for j in i:
            lista.append( {
                    "Score": str(j[0]),
                    "Cost": str(j[1]),
                    "Availability": str(j[2]),
                    "ResponseTime": str(j[3]),
                    "Provider": str(j[4])
                }
            )

    data["MatAll"] = lista
    lido.append(data)

    salvar(nameARQ, lido)

def CriaD(data):
    return {
    	"Item":data[1],
    	"Score":data[6],
    	"Cost":data[2] ,
    	"Ava":data[3],
    	"RT":data[4] ,
    	"MS":data[0],
    	"Prvd":str(data[5])
    }

 
def resultData(namePrvd,DataList,Lista,app):
    nameARQ = "Result-Data.json"
    lido = carregar(nameARQ)
    dataAll = {
    	"App": str(app),
        "Provider":str(namePrvd),
        "ScoreTotal":str(Lista[0]),
        "Cost":str(Lista[1]),
        "Ava":str(Lista[2]),
        "RT":str(Lista[3]),
        "Resultados":[]
    }
    
    for data in DataList:
        RES = CriaD(data)
        lineResult = str(data[1])+'\t\t'+str(data[6])+'\t\t'+str(data[2])+'\t\t'+str(data[3])+'\t\t'+str(data[4])+'\t\t'+str(data[0])+'\t\t'+str(data[5])
        print(lineResult)
        dataAll['Resultados'].append(RES)
   
    lido.append(dataAll)

    salvar(nameARQ, lido)
