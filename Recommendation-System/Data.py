# Autor: Vinícius Dias Batista.
# Data: 01/04/2022
import json
import os

Path = os.getcwd()
Aplications = []
Providers = []
ResultsData = []
MonitoringData = []
NewProviders = []
Interations = [] 
LinksProviders = []


DIC = {
    "Applications":[],
    "Providers":[],
    "ResultsData":[],
    "MonitoringData":[],
    "NewProviders":[],   
    "Interations":[],
    "LinksProviders":[]
}

Path = Path.replace('Recommendation-System','')
print(Path)
Remove = Path

for Path, SubPastas, Arquivos in os.walk(Path):
    for Arquivo in Arquivos:
        String = os.path.join(Path,Arquivo)
        String = String.replace(Remove,'')
        print(String)
        if("Applications/Application" in String):
            Aplications.append('../'+String)
        elif("Providers/Providers" in String):
            Providers.append('../'+String)
        elif("Results" in String):
            ResultsData.append('../'+String)
        elif("Data-Monitoring" in String):
            MonitoringData.append('../'+String)
        elif("NewProviders" in String):
            NewProviders.append('../'+String)
        elif("Interations/" in String):
            Interations.append('../'+String)
        elif("LinksProviders" in String):
            LinksProviders.append('../'+String)

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
DIC['ResultsData'] = ResultsData
DIC['MonitoringData'] = MonitoringData
DIC['NewProviders'] = NewProviders
DIC['Interations'] = Interations
DIC['LinksProviders'] = LinksProviders
Data = json.dumps(DIC,indent=5,sort_keys=False)
Name = "Dados.json"
ArquivoFinal = open(Name,'w')
ArquivoFinal.write(Data)
ArquivoFinal.close()

# print(DIC)