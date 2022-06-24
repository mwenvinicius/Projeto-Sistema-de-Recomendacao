from datetime import datetime
from gerador2 import Gerador
from arquivo import *
from horarios import *

namesArqs = [
    'Result-Data.json'
]

for i in namesArqs:

    results = loadFile(f'../L01/Results/{i}')

    date_initial = datetime(year=2022, month=5, day=20)
    date_final = datetime(year=2022, month=5, day=21)

    for index, app in enumerate(results):
        a = Gerador(
            indice=index,
            pasta=(f'../L01/monitoring'),
            intervalo=15,
            result=app,
            case=3,
            date_initial=date_initial,
            date_final=date_final
        )

        a.abreArq()
        a.abrirPastaPadrao()
        a.abrirArqDados()
        a.vaiProCaso()
        a.salvarArqGestao()
        print(f"APP: {a.name_app}")
        a.montar()