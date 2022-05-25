import copy
import json
import datetime as dt
from dateutil import rrule
import random
import os

# from scipy import rand

from arquivo import *
from horarios import *



class Gerador():

    def __init__(self, indice=0, pasta=None):
        self.date_initial = None #........ Data inicial do monitoramento
        self.date_final = None #.......... Data final do monitoramento
        self.name_app = None #............ Nome do app;
        self.microsservices = None #...... Microsserviços extraídos do arquivo result;
        self.pasta = pasta #.............. Pasta onde será salvo o caminho;
        self.case = 0 #................... Caso a ser gerado que será selecionado na função selectCase()
        self.result = None #.............. Aqui estarão os dados do arquivo resultData.json 
        self.intervalo = 15 #............. Intervalo em minutos, setado em 15 minutos.
        self.indice = indice #............ Indice onde o app se encontra no vetor presente no arquivo results
        self.arquivos = {
            'Pasta': '',
            'NomesArqs': [] } #........... Aqui serão salvos as informações sobre os arquivos de salvamento.
        
        #self.sequencia() #................ Faz a chamada das funções.

    def sequencia(self):
        #self.abreArq()
        #self.selecionarIntervalo()
        #self.selecionarDatas()
        #self.selecionarPasta()
        self.abrirPastaPadrao()
        self.abrirArqDados()
        #self.selectCase()
        self.vaiProCaso()
        self.montar()
        self.salvarArqGestao()

        print('Gerado! ;)')
        
    def abreArq(self):
        # Função que abre o arquivo result e transfere seus dados aos atributos da classe
        self.result = loadFile('resultData.json')[self.indice]
        self.name_app = self.result["App"]
        self.microsservices = [ i for i in self.result['Resultados'] ] # For que coloca os Micro

    def selecionarIntervalo(self):
        self.intervalo = int(input('Digite o intervalo (em min): '))
        print('\n\n')

    def selecionarDatas(self):
        # Função que solicitará ao usuario que ele digite as datas, tanto a inicial como a final.
        print('-'*60)
        print(f'Selecionar datas para o monitoramento {self.name_app}: ')
        print('-'*60)

        trava = 0

        while trava == 0:

            inicial = input('Digite a data inicial (DD/MM/YYYY) separado por /: ').split('/')
            final = input('Digite a data final (DD/MM/YYYY) separado por /: ').split('/')
            
            """ print(inicial)
            print(final) """

            self.date_initial = dt.datetime(day=int(inicial[0]), month=(int(inicial[1])), year=int(inicial[2]))
            self.date_final = dt.datetime(day=int(final[0]), month=(int(final[1])), year=int(final[2]))

            if self.date_initial >= self.date_final:
                print('Datas inválidas. Digite novamente \n\n')
            else:
                trava = 1

        print('\n\n')

    def abrirPastaPadrao(self):
        pasta = self.pasta

        if os.path.exists(pasta) == False:
            os.makedirs(pasta)

        pasta2 = (f'./{pasta}/{self.name_app}')

        if os.path.exists(pasta2) == False:
            os.makedirs(pasta2)
        
        self.arquivos['Pasta'] = pasta2

    def selecionarPasta(self):
        trava = 0

        while(trava != 1):

            if( int(input('Deseja abrir uma pasta para salvar os dados? (1 - Sim, 0 - Não): ')) == 1 ):
                pasta = input('Digite o nome da pasta que deseja salvar os arquivos: ')
                pasta = './'+pasta
            
                try:
                    if os.path.exists(pasta) == False:
                        os.makedirs(pasta)
                    trava = 1
                except:
                    print('Pasta não aceita!')
                    trava = 0
            
            else:
                pasta = ''
                trava = 1

            

        self.arquivos['Pasta'] = pasta

    def dadosIniciais(self, indice, nome):
        return {
            "NameFile": nome,
            "NameAPP": self.name_app,
            "NameOfMicroService": self.microsservices[indice]['MS'],
            "Provider": self.microsservices[indice]['Prvd'],
            "Availability": self.microsservices[indice]['Ava'],
            "Cost": self.microsservices[indice]['Cost'],
            "ResponseTime": self.microsservices[indice]['RT'],
            "Data_Inicial": str(self.date_initial),
            "Data_Final": str(self.date_final),
            "Monitoring": [] 
        }
        
    def abrirArqDados(self):
        for indice, i in enumerate(self.microsservices):
            nome = (f'{self.name_app}_MS{i["MS"]}_P{i["Prvd"]}.json')
            if len(self.arquivos['Pasta']) > 0:
                nome = (f'{self.arquivos["Pasta"]}/{nome}')
            arq = open(nome, 'w')
            arq.close()
            aux = self.dadosIniciais(indice, nome)
            saveFinalFile(nome, aux)
            self.arquivos['NomesArqs'].append(nome)

    def selectCase(self):
        # Função que solicitará ao usuário que ele selecione os casos a serem gerados.
        print('-'*60)
        print(f'Selecionar o caso a ser gerado para o app >>{self.name_app}<<: ')
        print('-'*60)
        print('Caso 1 = Todos os requisitos são atendidos.')
        print('Caso 2 = Nenhum dos requisitos são atendidos.')
        print('Caso 3 = Caso Aleatório')
        print('Caso 4 = Escolher qual requisito nao atendera')
        print('Caso 5 = Escolher qual microsserviço nao atendera')
        print('-'*60)

        while(self.case < 1 or self.case > 5):
            self.case = int(input('Digite o caso desejado: '))
        
        print('-'*60)
        print()

    def vaiProCaso(self):
        # Função que verifica qual caso é o selecionado e em seguida chama a função referente ao caso.
        if self.case < 4:
            self.casos_basicos()
        elif self.case == 4:
            self.selecionarRequisito()
        elif self.case == 5:
            self.selecionarMicroServ()

    def casos_basicos(self):
        # Função chama as funções para a definição de limites.
        for i in range(len(self.microsservices)):
            if self.case == 1:
                # Melhor Caso
                self.microsservices[i]['limitesSel'] = self.melhorCaso(i)
            
            elif self.case == 2:
                # Pior Caso
                self.microsservices[i]['limitesSel'] = self.piorCaso(i)

            elif self.case == 3:
                # Aleatório
                self.microsservices[i]['limitesSel'] = self.aleatorio(i)

    def melhorCaso(self, indice):
        # Seleciona os limites referentes ao melhor caso.
        limites = {
            'Availability': {
                'Inicio': float(self.microsservices[indice]['Ava']), 
                'Final': 1.0
            },
            
            'Cost': {
                'Inicio': 0.001, 
                'Final': float(self.microsservices[indice]['Cost'])
            },
            
            'ResponseTime': {
                'Inicio': 0.001, 
                'Final': float(self.microsservices[indice]['RT'])
            }
        }

        return limites

    def piorCaso(self, indice):
        # Seleciona os limites referentes ao pior caso.
        limites = {
            'Availability': {
                'Inicio': 0.0, 
                'Final': float(self.microsservices[indice]['Ava'])
            },
            'Cost': {
                'Inicio': float(self.microsservices[indice]['Cost']), 
                'Final': float(self.microsservices[indice]['Cost']) * 3
            },
            'ResponseTime': {
                'Inicio': float(self.microsservices[indice]['RT']), 
                'Final': float(self.microsservices[indice]['RT']) * 3
            }
        }
        return limites

    def aleatorio(self, indice):
        # Seleciona os limites referentes ao pior caso.
        limites = {
            'Availability': {
                'Inicio': 0.0, 
                'Final': 1.0
            },
            'Cost': {
                'Inicio': 0.0, 
                'Final': float(self.microsservices[indice]['Cost']) * 2
            },
            'ResponseTime': {
                'Inicio': 0.0, 
                'Final': float(self.microsservices[indice]['RT']) * 2
            }
        }
        return limites

    def selecionarRequisito(self):
        print()
        print('-'*70)
        print('Selecione o(s) requisito(s) que não atendam: ')
        print('(Caso deseje mais de um requisito, separe por vírgula tipo: (1,3) )')
        print('-'*70)
        print('1 - Availability / Disponibilidade')
        print('2 - Cost / Custo')
        print('3 - Response Time / Tempo de Resposta')
        print('-'*70)

        tam = 0
        while( tam < 1 or tam > 3 ):
            op = input('Selecione as opções: ')
            lista = op.split(',')
            tam = len(lista)

        selecionados = [ int(x) for x in lista ]
        self.casos_requisitos(selecionados)
        print('\n\n')

    def casos_requisitos(self, selecionados):
        for indice, i in enumerate(self.microsservices):
            i['limitesSel'] = self.requisito(selecionados, indice)

    def requisito(self, selecionados, indice):
        limite = {}

        if( 1 in selecionados ):
            limite['Availability'] = {
                'Inicio':  0.0,
                'Final': float(self.microsservices[indice]['Ava'])
            }
        else:
            limite['Availability'] = {
                'Inicio': float(self.microsservices[indice]['Ava']),
                'Final': 1.0
            }

        if ( 2 in selecionados ):
            limite['Cost'] = {
                'Inicio': float(self.microsservices[indice]['Cost']), 
                'Final': float(self.microsservices[indice]['Cost']) * 3
            }
        else:
            limite['Cost'] = {
                'Inicio': 0.0001, 
                'Final': float(self.microsservices[indice]['Cost'])
            }
        
        if( 3 in selecionados ):
            limite['ResponseTime'] = {
                'Inicio': float(self.microsservices[indice]['RT']), 
                'Final': float(self.microsservices[indice]['RT']) * 3
            }
        else:
            limite['ResponseTime'] = {
                'Inicio': 0.001, 
                'Final': float(self.microsservices[indice]['RT'])
            }
        
        return limite


    def selecionarMicroServ(self):
        print('-'*75)
        print('Selecione o microsservico: ')
        print('-'*75)
        for i in self.microsservices:
            print(f"Microsservice: {i['MS']} - Prvd: {i['Prvd']}")
        print('-'*75)
        op = input('Selecione (caso deseje mais de 1 separe por vírgulas): ')

        lista = op.split(',')
        selecionados = []

        for j in lista:
            selecionados.append(int(j))
        
        print(selecionados)
        self.casos_microsservico(selecionados)
        

    def casos_microsservico(self, selecionados):
        for indice, i in enumerate(self.microsservices):
            i['limitesSel'] = self.limitarMS(selecionados, indice, i)


    def limitarMS(self, selecionados, indice, ms):
        
        if ms['MS'] in selecionados:
            retorno = self.piorCaso(indice)
        else:
            retorno = self.melhorCaso(indice)
        
        return retorno



    def montar(self):
        for indice, i in enumerate(self.microsservices):
            
            aux = copy.deepcopy(self.date_initial)
            
            nome = self.arquivos['NomesArqs'][indice]
            arq = loadFile(nome)
            
            print(f"Gerando para o microsserviço: {self.microsservices[indice]['MS']}")

            while( compareDate(aux, self.date_final) == False ):
                arq = self.gerar(arq, i, aux)
                aux = avancaTempo(aux, self.intervalo)
            
            saveFinalFile(nome, lido=arq)
            """ print() """

    def gerar(self, arq, ms, data):

        ava = random.uniform( 
            ms['limitesSel']['Availability']['Inicio'], 
            ms['limitesSel']['Availability']['Final'] 
        )

        cost = random.uniform(
            ms['limitesSel']['Cost']['Inicio'], 
            ms['limitesSel']['Cost']['Final'] 
        )

        rt = random.uniform(
            ms['limitesSel']['ResponseTime']['Inicio'], 
            ms['limitesSel']['ResponseTime']['Final'] 
        )

        ava = round(ava, 2)
        cost = round(cost, 2)
        rt = round(rt, 2)

        arq['Monitoring'].append(
            {
                'Date': str(data.date()),
                'Time': str(data.time()),
                'Availability': ava,
                'Cost': cost,
                'ResponseTime': rt
            }
        )

        return arq

    def salvarArqGestao(self):
        nome = self.arquivos['Pasta']+'/gestao.json'

        if self.case == 1:
            self.arquivos['Case'] = [1, 'Melhor Caso']
        elif self.case == 2:
            self.arquivos['Case'] = [2, 'Pior Caso']
        elif self.case == 3:
            self.arquivos['Case'] = [3, 'Caso Aleatorio']
        elif self.case == 4:
            self.arquivos['Case'] = [4, 'Requisito selecionado']
        elif self.case == 5:
            self.arquivos['Case'] = [5, 'Microsservico selecionado']

        saveFinalFile(nameARQ=nome, lido=self.arquivos)

