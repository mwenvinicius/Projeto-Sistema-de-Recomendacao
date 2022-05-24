'''
Autor: Vinícius
Data: 14/04/2022
'''
from ast import In
import json
from datetime import datetime

Nome = "Dados.json"
with open(Nome,"r",encoding="utf-8") as data_file:
    Dados = json.load(data_file)

# Applications = Dados["Applications"]
Monitored = Dados["MonitoringData"]

'''
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
'''

print(Monitored)

for DataAPPs in Monitored:
    with open(DataAPPs,"r",encoding="utf-8") as data_file:
        MSData = json.load(data_file)
    for M in MSData:
        PA = M["Availability"]
        PC = M["Cost"]
        PRT = M["ResponseTime"]
        MSMonitored = M["Monitoring"]
        # print(M["Monitoring"])
        LOW = {
            "Availability":0,
            "Cost":0,
            "ResponseTime":0,
            "Data-Monitoring":[]
        }
        Qnt = 0 # Guarda a quantidade de vezes de dados de monitoramento.
        Sequence = 0 # Sequência em que um dos requisitos não está comprindo o prometido.
        Interval = []
        # Isso é um teste.
        XRT = []
        YRT = []
        Start = ""
        Tam = len(MSMonitored)
        for I in MSMonitored:
            '''
            print("[DATE]:%s;[TIME]:%s;[AVAILABILITY]:%.1f;[COST]:%.2f;[RESPONSE-TIME]:%.2f."
            %(I["Date"],I["Time"],I["Availability"],I["Cost"],I["ResponseTime"]))
            '''
            R = 0
            L = {
                "Date":"-",
                "Time":"-",
                "Availability":"-",
                "Cost":"-",
                "ResponseTime":"-",
                "Sequence":[]
            }

            if I["Availability"] < PA:
                L["Availability"] = I["Availability"]
                LOW["Availability"] += 1 
                R += 1
            if I["Cost"] > PC:
                L["Cost"] = I["Cost"]
                LOW["Cost"] += 1
                R += 4
            if I["ResponseTime"] > PRT:
                L["ResponseTime"] = I["ResponseTime"]
                LOW["ResponseTime"] += 1
                R += 6
            
            if R > 0:
                XRT.append(L["ResponseTime"])
                StringNew = I["Date"]+I["Time"]
                StringNew = StringNew.replace(":",'')
                StringNew = StringNew.replace("-",'')
                YRT.append(StringNew)
                L["Date"] = I["Date"]
                L["Time"] = I["Time"]
                L["Sequence"].append(Sequence)
                L["Sequence"].append(R)                
                LOW["Data-Monitoring"].append(L)
                if Sequence == 0:
                    Start = StringNew
                Atual = StringNew
                Sequence += 1
            else:
                if Start != '':
                    Interval.append([Start,Atual])
                    Start = ""
                Sequence = 0
            if(Tam-1==Qnt):
                Interval.append([Start,Atual])
            Qnt += 1
        # print(Qnt,Tam)
        '''
        for I in LOW["Data-Monitoring"]:   
            print(I)
        for I in LOW["Data-Monitoring"]:   
            if(I[Sequence][0] == 0 and ):
        '''
        # print(XRT)
        # print(YRT) 
        PerA  = LOW["Availability"] / (Qnt/100)
        PerC  = LOW["Cost"] / (Qnt/100)
        PerRT = LOW["ResponseTime"] / (Qnt/100)
        print(Interval)
        # print(PerA,PerC,PerRT)