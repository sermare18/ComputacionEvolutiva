import random

from deap import base
from deap import creator
from deap import tools

import global_def as gd
import individual_evaluation as so_eval

toolbox = base.Toolbox()
logbook = tools.Logbook()

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
    toolbox.register("attr", random.randint, 1, 3)
    # Structure initializers
    ''' El individuo se crea como una lista (o repeticion) de "attribute", definido justo antes. Tendrá una longitud igual al numero de celdas en el grid'''
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr, n=gd.num_rows * gd.num_cols)
    ''' La población se crea como una lista de "individual", definido justo antes'''
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", so_eval.fitness)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
#    toolbox.register("select", tools.selRoulette)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    return toolbox

def configure_param():    
    
    params = {}
    
    params['NGEN'] = 50
    params['PSIZE'] = 50
    params['CXPB'] = 0.8
    params['MUTPB'] = 0.1
    
    return params