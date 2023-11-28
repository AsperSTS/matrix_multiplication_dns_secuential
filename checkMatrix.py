import numpy as np
import sys
import os

def imprimir_parte_matriz(matriz, filas=10, columnas=10):
    for i in range(min(filas, matriz.shape[0])):
        for j in range(min(columnas, matriz.shape[1])):
            print(f"{matriz[i, j]:.4f}", end="\t")
        print("...")
    if filas < matriz.shape[0] or columnas < matriz.shape[1]:
        print("...")
def comparar_decimal(matriz1, matriz2):
# Verifica si las dimensiones de ambas matrices son iguales
    if matriz1.shape != matriz2.shape:
        print("Las matrices tienen dimensiones diferentes.")
    else:
        # Recorre las matrices y compara elemento por elemento
        filas, columnas = matriz1.shape
        for i in range(filas):
            for j in range(columnas):
                valor_matriz1 = matriz1[i, j]
                valor_matriz2 = matriz2[i, j]
                print(f"Matriz 1: {valor_matriz1}\nMatriz 2: {valor_matriz2}")
                # Compara los valores
                if valor_matriz1 != valor_matriz2:
                    print(f"Diferencia en la posición ({i}, {j}):")
                    print(f"Matriz 1: {valor_matriz1}")
                    print(f"Matriz 2: {valor_matriz2}")
def comparar_mayor_uno(matriz1, matriz2):
    # Verifica si las dimensiones de ambas matrices son iguales
    if matriz1.shape != matriz2.shape:
        print("Las matrices tienen dimensiones diferentes.")
    else:
        # Define el umbral de diferencia (mayor a 1 en este caso)
        umbral_diferencia = 1

        # Recorre las matrices y compara elemento por elemento
        filas, columnas = matriz1.shape
        for i in range(filas):
            for j in range(columnas):
                valor_matriz1 = matriz1[i, j]
                valor_matriz2 = matriz2[i, j]
                
                # Compara los valores considerando el umbral
                if abs(valor_matriz1 - valor_matriz2) > umbral_diferencia:
                    print(f"Diferencia mayor a {umbral_diferencia} en la posición ({i}, {j}):")
                    print(f"Matriz 1: {valor_matriz1}")
                    print(f"Matriz 2: {valor_matriz2}")
def comparar_npy():
    # Cargar los datos de los archivos .npy

    # Especifica la ruta completa de los archivos .npy en la carpeta "testMatrix"
    matrix1_path = os.path.join("matrixResults", sys.argv[1])
    matrix2_path = os.path.join("matrixResults", sys.argv[2])
    # Cargar las matrices desde archivos .npy en la carpeta "testMatrix"
    matriz1 = np.load(matrix1_path)
    matriz2 = np.load(matrix2_path)
    comparar_decimal(matriz1, matriz2)
    
comparar_npy()
