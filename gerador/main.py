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

def abrirApps(results, pasta):
    apps = []
    for i in range(len(results)):
        apps.append( Gerador(indice=i, pasta=pasta) )
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
    print('Selecione o app (digite o índice, se quiser mais de 1 separe por virgulas): ')
    for indice, i in enumerate(results):
        print(f'{indice} --- {i["App"]}')
    
    op = input('Selecione: ').split(',')
    indices = []
    for j in op:
        indices.append(int(j))

    retorno = []
    for k in indices:
        retorno.append( results[k] )

    print('-'*75)
    return retorno

def menu(results, pasta):
    print('-'*75)
    op = int(input('Deseja gerar para todos os apps (1-SIM;2-NAO): '))
    print('-'*75)
    if op == 1:
        retorno = abrirApps(results, pasta)  
    else:
        results2 = selecionarApp(results)
        retorno = abrirApps(results2, pasta)

    return retorno


pasta = input('Digite o nome da pasta onde serão salvo os arquivos: ')
results = loadFile('resultData.json')
apps = menu(results, pasta)
gerarTodos(apps)

""" for i in apps:
    print(f'name_app = {i.name_app} | caso = {i.case} | datas = {i.date_initial.date()} até {i.date_final.date()}')

"""