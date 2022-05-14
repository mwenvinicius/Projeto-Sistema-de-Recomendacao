import copy
import json
import datetime as dt
from dateutil import rrule
import random
import os

from scipy import rand

from arquivo import *
from horarios import *



class Monitoramento():

    def __init__(self):
        self.date_initial = None #........ Data inicial do monitoramento
        self.date_final = None #.......... Data final do monitoramento
        self.monitoramento = None #....... Aqui será guardado o monitoramento
        self.name_app = None #............ Nome do app;
        self.microsservices = None #...... Microsserviços extraídos do arquivo result;
        self.pasta = None #............... Pasta onde será salvo o caminho;
        self.case = 0 #................... Caso a ser gerado que será selecionado na função selectCase()
        self.result = None #.............. Aqui estarão os dados do arquivo resultData.json 
        self.intervalo = 15 #............. Intervalo em minutos, setado em 15 minutos.
        self.arquivos = {
            'Pasta': '',
            'NomesArqs': [] } #........... Aqui serão salvos as informações sobre os arquivos de salvamento.
        
        self.sequencia() #................ Faz a chamada das funções.

    def sequencia(self):
        self.abreArq()
        self.selecionarIntervalo()
        self.selecionarDatas()
        self.selecionarPasta()
        self.abrirArqDados()
        self.selectCase()
        self.vaiProCaso()
        self.montar()
        self.salvarArqGestao()
        print(self.date_initial, self.date_final)
        for i in self.microsservices:
            print(i)
        
    def abreArq(self):
        # Função que abre o arquivo result e transfere seus dados aos atributos da classe
        self.result = loadFile('resultData.json')[0]
        self.name_app = self.result["App"]
        self.microsservices = [ i for i in self.result['Resultados'] ] # For que coloca os Micro
        
        for i in self.microsservices:
            print(i) 

        print()

    def selecionarIntervalo(self):
        self.intervalo = int(input('Digite o intervalo (em min): '))

    def selecionarDatas(self):
        # Função que solicitará ao usuario que ele digite as datas, tanto a inicial como a final.
        print('-'*60)
        print('\tSelecionar datas: ')
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

    def selecionarPasta(self):
        trava = 0

        while(trava != 1):

            if( int(input('Deseja selecionar a pasta (1 - Sim, 0 - Não): ')) == 1 ):
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
        print('\tSelecionar o caso a ser gerado: ')
        print('-'*60)
        print('Caso 1 = Todos os requisitos são atendidos.')
        print('Caso 2 = Nenhum dos requisitos são atendidos.')
        print('Caso 3 = Caso Aleatório')
        print('Caso 4 = Escolher qual requisito não atenderá')
        print('-'*60)

        while(self.case < 1 or self.case > 4):
            self.case = int(input('Digite o caso desejado: '))
        
        print('-'*60)
        print()

    def vaiProCaso(self):
        # Função que verifica qual caso é o selecionado e em seguida chama a função referente ao caso.
        if self.case < 4:
            self.casos_basicos()
        elif self.case == 4:
            self.selecionarRequisito()
        else:
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
        pass

    def montar(self):
        for indice, i in enumerate(self.microsservices):
            
            aux = copy.deepcopy(self.date_initial)
            
            while( compareDate(aux, self.date_final) == False ):
                
                print(aux, end='---- ')
                print(indice)

                nome = self.arquivos['NomesArqs'][indice]
                arq = loadFile(nome)
                arq = self.gerar(arq, i, aux)
                saveFinalFile(nome, lido=arq)

                aux = avancaTempo(aux, self.intervalo)
            print()

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
        saveFinalFile(nameARQ=nome, lido=self.arquivos)



if __name__ == '__main__':
    Monitoramento()