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

def comparar_npy():
    # Cargar los datos de los archivos .npy

    # Especifica la ruta completa de los archivos .npy en la carpeta "testMatrix"
    matrix1_path = os.path.join("matrixResults", sys.argv[1])
    matrix2_path = os.path.join("matrixResults", sys.argv[2])
    # Cargar las matrices desde archivos .npy en la carpeta "testMatrix"
    datos1 = np.load(matrix1_path)
    datos2 = np.load(matrix2_path)

    # Redondear los datos a la parte entera
    datos1_redondeados = np.round(datos1)
    datos2_redondeados = np.round(datos2)

    # Comparar si los datos redondeados son iguales
    son_iguales = np.array_equal(datos1_redondeados, datos2_redondeados)

    if son_iguales:
        print("Los archivos .npy son iguales (ignorando decimales).")
    else:
        print("Los archivos .npy son diferentes (ignorando decimales).")
    print(f"{sys.argv[1]}\n")
    imprimir_parte_matriz(datos1)
    
    print(f"\n{sys.argv[2]}\n")

    imprimir_parte_matriz(datos1)
comparar_npy()
