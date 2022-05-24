'''
Autor: Vinícius Dias Batista.
Data: 08/05/2022
'''
import json

NomeArquivo = "Dados.json"
with open(NomeArquivo,"r",encoding="utf-8") as data_file:
    Dados = json.load(data_file)

SelectionsResults = Dados["ResultsData"]

NomeArquivo2 = SelectionsResults[0]
with open(NomeArquivo2,"r",encoding="utf-8") as data_file:
    ApplicationData = json.load(data_file)
'''
MicrosservicesMD = [] # Arquivos Dados de Monitoramento dos Microsserviços.
for Application in ApplicationData:
    print(Application["App"])
'''

# Função definida para procurar arquivos de monitoramento dos microsserviços pelo nome do APP.
def GetMicroservicesMonitoringFiles(ApplicationResultsData,FilesMonitoring):
    MMF = []
    for Application in ApplicationResultsData:
        LF = []
        for File in FilesMonitoring:
            if Application['App'] in File:
                LF.append(File)
        AppMMF = {
            "AppName":Application['App'],
            "MMFilesApp":LF
        }
        MMF.append(AppMMF)
    return MMF

def ReadingDataFromMicroservices(MMFiles):
    DMM = []
    for File in MMFiles:
        with open(File,"r",encoding="utf-8") as data_file:
            Data = json.load(data_file)
        DMM.append(Data)
    return DMM

def AnalysisOfAMicroservice(MMS):
    Data = []
    for M in MMS:
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
            
            Tupla = (I["Availability"],I["Cost"],I["ResponseTime"])
            Data.append(Tupla)

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
        # print(Interval)
        # print(PerA,PerC,PerRT)
        Percentual = (PerA,PerC,PerRT)
    # O que vou retornar nessa função ?
    # print(Data)
    return [Interval,Percentual,Data]

def ApplicationAnalysis(DataAPP):
    MonitoringFiles = ReadingDataFromMicroservices(DataAPP["MMFilesApp"])
    DataMMF = []
    for I in MonitoringFiles:
        
        Results = AnalysisOfAMicroservice(I)
        DataMMF.append(Results[2])

def GetTime(MS):
    Time = []
    for I in MS[0]['Monitoring']:
        T = I['Date']+I['Time']
        Time.append(T)
    return Time

# print(GetMicroservicesMonitoringFiles(ApplicationData,Dados["MonitoringData"]))
# X = GetMicroservicesMonitoringFiles(ApplicationData,Dados["MonitoringData"])
# Y = ReadingDataFromMicroservices(X[0]["MMFilesApp"])
# print(Y)
# print(X)
# print(AnalysisOfAMicroservice(Y[0]))
# ApplicationAnalysis(X[0])