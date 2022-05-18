import json

ArquivosResultados = "./ResultsAPP1-a80.json"

with open(ArquivosResultados,"r",encoding="utf-8") as data_file:
    Dados = json.load(data_file)

ArquivosProvidersRS = "./resultData-RS.json"

with open(ArquivosProvidersRS,"r",encoding="utf-8") as data_file:
    Providers = json.load(data_file)

def MSRSystem(MSF):
    MS = len(MSF['MS'])
    DataProvidersR = []
    MSN = 0
    for I in MSF['MS']:
        print("O Microsserviço (%s) teve os seguintes resultados: "%(I['NameMS']))
        if I['DnfAva'] == 0:
            print("O resquisito de disponibilidade foi cumprindo durante todo o período de monitoramento.")
        else:
            print("Disponibilidade: Durante %.2f%% do tempo de monitoramento esse requisito não cumpriu o prometido."%(I['DnfAva']))
        
        if I['DnfCost'] == 0:
            print("O resquisito de custo foi cumprindo durante todo o período de monitoramento.")
        else:
            print("Custo: Durante %.2f%% do tempo de monitoramento esse requisito não cumpriu o prometido."%(I['DnfCost']))
        
        if I['DnfRT'] == 0:
            print("O resquisito de disponibilidade foi cumprindo durante todo o período de monitoramento.")
        else:
            print("Tempo de Resposta: Durante %.2f%% do tempo de monitoramento esse requisito não cumpriu o prometido."%(I['DnfRT']))
        
        if I['DnfAva'] != 0 or I['DnfCost'] != 0 or I['DnfRT'] != 0:
            print("\nRECOMENDAÇÕES\n")
            for J in Providers:
                print("| LinkProvider: %s."%(J["Provider"]))
                print("| - PROVEDOR:%s"%(J["Resultados"][MSN]["Prvd"]))
                print("|  + Disponibilidade (Prometida): %.2f."%(J["Resultados"][MSN]["Ava"]))
                print("|  + Custo (Prometido): %.2f."%(J["Resultados"][MSN]["Cost"]))
                print("|  + Tempo de Resposta (Prometido): %.2f.\n"%(J["Resultados"][MSN]["RT"]))
        MSN += 1
    

MSRSystem(Dados)