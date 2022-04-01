# Autor: Vinícius Dias Batista.
# Data: 01/04/2022
import os

Path = ""
Aplications = []
Providers = []
ResultsData = []
MonitoringData = []
NewProviders = []

for Path, SubPastas, Arquivos in os.walk(Path):
    for Arquivo in Arquivos:
        String = os.path.join(Path,Arquivo)
        if("Application" in String):
            Aplications.append(String)
        elif("Providers" in String):
            Providers.append(String)
        elif("Results" in String):
            ResultsData.append(String)
        elif("Data-Monitoring" in String):
            MonitoringData.append(String)
        elif("NewProviders" in String):
            NewProviders.append(String)

print(Aplications)
print(Providers)
print(ResultsData)
print(MonitoringData)
print(NewProviders)

# Files = os.listdir(Path)
# Files = [f for f in os.listdir(Path) if os.path.isfile(os.path.join(Path,f))]
# print(Files)
# from os.path import isfile, join
# Path = '/home/viniciusdiasb/Documentos/Recommendation-System'
# Files = listdir(Path)
# Caminho = "/home/viniciusdiasb/Documentos/Recommendatio-System"
