def compareDate(initial_date, final_date):
    # Para quando a data fica igual e o tempo fica maior ou igual
    if (initial_date.date() == final_date.date()) and (initial_date.time() >= final_date.time()): 
        retorno = True
    else:
        retorno = False
    return retorno