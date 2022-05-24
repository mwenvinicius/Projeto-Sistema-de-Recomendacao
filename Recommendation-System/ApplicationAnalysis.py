import Analysis
import json

ResultData = "./resultData.json"

MonitoringFiles = ["APP1-a80/APP1-a80_MS0_P22.json",
          "APP1-a80/APP1-a80_MS1_P22.json",
          "APP1-a80/APP1-a80_MS2_P39.json",
          "APP1-a80/APP1-a80_MS3_P22.json",
          "APP1-a80/APP1-a80_MS4_P5.json",
          "APP1-a80/APP1-a80_MS5_P41.json"]


with open(ResultData,"r",encoding="utf-8") as data_file:
    Dados = json.load(data_file)

print(Dados[0])

def APPAnalysis(APPData):
    Qnt = len(APPData['Resultados'])
    # print(Qnt)

    ListDataMS = Analysis.ReadingDataFromMicroservices(MonitoringFiles)
    Lista = []
    DataMS = []
    Historic = []
    Sequence = 0
    Interval = []
    Time = Analysis.GetTime(ListDataMS[0])
    PercentualMS = []
    Intervals = []
    LOW = {
        "AVAL":0,
        "COSTL":0,
        "RTL":0
    }

    for I in range(Qnt):
        This = Analysis.AnalysisOfAMicroservice(ListDataMS[I])
        # print(This)
        # print(MonitoringFiles[I])
        Block = 0
        NMS = ""
        for I in MonitoringFiles[I]:
            if I == '_' and Block == 0:
                Block = 1
            elif I == '_' and Block == 1:
                Block = 0
            if Block == 1 and I != '_':
                NMS += I
         
        # print(NMS)

        Ms = {
            "NameMS":NMS,
            "DnfAva":This[1][0],
            "DnfCost":This[1][1],
            "DnfRT":This[1][2],
            "DnfInterval":This[0]
            
        }
        Lista.append(Ms)
        DataMS.append(This[2])
    
    # print(len(DataMS))
    # print(ListDataMS[0])
   
    for I in range(len(DataMS[0])):
        Ava = 0
        Cost = 0
        RT = 0
        R = 0
        for J in range(len(DataMS)):
            Ava += DataMS[J][I][0]
            Cost += DataMS[J][I][1]
            RT += DataMS[J][I][2]
        # print(Ava,Cost,RT)
        # print(APPData['Ava'])
        if Ava/len(DataMS) < float(APPData['Ava']):
            R += 1
            LOW["AVAL"] += 1
        if Cost > float(APPData['Cost']):
            R += 4
            LOW["COSTL"] += 1
        if RT > float(APPData['RT']):
            R += 6
            LOW["RTL"] += 1
        Tupla = (Ava/len(DataMS),Cost,RT)
        Historic.append(Tupla)
        # print(R)
        if R > 0:
            if Sequence == 0:
                Start = Time[I]
                Sequence += 1
            Atual = Time[I]
        else:
            if Start != '':
                Interval.append([Start,Atual])
                Start = ""
                Sequence = 0
        if(I+1==len(DataMS[0])):
                Interval.append([Start,Atual])
    
    # print(Interval)
    TAM = len(DataMS[0])
    Data = {
        "App":APPData["App"],
        "Availability":APPData["Ava"],
        "Cost":APPData["Cost"],
        "ResponseTime":APPData["RT"],
        "Percentage":{"Ava":LOW["AVAL"] / (TAM/100),
            "Cost":LOW["COSTL"] / (TAM/100),
            "RT":LOW["RTL"] / (TAM/100)},
        "Interval":{"APPIntervals":Interval},
        "MS":Lista
    }

    NomeArquivo = 'Results'+ str(APPData["App"])+'.json'
    ArquivoFinal = open(NomeArquivo,'w')
    Data =  json.dumps(Data,indent=5,sort_keys=False)
    ArquivoFinal.write(Data)
    ArquivoFinal.close()

APPAnalysis(Dados[0])