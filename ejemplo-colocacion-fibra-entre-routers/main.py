import numpy as np

def esta_conectado(grid, br, bc, num_rows, num_cols):
    # Crear una matriz para marcar las celdas visitadas
    visitado = np.zeros((num_rows, num_cols), dtype=bool)

    # Iniciar la búsqueda en profundidad desde el punto inicial
    stack = [(br, bc)]
    while stack:
        r, c = stack.pop()
        if not visitado[r, c] and (grid[r, c] == 2 or grid[r, c] == 1):
            visitado[r, c] = True
            # Agregar las celdas vecinas a la pila
            if r > 0: stack.append((r - 1, c))
            if r < num_rows - 1: stack.append((r + 1, c))
            if c > 0: stack.append((r, c - 1))
            if c < num_cols - 1: stack.append((r, c + 1))

    # Crear listas para los routers conectados y no conectados
    routers_conectados = []
    routers_no_conectados = []

    # Verificar si todos los routers están conectados al punto inicial
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r, c] == 1:
                if visitado[r, c]:
                    routers_conectados.append((r, c))
                else:
                    routers_no_conectados.append((r, c))

    print(visitado);
    return routers_conectados, routers_no_conectados

def calcular_zona_cubierta(grid, r, c, R, num_rows, num_cols):
    # Crear una lista para almacenar las celdas cubiertas
    celdas_cubiertas = []

    # Recorrer todas las celdas dentro del rango del router
    for x in range(max(0, r - R), min(num_rows, r + R + 1)):
        for y in range(max(0, c - R), min(num_cols, c + R + 1)):
            # Verificar si la celda está cubierta por el router
            if abs(r - x) <= R and abs(c - y) <= R:
                # Verificar si no hay una pared dentro del rectángulo que encierra a [r, c] y [x, y]
                if not hay_pared(grid, r, c, x, y):
                    celdas_cubiertas.append((x, y))

    return celdas_cubiertas

def hay_pared(grid, r1, c1, r2, c2):
    # Recorrer todas las celdas dentro del rectángulo que encierra a [r1, c1] y [r2, c2]
    for x in range(min(r1, r2), max(r1, r2) + 1):
        for y in range(min(c1, c2), max(c1, c2) + 1):
            # Verificar si la celda es una pared
            if grid[x][y] == '#':
                return True

    return False

'''
# Crear un grid de prueba
grid = np.zeros((5, 5), dtype=int)
br = 0
bc = 0

# Colocar algunos routers y cables backbone en el grid
grid[br, bc] = 2  # Punto inicial
grid[br + 1, bc] = 2  # Cable backbone conectado al punto inicial
grid[br + 1, bc + 1] = 1  # Router conectado al cable backbone
grid[br + 2, bc + 2] = 1  # Router no conectado

# Llamar a la función esta_conectado
routers_conectados, routers_no_conectados = esta_conectado(grid, 0, 0, 5, 5);

# Imprimir los resultados
print(grid)
print("Routers conectados:", routers_conectados)
print("Routers no conectados:", routers_no_conectados)
'''

# Crear un grid de prueba
grid = [
    ['-', '-', '-', '-', '-'],
    ['-', '#', '-', '-', '-'],
    ['-', '-', '1', '-', '-'],
    ['-', '-', '-', '#', '-'],
    ['-', '-', '-', '-', '-']
]

# Definir el radio del rango del router
R = 2

# Definir las coordenadas del router
r = 2
c = 2

# Llamar a la función calcular_zona_cubierta
celdas_cubiertas = calcular_zona_cubierta(grid, r, c, R, 5, 5)

# Imprimir las celdas cubiertas
for x, y in celdas_cubiertas:
    print(f"Celda cubierta: ({x}, {y})")
