import numpy as np
import time
import sys
from mpi4py import MPI
import threading
import psutil
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd

exit_event = None
cpu_total_usage = []
memory_usage = []
interval = float(sys.argv[3])

def obtain_dictionary_key(dictionary, val):
    for key, vals in dictionary.items():
        if val in vals:
            return key
    return None  

def create_unique_filename(filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{filename}_{timestamp}"
    return unique_filename

def create_unique_folder(base_folder):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{base_folder}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def monitor_cpu_usage(exit_event):
    global cpu_total_usage
    global interval
    global memory_usage
    while not exit_event.is_set():  
        cpu_total_usage.append(psutil.cpu_percent(interval=interval))
        memory_usage.append(psutil.virtual_memory().used)


def multiply_matrices(matrix_list):
    result = matrix_list[0]
    for matrix in matrix_list[1:]:
        result = np.dot(result, matrix)
    return result


def main():

    global exit_event
    global cpu_total_usage
    global interval
    global memory_usage

    initial_mem = psutil.virtual_memory().used
    cpu_total_usage.append(psutil.cpu_percent())
    memory_usage.append(psutil.virtual_memory().used)

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
        #matrix_result_output_folder = f"matrixResults/float/secuential{sys.argv[1][minus:-4]}"
        matrix_result_output_folder = f"matrixResults"
        csv_folder = f'floatMeasurementResults/{group}/secuential'

    else:
        minus = 3
        group = obtain_dictionary_key(matrix_groups,int(sys.argv[1][minus:-4]))
        data_type_matrix = "Int"
        #matrix_result_output_folder = f"matrixResults/int/secuential{sys.argv[1][minus:-4]}"
        matrix_result_output_folder = f"matrixResults"
        csv_folder = f'intMeasurementResults/{group}/secuential'
     

    print(f"Cargando matrices de: {sys.argv[1][minus:-4]}x{sys.argv[1][minus:-4]}")
    # Especifica la ruta completa de los archivos .npy en la carpeta "testMatrix"
    matrix1_path = os.path.join("MatrixFiles", sys.argv[1])
    matrix2_path = os.path.join("MatrixFiles", sys.argv[2])

    # Cargar las matrices desde archivos .npy en la carpeta "testMatrix"
    matrix1 = np.load(matrix1_path)
    matrix2 = np.load(matrix2_path)

    # Creamos un evento para parar el monitoreo de memoria y cpu
    exit_event = threading.Event()

    # Creamos un hilo de monitoreo
    cpu_monitor_thread = threading.Thread(target=monitor_cpu_usage, args=(exit_event,))
    cpu_monitor_thread.start()

    print("Ejecutando algoritmo secuencial")
    # Registra el tiempo inicial
    tiempo_inicial = time.time()
    
    
    # Ejemplo de multiplicación de dos matrices de forma secuencial
    result_matrix = multiply_matrices([matrix1, matrix2])

    # Registra el tiempo final
    tiempo_final = time.time()
    # Terminamos el monitoreo
    exit_event.set()
    cpu_monitor_thread.join()

    # Calcula el tiempo transcurrido
    total_time_elapsed = tiempo_final - tiempo_inicial
    print(f"Ejecucion finalizada: {total_time_elapsed}")

    avg_cpu =  np.mean(cpu_total_usage)
    # Calculamos en MB la memoria que se ha utilizado
    mb_memory_usage = [(i/1024/1024) for i in list(memory_usage)]
    initial_mem = (initial_mem/1024/1024)

    avg_memory = np.mean(mb_memory_usage ,axis=0)
    avg_memory = avg_memory-initial_mem
    
    # Guardamos la matriz resultante de la multiplicacion
    os.makedirs(matrix_result_output_folder, exist_ok=True)  # Crea la carpeta si no existe
    #output_file = os.path.join(matrix_result_output_folder, create_unique_filename(f'SEC_{sys.argv[1][minus:-4]}_matrix'))
    output_file = os.path.join(matrix_result_output_folder, f'SEC_{sys.argv[1][minus:-4]}_matrix')
    #np.savetxt(output_file+".txt", result_matrix, fmt=saving_format[data_type_matrix], delimiter=' ')
    np.save(output_file,result_matrix)

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
        os.makedirs(csv_folder, exist_ok=True)  # Crea la carpeta si no existe
        csv_output_file = os.path.join(csv_folder, f'{sys.argv[1][minus:-4]}{data_type_matrix}Table.csv')
        performanceDataFrame.to_csv(csv_output_file, index=False)
    

if __name__ == "__main__":
    main()
