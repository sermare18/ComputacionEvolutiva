# -*- coding: utf-8 -*-
import numpy as np

import global_def as gd

# Mono-Objective
def fitness (individual):
    (fit_times, unadapted) = fitness_complete (individual)
    return fit_times,

def fitness_comb (individual):
    (fit_times, unadapted) = fitness_complete (individual)
    
    return fit_times - (10 * unadapted)

# Constraint Handling
def feasible(individual):
    (fit_times, unadapted) = fitness_complete (individual)
    return unadapted == 0

def distance(individual):
    (fit_times, unadapted) = fitness_complete (individual)
    return unadapted
    
# Multi-Objective
def fitness_complete (individual):

    fit = 0
    unadapted = 0
    
    (rides_vehicle, s) = fenotype(individual)
    
    #Para cada vehiculo (saltando el 0, que implica 'no se realiza el viaje'):
    for v in range(gd.num_vehic+1):
        # Recuperamos del individuo todas las posiciones con su id (son los viajes que se le asignan)
        #r_vehic = [i for i, x in enumerate(individual) if x == (v+1)]
        # Reordenamos los viajes en funcion de su hora de inicio
        #r_vehic = order_by_start(r_vehic)
        r_vehic = rides_vehicle[v]
    
        # Todos los coches empiezan en al punto (0,0) al incio
        current_pos = (0,0)
        current_time = 0
        for r in r_vehic:
            # Tiempo hasta alcanzar el punto de inicio
            t_ini = travel_time(current_pos,gd.rides[r,[0,1]])
            current_time = current_time + t_ini
            # Tiempo de espera hasta recoger al cliente
            early_by = gd.rides[r,4] - current_time
            if(early_by > 0): # Si llega antes, tiene que esperar
                current_time = gd.rides[r,4]
                fit = fit + gd.bonus # Si llega antes, tiene bonus
            # Tiempo de viaje hasta el destino
            t_end = travel_time(gd.rides[r,[0,1]],gd.rides[r,[2,3]])
            current_time = current_time = current_time + t_end
            current_pos = gd.rides[r,[2,3]]
            
            # Si no hay más pasos en la simulación, no se sigue comprobando
            if(current_time >= gd.num_steps):
                break;

            # Si llega antes de lo solicitado, tiene bonus
            if(current_time < gd.rides[r,5]):
                fit = fit + travel_time(gd.rides[r,[0,1]],gd.rides[r,[2,3]])

            if (gd.rides[r,6] == 1) and (gd.adapted[v-1] == 0):
                unadapted = unadapted+1

    return fit,unadapted

def order_by_start(rides):
    order = np.argsort(gd.rides[rides,4])
    rides_o = []
    for o in order:
        rides_o.append(rides[o])
    
    return rides_o
    

def travel_time(ini, end):
    return abs(ini[0]-end[0])+abs(ini[1]-end[1])


## 
def fenotype (individual):

    # Se considera que el vehículo 0 significa no atender a ese viaje
    # La posicion 0 no tendrá por lo tanto asignados nunca ninguno
    rides_assigned = [[]]
    s = ''
    
    for v in range(gd.num_vehic):
        r_vehic = [i for i, x in enumerate(individual) if x == (v+1)]
        r_vehic = order_by_start(r_vehic)
        rides_assigned.append(r_vehic)

        s = s + "Vehicle {} has assigned rides: {}\n".format((v+1),str(r_vehic))

#    print(s)
#    print(rides_assigned)
    
    return rides_assigned, s


if __name__ == "__main__":
    
    import data_management as dm
    file = "./qualification_round_2018.in/a_example_sp.in"
    dm.load_mo(file)
    
    indiv = [1, 2, 2]
    
    print('fitness single obj:',fitness(indiv))
    print('fitness combinado:',fitness_comb(indiv))
    print('fitness multi-obj:',fitness_complete(indiv))
