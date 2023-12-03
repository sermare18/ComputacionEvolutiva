import random

from deap import base
from deap import creator
from deap import tools

import global_def as gd
import individual_evaluation as so_eval

toolbox = base.Toolbox()
logbook = tools.Logbook()

def attr():
    # Generar un número aleatorio entre 0 y 1
    r = random.random()
    # Devolver 0 con una probabilidad del 70%, 1 con una probabilidad del 20% y 2 con una probabilidad del 10%
    if r < 0.7:
        return 0
    elif r < 0.9:
        return 1
    else:
        return 2


def configure_solution():
    ''' 
    Se configura el fitness que se va a emplear en los individuos
	 En este caso se configura para:
	    1.buscar un único objetivo: es una tupla de solo un numero
	    2.maximizar ese objetivo (se multiplica por un num. positivo)
    '''
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    
    ''' Se configura el individuo para que utilice la descripción anterior de fitness dentro de los individuos '''
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    # Attribute generator
    # 0 -> En esa celda no se coloca ni router ni backbone
    # 1 -> En esa celda se coloca un router
    # 2 -> En esa celda se coloca un cable backbone
    toolbox.register("attr", attr)
    # Structure initializers
    ''' El individuo se crea como una lista (o repeticion) de "attribute", definido justo antes. Tendrá una longitud igual al numero de celdas en el grid'''
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr, n=gd.num_rows * gd.num_cols)
    ''' La población se crea como una lista de "individual", definido justo antes'''
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", so_eval.evaluar_individuo)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
#    toolbox.register("select", tools.selRoulette)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    return toolbox

def configure_param():    
    
    params = {}
    
    params['NGEN'] = 1000
    params['PSIZE'] = 50
    params['CXPB'] = 0.8
    params['MUTPB'] = 0.5
    
    return params