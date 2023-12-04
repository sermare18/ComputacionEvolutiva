import numpy as np
import global_def as gd
import data_management as dm

def evaluar_individuo(individual):
    # Convertir el individuo a una matriz 2D para facilitar el manejo
    grid = np.array(individual).reshape(gd.num_rows, gd.num_cols)
    
    num_celdas_cubiertas = calcular_cubrimiento_routers(grid)
    # Conectar los routers con el punto inicial de fibra
    celdas = conectar_routers(grid)
    num_routers = len(celdas)
    celdas_no_repetidas = set(sum(celdas, []))
    num_fibra = len(celdas_no_repetidas)

    # print("\n")
    # print(f'El número total de elementos en la lista "celdas" es: {sum(len(sublista) for sublista in celdas)}')
    # print("Celdas no repetidas: ", len(celdas_no_repetidas))
    # print(celdas)
    # print("-------------------------------------------")
    # print(celdas_no_repetidas)
    
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

def connect_cells(router, cable):
    x1, y1 = router
    x2, y2 = cable
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    sx, sy = 1 if x1 < x2 else -1, 1 if y1 < y2 else -1
    err = dx - dy
    x, y = x1, y1
    cells = []

    while x != x2 or y != y2:
        cells.append((x, y))
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    cells.append((x, y)) 
    
    return cells

def conectar_routers(grid_individual):
    celdas_a_conectar = []
    for r in range(len(grid_individual)):
        for c in range(len(grid_individual[0])):
            if grid_individual[r][c] == 1:
                 celdas_a_conectar.append(connect_cells((r, c), (gd.br, gd.bc)))
    return celdas_a_conectar

def calcular_cubrimiento_routers(grid_individual):
    num_celdas_cubiertas = 0
    for r in range(len(grid_individual)):
        for c in range(len(grid_individual[0])):
            if grid_individual[r][c] == 1:
                 num_celdas_cubiertas += calcular_zona_cubierta(r, c)
    return num_celdas_cubiertas

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


def fenotype(individual):
    # Convertir el individuo a una matriz 2D
    grid = np.array(individual).reshape(gd.num_rows, gd.num_cols)

    # Conectar los routers con el punto inicial de fibra
    celdas = conectar_routers(grid)
    
    celdas_no_repetidas = set(sum(celdas, []))

    # Escribir el archivo de salida
    with open('output.txt', 'w') as archivo:
        archivo.write(f'Número de routers: {len(celdas)}\n')
        archivo.write(f'Número de fibra: {len(celdas_no_repetidas)}\n\n')
        archivo.write('En cada fila de a continuación, se representa el cableado de la red.\nLa primera celda es la posicion del router y la última celda es la posición del primer punto de fibra.\n')
        for i, lista in enumerate(celdas, 1):
            archivo.write(f'Cableado {i}: {str(lista)}\n')

if __name__ == "__main__":
    
    
    file = "./Router-placement/qualification_round_2017.in/small_example.in"
    dm.load(file)
    
    indiv_mini_example = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    indiv_small_example = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    print('fitness ejemplo',evaluar_individuo(indiv_small_example))