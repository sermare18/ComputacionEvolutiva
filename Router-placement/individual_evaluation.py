import numpy as np
import global_def as gd
import data_management as dm

def evaluar_individuo(individual):
    # Convertir el individuo a una matriz 2D para facilitar el manejo
    grid = np.array(individual).reshape(gd.num_rows, gd.num_cols)
    
    routers_conectados, routers_no_conectados, num_routers, num_fibra = esta_conectado(grid)
    
    # Verificar que no se ha puesto ningún router dentro de alguna pared
    for pos_router in routers_conectados + routers_no_conectados:
        r, c = pos_router
        if gd.grid[r][c] == 3:
            return -np.inf,
    
    # Verificar si los routers y cables backbone están correctamente conectados
    if len(routers_conectados) == 0:
        return -np.inf,

    num_celdas_cubiertas = 0
    # Calcular el alcance de cada router bien conectados
    for pos_router in routers_conectados:
        num_celdas_cubiertas += calcular_zona_cubierta(pos_router[0], pos_router[1])

    fiber_cost = num_fibra * gd.price_backbone
    router_cost = num_routers * gd.price_router
    # Calcular el costo total de los routers y cables backbone colocados
    costo_total = fiber_cost + router_cost

    # Si el costo total excede el presupuesto, devolver -np.inf
    if costo_total > gd.budget:
        return -np.inf,

    # Calcular la puntuación
    puntuacion = num_celdas_cubiertas * 1000 + (gd.budget - costo_total)

    return puntuacion,


def esta_conectado(grid_individual):
    # Crear una matriz para marcar las celdas visitadas
    visitado = np.zeros((gd.num_rows, gd.num_cols), dtype=bool)
    
    # Iniciar la búsqueda en profundidad desde el punto inicial
    stack = [(gd.br, gd.bc)]
    while stack:
        r, c = stack.pop()
        if not visitado[r, c] and (grid_individual[r, c] == 2 or grid_individual[r, c] == 1):
            visitado[r, c] = True
            # Agregar las celdas vecinas a la pila
            if r > 0: stack.append((r - 1, c))
            if r < gd.num_rows - 1: stack.append((r + 1, c))
            if c > 0: stack.append((r, c - 1))
            if c < gd.num_cols - 1: stack.append((r, c + 1))
    
    # Crear listas para los routers conectados y no conectados
    routers_conectados = []
    routers_no_conectados = []
    num_total_routers = 0
    num_total_fibra = 0
    # Verificar si todos los routers están conectados al punto inicial
    for r in range(gd.num_rows):
        for c in range(gd.num_cols):
            if grid_individual[r, c] == 1:
                num_total_routers += 1
                if visitado[r, c]:
                    routers_conectados.append((r, c))
                else:
                    routers_no_conectados.append((r, c))
            if grid_individual[r, c] == 2:
                num_total_fibra += 1

    return routers_conectados, routers_no_conectados, num_total_routers, num_total_fibra

def calcular_zona_cubierta(r, c):
    # Crear una lista para almacenar las celdas cubiertas
    celdas_cubiertas = []

    # Recorrer todas las celdas dentro del rango del router
    for x in range(max(0, r - gd.radius_router), min(gd.num_rows, r + gd.radius_router + 1)):
        for y in range(max(0, c - gd.radius_router), min(gd.num_cols, c + gd.radius_router + 1)):
            # Verificar si la celda está cubierta por el router
            if abs(r - x) <= gd.radius_router and abs(c - y) <= gd.radius_router:
                # Verificar si no hay una pared dentro del rectángulo que encierra a [r, c] y [x, y] y que la celda que cubre sea una target cell (4)
                if not hay_pared(r, c, x, y) and gd.grid[x, y] == 4:
                    celdas_cubiertas.append((x, y))

    return len(celdas_cubiertas)

def hay_pared(r1, c1, r2, c2):
    # Recorrer todas las celdas dentro del rectángulo que encierra a [r1, c1] y [r2, c2]
    for x in range(min(r1, r2), max(r1, r2) + 1):
        for y in range(min(c1, c2), max(c1, c2) + 1):
            # Verificar si la celda es una pared
            if gd.grid[x][y] == 3:
                return True

    return False


'''
La función fenotype(individual) toma una lista de enteros individual que representa una solución al problema de asignación de viajes 
a vehículos. Cada entero en individual representa el vehículo asignado a un viaje específico. 
El valor 0 significa que el viaje no se atiende.
EJEMPLO
El individuo [1, 2, 1] significa que el primer y tercer viaje están asignados al vehículo 1, 
y el segundo viaje está asignado al vehículo 2. 
'''
def fenotype(individual):
    # Crear una matriz vacía para el fenotipo
    fenotipo = [[' ' for _ in range(gd.num_cols)] for _ in range(gd.num_rows)]
    
    # Recorrer el genotipo
    for i, gen in enumerate(individual):
        # Convertir el índice lineal en un índice bidimensional
        fila = i // gd.num_cols
        columna = i % gd.num_cols

        # Si el gen es 2, hay un cable de fibra óptica en esta celda
        if gen == 2:
            fenotipo[fila][columna] = 'C'  # C de Cable

        # Si el gen es 1, hay un router en esta celda
        elif gen == 1:
            fenotipo[fila][columna] = 'R'  # R de Router

    # Imprimir el fenotipo
    for fila in fenotipo:
        print(' '.join(fila))


if __name__ == "__main__":
    
    file = "./Router-placement/qualification_round_2017.in/mini_example.in"
    dm.load(file)
    
    indiv = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    print('fitness ejemplo',evaluar_individuo(indiv))
    
    print(fenotype(indiv))
