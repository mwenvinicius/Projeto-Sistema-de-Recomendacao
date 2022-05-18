from arquivo import *
from horarios import *
from gerador2 import Gerador


def sequencia(app):
    app.abreArq()
    app.selecionarIntervalo()
    app.selectCase()
    app.selecionarDatas()
    app.abrirPastaPadrao()
    app.abrirArqDados()
    app.vaiProCaso()
    app.salvarArqGestao()


def abrirApps(results):
    apps = []
    for i in range(len(results)):
        apps.append( Gerador(indice=i) )
        sequencia(app=apps[i])
    return apps

def gerarTodos(apps):
    print('-'*75)
    for i in apps:
        print(f"APP: {i.name_app}")
        i.montar()
        print('-'*75)
    print('Gerado! ;) ')


def selecionarPasta():
    pass




results = loadFile('../Recommendation-System/resultData.json')
apps = abrirApps(results)
gerarTodos(apps)

for i in apps:
    print(f'name_app = {i.name_app} | caso = {i.case} | datas = {i.date_initial.date()} até {i.date_final.date()}')

