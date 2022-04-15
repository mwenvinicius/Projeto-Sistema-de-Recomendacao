'''
Autor: Vinícius
Data: 14/04/2022
'''
import json

Nome = "Dados.json"
with open(Nome,"r",encoding="utf-8") as data_file:
    Dados = json.load(data_file)


Applications = Dados["Applications"]
# print(Applications)
# print("Quantidade de Applicações: %d."%(len(Applications)))
for X in Applications: 
    with open(X,"r",encoding="utf-8") as data_file:
        App = json.load(data_file)
    for NameApp in App:
        print(NameApp["app"])
        print("# Microsservices:")
        for Microsservices in NameApp["microservices"]:
            print(Microsservices["nameMS"])
    print("")
