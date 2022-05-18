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

def selecionarApp(results):
    print('Selecione o app (digite o índice): ')
    for indice, i in enumerate(results):
        print(f'{indice+1} --- {i["App"]}')
    
    op = int(input('Selecione: '))
    op = op - 1

    retorno = [ results[op] ]
    return retorno



def menu(results):
    print('-'*75)
    op = int(input('Deseja gerar para todos os apps (1-SIM;2-NAO): '))
    print('-'*75)
    if op == 1:
        retorno = abrirApps(results)  
    else:
        results2 = selecionarApp(results)
        retorno = abrirApps(results2)

    return retorno




results = loadFile('resultData.json')
apps = menu(results)
gerarTodos(apps)

""" for i in apps:
    print(f'name_app = {i.name_app} | caso = {i.case} | datas = {i.date_initial.date()} até {i.date_final.date()}')

"""