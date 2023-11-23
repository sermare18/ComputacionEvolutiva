import numpy as np
import global_def as gd
import data_management as dm

def fitness(individual):
    fit = 0
    (rides_vehicle, s) = fenotype(individual)
    
    # Para cada vehículo (saltando el 0, que implica 'no se realiza el viaje'):
    for v in range(gd.num_vehic + 1):
        # Recuperamos del individuo todas las posiciones con su id (son los viajes que se le asignan)
        #r_vehic = [i for i, x in enumerate(individual) if x == (v+1)]
        # Reordenamos los viajes en funcion de su hora de inicio
        #r_vehic = order_by_start(r_vehic)
        r_vehic = rides_vehicle[v]
        
        # Todos los coches empiezan en el punto (0,0) al inicio
        current_pos = (0, 0)
        current_time = 0
        for r in r_vehic:
            # Tiempo hasta alcanzar el punto de inicio
            t_ini = travel_time(current_pos, gd.rides[r,[0,1]])
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
            
            # Si se completa el viaje antes de la hora de fin,
            # se tiene una puntuación por la distancia completada
            if(current_time < gd.rides[r,5]):
                fit = fit + travel_time(gd.rides[r,[0,1]],gd.rides[r,[2,3]])
            
    return fit,

# Función devuelve los viajes ordenados en función de su earliest start
def order_by_start(rides):
    order = np.argsort(gd.rides[rides,4])
    rides_o = []
    for o in order:
        rides_o.append(rides[o])
    
    return rides_o

# Función que devuelve el tiempo de viaje
def travel_time(ini, end):
    return abs(ini[0]-end[0])+abs(ini[1]-end[1])

'''
La función fenotype(individual) toma una lista de enteros individual que representa una solución al problema de asignación de viajes 
a vehículos. Cada entero en individual representa el vehículo asignado a un viaje específico. 
El valor 0 significa que el viaje no se atiende.
EJEMPLO
El individuo [1, 2, 1] significa que el primer y tercer viaje están asignados al vehículo 1, 
y el segundo viaje está asignado al vehículo 2. 
'''
def fenotype(individual):
    # Se considera que el vehículo 0 significa no atender a ese viaje
    # La posición 0no tendrá por lo tanto asignados nunca ninguno
    
    # Inicializa una lista de listas, donde cada lista interna representará los viajes asignados a un vehículo específico. La primera lista interna está vacía porque el vehículo 0 significa que el viaje no se atiende.
    rides_assigned = [[]]
    # Inicializa una cadena vacía s que se utilizará para almacenar una descripción textual de las asignaciones de viajes.
    s = ''
    
    for v in range(gd.num_vehic):
        r_vehic = [i for i, x in enumerate(individual) if x == (v + 1)]
        r_vehic = order_by_start(r_vehic)
        rides_assigned.append(r_vehic)
        
        s = s + "Vehicle {} has assigned rides: {}\n".format((v+1),str(r_vehic))
        
    return rides_assigned, s

if __name__ == "__main__":
    
    file = "./Self-driving rides/qualification_round_2018.in/a_example.in"
    dm.load(file)
    
    indiv = [1, 2, 2]
    
    print('fitness ejemplo',fitness(indiv))
