import datetime as dt
from dateutil import rrule
import random
from horarios import *
from arquivo import *


def selectBasicLimits( File, case):

    #print("Chegou aqui!")

    if case == 1:
        # Melhor caso
        ava =  [ float(File["Availability"]), 1.0 ]
        cost = [ 0.0, float(File["Cost"]) ]
        resp = [ 0.0, float(File["ResponseTime"]) ]
    
    elif case == 2:
        # Pior caso
        ava =  [ 0.0, float(File["Availability"]) ]
        cost = [ float(File["Cost"]), 200.0 ]
        resp = [ float(File["ResponseTime"]), 100.0 ]

    else:
        # Caso aleatório
        ava =  [ 0.0, 1.0 ]
        cost = [0.0, 200.0]
        resp = [0.0, 100.0]

    #print(ava)

    limits =  {
        'Availability': ava,
        'Cost': cost,
        'ResponseTime': resp
    }

    return limits


def selectRequiLimits(File, Requirements):

    """ if Requirements["Defined"] == False:
        # Caso o caso dos requirimentos já não estejam selecionados, ele sorteia um caso para cada um.
        Requirements["Defined"] = True
        Requirements["Availability"] = random.randint(1,3)
        Requirements["Cost"] = random.randint(1,3)
        Requirements["ResponseTime"] = random.randint(1,3) """


    if Requirements["Availability"] == 1:
        ava = [ float(File["Availability"]), 1.0 ]
    elif Requirements["Availability"] == 2:
        ava = [ 0.0, float(File["Availability"]) ]
    else:
        ava = [ 0.0, 1.0 ]
    

    if Requirements["Cost"] == 1:
        cost = [ 0.0, float(File["Cost"]) ]
    elif Requirements["Cost"] == 2:
        cost = [ float(File["Cost"]), 200.0 ]
    else:
        cost = [0.0, 200.0]


    if Requirements["ResponseTime"] == 1:
        resp = [ 0.0, float(File["ResponseTime"]) ]
    elif Requirements["ResponseTime"] == 2:
        resp = [ float(File["ResponseTime"]), 100.0 ]
    else:
        resp = [0.0, 200.0]
    

    limits =  {
        'Availability': ava,
        'Cost': cost,
        'ResponseTime': resp
    }

    return limits


def generateRandomData(File, initial_date, limits):
    File[0]['Monitoring'].append(
        {
            "Date": str(initial_date.date()),
            "Time": str(initial_date.time()),
            "Availability": round( random.uniform( limits["Availability"][0], limits["Availability"][1] ) , 2) ,
            "Cost": round( random.uniform( limits["Cost"][0], limits["Cost"][1] ) , 2) ,
            "ResponseTime": round( random.uniform( limits["ResponseTime"][0], limits["ResponseTime"][1] ) , 2)
        }
    )


def selectCase(File, data):
    if data["Case"] in [1,2,3]:
        # Caso básico.
        generateRandomData(File, data["Initial"], selectBasicLimits(File[0], data["Case"]))
    elif data["Case"] == 4:
        # Parcial pelo o requerimento.
        #print(File)
        generateRandomData(File, data["Initial"], selectRequiLimits(File[0], data["RequirementSelected"]) )


def generate( data ):
    Files = openFiles(data["App"])
    while( compareDate( data["Initial"], data["Final"] ) == False ):
        weeknd = int(data["Initial"].date().weekday())
        
        if weeknd in data["SelectedDAYS"]:
            #print("Chegou aqui")
            for i in Files:
                selectCase(i, data)
        
        data["Initial"] = rrule.rrule(rrule.MINUTELY, interval=data["Interval"], dtstart=data["Initial"], count=2)[1] # Acrescenta o intervalo de tempo no marcador de tempo.
    
    saveFiles(Files)


# Interval in minutes:
# interval = 15

# Datas:
# initial_date = dt.datetime(year=2022, month=2, day=19)
# final_date = dt.datetime(year=2022, month=2, day=22)

'''
    selectDAYS:
        0 : Monday
        1 : Tuersday
        2 : Wednesday
        3 : Thursday
        4 : Friday
        5 : Saturday
        6 : Sunday      '''
#selectedDAYS = [0,1,2,3,4,5,6] # Configurado para somente os dias de semana.


# Leitura dos dados do arquivo Result:
aux = loadFile('resultData.json')[0] # Carrega dados de um App do arquivo results.

""" app = {
    "NameApp": aux["App"],
    "MicroServices": [ i for i in aux['Resultados'] ] # For que coloca os Micro
} """

'''
    A variável CASE indica qual o situação será gerada.
    
    * Casos básicos:
        [OK] - 1 - O gerador gerará arquivos com dados randomicos porém todos os requisitos são atendidos.
        
        [OK] - 2 - O gerador gerará arquivos com dados randomicos porém nenhum dos requisitos serão atendidos.
        
        [OK] - 3 - O gerador gerará arquivos onde cada hora resultará em valores diferentes.
    
    * Casos por Requirementos:
        [OK] - 4 - O gerador gerará arquivos onde será escolhido randomicamente quais requirimentos atenderão os requerimentos. Exemplo: Disponibilidade atende, ao mesmo tempo que o custo não.
    
    * Casos por Microsserviço:
        [  ] - 5 - O gerador gerará arquivos onde serão escolhidos randomicamente quais microsserviços atenderão os requerimentos. Exemplo: MS5 está atendendo, ao mesmo tempo que o MS7 não.
'''

data = {
    
    "Interval": 15, # Intervalo em minutos
    
    "Initial": dt.datetime(year=2022, month=2, day=19), # Data inicial
    
    "Final": dt.datetime(year=2022, month=2, day=22), # Data Final
    
    "SelectedDAYS": [0,1,2,3,4,5,6], # Configurado para somente os dias de semana.
    
    "App": {
        "NameApp": aux["App"],
        "MicroServices": [ i for i in aux['Resultados'] ] # For que coloca os Micro
    },

    "Case": 4,

    "RequirementSelected": {
        #"Defined": True,
        # 1 - melhor caso
        # 2 - pior caso
        # 3 - aleatório

        "Availability": 1,  # Melhor caso.
        "Cost": 1,          # Melhor caso.
        "ResponseTime": 2   # Pior caso.
    }
}

generate(data)
#
