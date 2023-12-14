# -*- coding: utf-8 -*-
import random

from deap import base
from deap import creator

from deap import tools

import global_def as gd
import individual_evaluation as mo_eval

toolbox = base.Toolbox()
logbook = tools.Logbook()

def configure_solution_const():
    
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_int", random.randint, 0, gd.num_vehic)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, gd.num_rides)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", mo_eval.fitness)
    toolbox.decorate("evaluate", tools.DeltaPenalty(mo_eval.feasible, 7.0, mo_eval.distance))
    
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox


def configure_solution_mo():

    creator.create("FitnessMixed", base.Fitness, weights=(1.0,-1.0))
    creator.create("Individual", list, fitness=creator.FitnessMixed)

    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_int", random.randint, 0, gd.num_vehic)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, gd.num_rides)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", mo_eval.fitness_complete)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)
    toolbox.register("select", tools.selSPEA2)
    # toolbox.register("select", tools.selSPEA2())    
    
    return toolbox
 
def configure_param():
    
    params = {}
    
    params['NGEN'] = 100
    params['PSIZE'] = 50
    params['CXPB'] = 0.75
    params['MUTPB'] = 0.1
    
    return params