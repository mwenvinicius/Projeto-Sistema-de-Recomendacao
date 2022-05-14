from dateutil import rrule

def compareDate(initial_date, final_date):
    # Esta função retorna True se a data inicial chegou na data final.
    if (initial_date.date() == final_date.date()) and (initial_date.time() >= final_date.time()): 
        retorno = True
    else:
        retorno = False
    return retorno


def avancaTempo(inicial, intervalo):
    inicial = rrule.rrule( 
        rrule.MINUTELY, 
        interval=intervalo, 
        dtstart=inicial, 
        count=2)[1]
    return inicial