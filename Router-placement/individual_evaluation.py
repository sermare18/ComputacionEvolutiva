import numpy as np
import global_def as gd
import data_management as dm

def fitness(individual):
    routers_positions = [i for i, gene in enumerate(individual) if gene]
    routers_cost = len(routers_positions) * gd.price_router
    fiber_cells = set()
    
    # Inicializar fibra óptica desde el punto inicial
    initialize_fiber(individual, (gd.br, gd.bc), fiber_cells)
    
    for router_position in routers_positions:
        # Agregar las celdas cubiertas por el router a la fibra óptica
        fiber_cells.update(get_cells_covered(router_position, individual))
        
    fiber_cost = len(fiber_cells) * gd.price_backbone
    total_cost = routers_cost + fiber_cost
    remaining_budget = gd.budget - total_cost
    
    # Each submission earns 1000 points for each target cell covered with Internet access and 1 point for each unit of remaining budget.
    points = len(fiber_cells) * POINTS_PER_CELL + remaining_budget * POINTS_PER_BUDGET

    return points,

# Función para obtener las celdas cubiertas por un router
def get_cells_covered(router_position, individual):
    covered_cells = set()
    x, y = router_position % gd.num_cols, router_position // gd.num_cols

    for i in range(x - gd.radius_router, x + gd.radius_router + 1):
        for j in range(y - gd.radius_router, y + gd.radius_router + 1):
            if 0 <= i < gd.num_cols and 0 <= j < gd.num_rows and not is_wall(i, j, individual):
                covered_cells.add(j * gd.num_cols + i)

    return covered_cells

# Función para inicializar la fibra óptica desde el punto inicial
def initialize_fiber(individual, initial_point, fiber_cells):
    initial_index = initial_point[1] * gd.num_cols + initial_point[0]
    individual[initial_index] = 1  # Conectar la celda inicial a la fibra óptica
    fiber_cells.add(initial_index)
    
# Función para verificar si una celda es una pared
def is_wall(x, y, individual):
    index = y * gd.num_cols + x
    return individual[index] == 0  # 0 representa una pared

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
    
    file = "./qualification_round_2018.in/a_example.in"
    dm.load(file)
    
    indiv = [1, 2, 2]
    
    print('fitness ejemplo',fitness(indiv))
