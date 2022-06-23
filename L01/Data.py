# Autor: Vinícius Dias Batista.
# Data: 01/04/2022
import json
import os

Path = os.getcwd()

Aplications = []
Providers = []
Iterations = [] 
LinksProviders = []


DIC = {
    "Applications":[],
    "Providers":[], 
    "Iterations":[],
    "LinksProviders":[]
}

print(Path)

Remove = Path

for Path, SubPastas, Arquivos in os.walk(Path):
    for Arquivo in Arquivos:
        String = os.path.join(Path,Arquivo)
        String = String.replace(Remove,'')
        print(String)
        
        if("Applications/Application" in String):
            Aplications.append('.'+String)
        elif("Providers/Providers" in String):
            Providers.append('.'+String)
        elif("Iterations/" in String):
            Iterations.append('.'+String)
        elif("Links-Providers" in String):
            LinksProviders.append('.'+String)
        '''
        elif("resultData" in String):
            ResultsData.append('../'+String)
        elif("gerador/APP" in String):
            MonitoringData.append('../'+String)
        elif("NewProviders" in String):
            NewProviders.append('../'+String)
        '''
        

'''
print(os.path.abspath(os.getcwd()))
print(Aplications)
print(Providers)
print(ResultsData)
print(MonitoringData)
print(NewProviders)
'''

DIC['Applications'] = Aplications
DIC['Providers'] = Providers
DIC['Iterations'] = Iterations
DIC['LinksProviders'] = LinksProviders
# DIC['ResultsData'] = ResultsData
# DIC['MonitoringData'] = MonitoringData
# DIC['NewProviders'] = NewProviders

Data = json.dumps(DIC,indent=5,sort_keys=False)
Name = "Data-Start.json"
ArquivoFinal = open(Name,'w')
ArquivoFinal.write(Data)
ArquivoFinal.close()

# print(DIC)
