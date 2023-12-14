# Importamos el módulo random para generar números aleatorios
import random

# Definimos una función que recibe el nombre del fichero de texto
def modificar_fichero(nombre_original, nombre_resultado):

  # Abrimos el fichero en modo lectura
  with open(nombre_original, "r") as f:

    # Leemos todas las líneas del fichero y las guardamos en una lista
    lineas = f.readlines()

  # Cerramos el fichero
  f.close()

  # Obtenemos el tercer número de la primera línea, que indica cuántas líneas nuevas hay que añadir
  num_coches = int(lineas[0].split()[2])

  # Creamos una lista vacía para guardar las líneas modificadas
  lineas_modificadas = []

  # Añadimos la primera línea sin modificar
  lineas_modificadas.append(lineas[0])

  # Recorremos el resto de líneas
  for linea in lineas[1:]:

    # Generamos un 0 o un 1 al azar, con más probabilidad de que sea un 0
    # Para ello, usamos la función random.choices, que recibe una lista de elementos y una lista de pesos
    # En este caso, el 0 tiene un peso de 0.7 y el 1 tiene un peso de 0.3
    bit = random.choices([0, 1], weights=[0.7, 0.3])[0]

    # Añadimos el bit al final de la línea, con un espacio de separación
    linea_modificada = linea.strip() + " " + str(bit) + "\n"

    # Añadimos la línea modificada a la lista
    lineas_modificadas.append(linea_modificada)

  # Generamos una línea de 0s y 1s con más 0s que 1s, usando la misma función que antes
  # La longitud de la línea es la misma que la de las líneas anteriores, que se puede obtener restando uno al número de elementos de la primera línea
  linea_nueva = ""
  for i in range(num_coches):
    bit = random.choices([0, 1], weights=[0.7, 0.3])[0]
    linea_nueva += str(bit) + " "
  linea_nueva = linea_nueva.strip() + "\n"

  # Añadimos la línea nueva al final del fichero 
  lineas_modificadas.append(linea_nueva)

  # Abrimos el fichero en modo escritura
  with open(nombre_resultado, "w") as f:

    # Escribimos las líneas modificadas en el fichero
    f.writelines(lineas_modificadas)

  # Cerramos el fichero
  f.close()

  # Devolvemos un mensaje de éxito
  return "El fichero ha sido modificado con éxito."


# if __name__ == "__main__":
    
    # original_file = "./Self-driving rides/qualification_round_2018.in/e_high_bonus.in"
    # destination_file = "./Self-driving-rides-mo/qualification_round_2018.in/e_high_bonus.in"
    # modificar_fichero(original_file, destination_file)
    