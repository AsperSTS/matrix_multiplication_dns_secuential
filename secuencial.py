import numpy as np
import time
import sys
import threading
import psutil
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd

# Variables globales para el monitoreo
exit_event = None
cpu_total_usage = []
memory_usage = []
interval = float(sys.argv[3])

# Función para obtener la clave de un diccionario basándose en un valor
def obtain_dictionary_key(dictionary, val):
    for key, vals in dictionary.items():
        if val in vals:
            return key
    return None  

# Función para crear un nombre de archivo único con la marca de tiempo
def create_unique_filename(filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{filename}_{timestamp}"
    return unique_filename

# Función para crear una carpeta única con la marca de tiempo
def create_unique_folder(base_folder):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{base_folder}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

# Función para monitorear el uso de CPU y memoria en un hilo
def monitor_cpu_usage(exit_event):
    global cpu_total_usage
    global interval
    global memory_usage
    while not exit_event.is_set():  
        cpu_total_usage.append(psutil.cpu_percent(interval=interval))
        memory_usage.append(psutil.virtual_memory().used)

# Función para multiplicar matrices de forma recursiva
def multiply_matrices(A, B):
    n = len(A)
    result = np.zeros((n, n))

    # Si la matriz es lo suficientemente pequeña, realiza una multiplicación normal
    if n <= 64:
        return np.dot(A, B)

    # Divide las matrices en 4 submatrices
    mid = n // 2
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]

    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]

    # Realiza las multiplicaciones recursivas
    C11 = multiply_matrices(A11, B11) + multiply_matrices(A12, B21)
    C12 = multiply_matrices(A11, B12) + multiply_matrices(A12, B22)
    C21 = multiply_matrices(A21, B11) + multiply_matrices(A22, B21)
    C22 = multiply_matrices(A21, B12) + multiply_matrices(A22, B22)

    # Combina las submatrices en la matriz resultante
    result[:mid, :mid] = C11
    result[:mid, mid:] = C12
    result[mid:, :mid] = C21
    result[mid:, mid:] = C22

    return result

# Función principal
def main():
    global exit_event
    global cpu_total_usage
    global interval
    global memory_usage

    # Inicialización de variables de monitoreo
    initial_mem = psutil.virtual_memory().used
    cpu_total_usage.append(psutil.cpu_percent())
    memory_usage.append(psutil.virtual_memory().used)

    # Configuración de carpetas y variables según los argumentos de línea de comandos
    matrix_result_output_folder = None
    minus = None
    csv_folder = None

    matrix_groups = {
    'group1': [64, 128, 256],
    'group2': [512, 1024, 2048],
    'group3': [4096, 8192]
    }
    saving_format = {
        'Float':'%.3f',
        'Int': '%d'
    }
    
    if sys.argv[1][2:-4].startswith('f'): 
        minus = 4
        group = obtain_dictionary_key(matrix_groups,int(sys.argv[1][minus:-4]))
        data_type_matrix = "Float"
        matrix_result_output_folder = f"matrixResults"
        csv_folder = f'floatMeasurementResults/{group}/secuential'

    else:
        minus = 3
        group = obtain_dictionary_key(matrix_groups,int(sys.argv[1][minus:-4]))
        data_type_matrix = "Int"
        matrix_result_output_folder = f"matrixResults"
        csv_folder = f'intMeasurementResults/{group}/secuential'
     
    # Informa sobre las matrices cargadas
    print(f"Cargando matrices de: {sys.argv[1][minus:-4]}x{sys.argv[1][minus:-4]}")
    
    # Especifica la ruta completa de los archivos .npy en la carpeta "MatrixFiles"
    matrix1_path = os.path.join("MatrixFiles", sys.argv[1])
    matrix2_path = os.path.join("MatrixFiles", sys.argv[2])

    # Cargar las matrices desde archivos .npy en la carpeta "MatrixFiles"
    matrix1 = np.load(matrix1_path)
    matrix2 = np.load(matrix2_path)

    # Crear un evento para parar el monitoreo de memoria y CPU
    exit_event = threading.Event()

    # Crear un hilo de monitoreo
    cpu_monitor_thread = threading.Thread(target=monitor_cpu_usage, args=(exit_event,))
    cpu_monitor_thread.start()

    # Informar que se está ejecutando el algoritmo secuencial
    print("Ejecutando algoritmo secuencial")
    
    # Registrar el tiempo inicial
    tiempo_inicial = time.time()
    
    # Ejemplo de multiplicación de dos matrices de forma secuencial
    result_matrix = multiply_matrices(matrix1, matrix2)

    # Registrar el tiempo final
    tiempo_final = time.time()
    
    # Terminar el monitoreo
    exit_event.set()
    cpu_monitor_thread.join()

    # Calcular el tiempo transcurrido
    total_time_elapsed = tiempo_final - tiempo_inicial
    print(f"Ejecucion finalizada: {total_time_elapsed}")

    # Calcular estadísticas de rendimiento
    avg_cpu =  np.mean(cpu_total_usage)
    mb_memory_usage = [(i/1024/1024) for i in list(memory_usage)]
    initial_mem = (initial_mem/1024/1024)
    avg_memory = np.mean(mb_memory_usage ,axis=0)
    avg_memory = avg_memory-initial_mem
    
    # Guardar la matriz resultante de la multiplicación
    os.makedirs(matrix_result_output_folder, exist_ok=True)  # Crear la carpeta si no existe
    output_file = os.path.join(matrix_result_output_folder, create_unique_filename(f'SEC_{sys.argv[1][minus:-4]}_matrix'))
    np.savetxt(output_file+".txt", result_matrix, fmt=saving_format[data_type_matrix], delimiter=' ')
    np.save(output_file, result_matrix)

    # Guardar estadísticas de rendimiento en un archivo CSV
    try:   
        csv_output_file = os.path.join(csv_folder, f'{sys.argv[1][minus:-4]}{data_type_matrix}Table.csv')
        performanceDataFrame = pd.read_csv(csv_output_file)
        # Agregar una fila
        performanceDataFrame.loc[len(performanceDataFrame)] = [sys.argv[1][minus:-4], avg_cpu, avg_memory, total_time_elapsed]
        performanceDataFrame.to_csv(csv_output_file,index=False)

    except FileNotFoundError:
        measurementCsvData = {
                        "MATRIZ": [sys.argv[1][minus:-4]],
                        "CPU": [avg_cpu],
                        "RAM": [avg_memory],
                        "TIEMPO": [total_time_elapsed] 
                        }
        performanceDataFrame = pd.DataFrame(measurementCsvData)
        os.makedirs(csv_folder, exist_ok=True)  # Crear la carpeta si no existe
        csv_output_file = os.path.join(csv_folder, f'{sys.argv[1][minus:-4]}{data_type_matrix}Table.csv')
        performanceDataFrame.to_csv(csv_output_file, index=False)

if __name__ == "__main__":
    main()
