from deap import base, tools
from deap import algorithms

import data_management as dm
import algorithm_config as ConfiguracionSolucion
import individual_evaluation as ie
import matplotlib.pyplot as plt
import numpy as np 


def configuraEstadisticasEvolucion():

    # Se configura que estadísticas se quieren analizar sobre la evolucion
    # We set up which statistics you want to analyse on the evolution
    stats = tools.Statistics(lambda ind: ind.fitness.values) 
    stats.register("avg", np.mean) 
    stats.register("std", np.std) 
    stats.register("min", np.min) 
    stats.register("max", np.max) 
    
    return stats

def visualizaGrafica(log):

    # Se recuperan los datos desde el log
    # Data is retrieved from the log
    gen = log.select("gen")
    avgs = log.select("avg")
    
    # Se establece una figura para dibujar
    # A figure is set to draw
    fig, ax1 = plt.subplots()
    
    # Se representa la media del valor de fitness por cada generación
    # The average fitness value is plotted for each generation.
    line1 = ax1.plot(gen, avgs, "r-", label="Average Fitness")    
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness", color="b")
    
    ''' Notad que se deberían representar mas cosas. Por ejemplo el maximo y el minimo de ese fitness se están recogiendo en las estadisticas, aunque en el ejemplo no se representen '''
    ''' Note that additional information should be represented. For example, the maximum and minimum of that fitness are being collected in the statistics, although in the example they are not represented'''

    plt.show()

def realizaEvolucion(stats):
    # Se configura cómo se define cada individuo, la población y la configuración del algoritmo
    toolbox = ConfiguracionSolucion.configure_solution()
    
    # Se configuran los parámetros del algoritmo genético
    params = ConfiguracionSolucion.configure_param()
    
    # Se inicializa la poblacion con 300 individuos
    population = toolbox.population(n=params['PSIZE'])
    
    # Se llama al algoritmo que permite la evolucion de las soluciones
    population, logbook = algorithms.eaSimple(population, toolbox, 
	                               cxpb=params['CXPB'], mutpb=params['MUTPB'], # Probabilidades de cruce y mutacion
	                               ngen=params['NGEN'], verbose=False, stats=stats) # Numero de generaciones a completar y estadisticas a recoger
    
    # Por cada generación, la estructura de logbook va almacenando un resumen de los avances del algoritmo.
    print("El resultado de la evolución es: ")
    print(logbook)

    # Comprobamos cual es la mejor solucion encontrada por evolucion
    best_solution = tools.selBest(population,1)[0]
    print("La mejor solucion encontrada es: ")
    print(best_solution)
    
    return logbook, best_solution

if __name__ == "__main__":
    file = "./qualification_round_2018.in/a_example.in"
    dm.load(file)
    stats = configuraEstadisticasEvolucion()
    log, best_solution = realizaEvolucion(stats)
    print("Fenotipo:")
    print(ie.fenotype(best_solution)[1])
    visualizaGrafica(log)
