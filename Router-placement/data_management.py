import numpy as np
import global_def as gd

def load(file):
    
    #%% 
    
    in_file = open(file, "r")
    contentLines = in_file.readlines()
    in_file.close()
    
    #%% Load first line, describing the problem
    line1 = contentLines[0].split()
    gd.num_rows = int(line1[0])
    gd.num_cols = int(line1[1])
    gd.radius_router = int(line1[2])
    
    # Load de second line, describing the problem
    line2 = contentLines[1].split()
    gd.price_backbone = int(line2[0])
    gd.price_router = int(line2[1])
    gd.budget = int(line2[2])
    
    # Load de third line, describing the problem
    line3 = contentLines[2].split()
    gd.br = int(line3[0])
    gd.bc = int(line3[1])
    
    print("num_rows",gd.num_rows)
    print("num_cols",gd.num_cols)
    print("radius_router",gd.radius_router)
    print("price_backbone",gd.price_backbone)
    print("price_router",gd.price_router)
    print("budget",gd.budget)
    print("br",gd.br)
    print("bc",gd.bc)
    
    #%%
    # Crear un diccionario de mapeo para caracteres
    char_mapping = {'#': 3, '.': 4, '-': 5}
    
    gd.grid = np.zeros((gd.num_rows, gd.num_cols), dtype=int)
    
    # Llenar la cuadrícula
    for n_line in range(gd.num_rows):
        line = contentLines[n_line + 3].strip()
        for pos, cell in enumerate(line):
            # Asignar el valor correspondiente según el mapeo
            gd.grid[n_line, pos] = char_mapping.get(cell, -1)
    print(gd.grid)
    print("Data read correctly")
    
def load_mo(file):
    load(file)
    
    in_file = open(file, "r")
    contentLines = in_file.readlines()
    in_file.close()
    
    gd.adapted = [int(i) for i in contentLines[-1].split()]
        
def save(file_path, result):
    with open(file_path, "w+") as file:
        for r in result[1:]:
            # Esta línea convierte el elemento actual r en una cadena, elimina el primer y último carácter (que serían los corchetes si r es una lista), y luego elimina todas las comas. El resultado se asigna a la variable r_str.
            r_str = str(r)[1:-1].replace(',','')
            # Esta línea escribe una cadena en el archivo. La cadena contiene el número de elementos en r (obtenido con len(r)), seguido de un espacio, seguido de la cadena r_str. Luego se añade un salto de línea (\n) al final.
            file.write("{} {}\n".format(len(r), r_str))
            
if __name__ == "__main__":
#    file = "./qualification_round_2018.in/a_example.in"
#    load(file)    
    file = "./Router-placement/qualification_round_2017.in/charleston_road.in"
    load(file);