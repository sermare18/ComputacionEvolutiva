import random

from deap import base
from deap import creator
from deap import tools

import global_def as gd
import individual_evaluation as so_eval
import data_management as dm

toolbox = base.Toolbox()
logbook = tools.Logbook()

def attr(index):
    row = index // gd.num_cols
    col = index % gd.num_cols
    
    if row == gd.br and col == gd.bc:
        return 2
    
    if gd.grid[row, col] != 4:
        return 0
    else:
        # Verificar las celdas vecinas
        vecinos = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        hay_cable_vecino = any((r, c) == (gd.br, gd.bc) for r, c in vecinos if 0 <= r < gd.num_rows and 0 <= c < gd.num_cols)        
        if not hay_cable_vecino:
            return 0

        # Generar un número aleatorio entre 0 y 1
        r = random.random()
        # Devolver 2 (cables) con una probabilidad del 60%, 1 (routers) con una probabilidad del 30% y 0 (nada) con una probabilidad del 10%
        if r < 0.6:
            return 2
        elif r < 0.9:
            return 1
        else:
            return 0


def attr_generator():
    return (attr(i) for i in range(gd.num_rows * gd.num_cols))

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
    toolbox.register("attr_generator", attr_generator)
    # Structure initializers
    ''' El individuo se crea como una lista (o repeticion) de "attribute", definido justo antes. Tendrá una longitud igual al numero de celdas en el grid'''
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_generator)
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
    
    params['NGEN'] = 100
    params['PSIZE'] = 50
    params['CXPB'] = 0.8
    params['MUTPB'] = 0.1
    
    return params

if __name__ == "__main__":
    file = "./Router-placement/qualification_round_2017.in/mini_example.in"
    dm.load(file)
    toolbox = configure_solution()
    params = configure_param()
    
    # Generar un individuo
    individual = toolbox.individual()

    # Evaluar el fitness del individuo
    fitness = toolbox.evaluate(individual)

    # Imprimir el individuo y su fitness
    print("Individuo:", individual)
    print("Fitness:", fitness)
