import numpy as np
import global_def as gd

def load(file):
    
    #%% 
    
    in_file = open(file, "r")
    contentLines = in_file.readlines()
    in_file.close()
    
    #%% Load first line, describing the problem
    param = contentLines[0].split()
    gd.num_rows = int(param[0])
    gd.num_cols = int(param[1])
    gd.num_vehic = int(param[2])
    gd.num_rides = int(param[3])
    gd.bonus = int(param[4])
    gd.num_steps = int(param[5])
    
    print("num_rows",gd.num_rows)
    print("num_cols",gd.num_cols)
    print("num_vehic",gd.num_vehic)
    print("num_rides",gd.num_rides)
    print("bonus",gd.bonus)
    print("num_steps",gd.num_steps)
    
    #%%
    gd.rides = np.zeros((gd.num_rides, 7))
    
    for n_line in range(gd.num_rides):
        line = contentLines[n_line + 1]
        for pos, d in enumerate(line.split()):
            gd.rides[n_line, pos] = d
    
    print(gd.rides)
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
    file = "./Self-driving rides/qualification_round_2018.in/b_should_be_easy_sp.in"
    load_mo(file)