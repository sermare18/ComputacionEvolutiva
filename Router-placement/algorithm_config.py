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
    
    # Calcular el número máximo de routers que se pueden colocar
    max_routers = int(gd.budget / gd.price_router)
    
    # Calcular el número máximo de celdas que se pueden cablear
    max_celdas = gd.num_celdas_objetivo + gd.num_celdas_pared
    
    # Calcular el número máximo de routers que se pueden colocar con el presupuesto restante después de cablear todas las celdas
    routers_restantes = int((gd.budget - max_celdas * gd.price_backbone) / gd.price_router)

    # En la posicion del cable principal no colocamos routers
    if row == gd.br and col == gd.bc:
        return 0
    
    # En las celdas de pared (#) y celdas vacías (-) no colocamos routers
    if gd.grid[row, col] != 4:
        return 0
    else:
        # Generar un número aleatorio entre 0 y 1
        r = random.random()
        # Devolver 1 (router) con una probabilidad del 5%, 0 (nada) con una probabilidad del 95%
        if r < 0.05 and gd.contador_routers < routers_restantes:
            gd.contador_routers += 1;
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
    
    params['NGEN'] = 20
    params['PSIZE'] = 50
    params['CXPB'] = 0.8
    params['MUTPB'] = 0.1
    
    return params

if __name__ == "__main__":
    file = "./Router-placement/qualification_round_2017.in/charleston_road.in"
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
    print(gd.contador_routers)