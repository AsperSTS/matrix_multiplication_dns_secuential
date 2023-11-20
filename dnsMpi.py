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
def dns_matrix_multiply(A, B):
    n = len(A)
    result = np.zeros((n, n))

    # Caso base: Si la matriz es lo suficientemente pequeña, realiza una multiplicación normal
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

    # Realiza las multiplicaciones recursiva
    C11 = dns_matrix_multiply(A11, B11) + dns_matrix_multiply(A12, B21)
    C12 = dns_matrix_multiply(A11, B12) + dns_matrix_multiply(A12, B22)
    C21 = dns_matrix_multiply(A21, B11) + dns_matrix_multiply(A22, B21)
    C22 = dns_matrix_multiply(A21, B12) + dns_matrix_multiply(A22, B22)

    # Combina las submatrices en la matriz resultante
    result[:mid, :mid] = C11
    result[:mid, mid:] = C12
    result[mid:, :mid] = C21
    result[mid:, mid:] = C22

    return result

def create_unique_folder(base_folder):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{base_folder}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def create_unique_filename(filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{filename}_{timestamp}"
    return unique_filename

def monitor_cpu_usage(exit_event):
    global cpu_total_usage
    global interval
    global memory_usage
    while not exit_event.is_set():  
        cpu_total_usage.append(psutil.cpu_percent(interval=interval))
        memory_usage.append(psutil.virtual_memory().used)

def obtain_dictionary_key(dictionary, val):
    for key, vals in dictionary.items():
        if val in vals:
            return key
    return None  

def main():
    global exit_event
    global cpu_total_usage
    global interval
    global memory_usage
    initial_mem = psutil.virtual_memory().used
    cpu_total_usage.append(psutil.cpu_percent())

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
        #matrix_result_output_folder = f"matrixResults/float/dns{sys.argv[1][minus:-4]}"
        matrix_result_output_folder = f"matrixResults"
        csv_folder = f'floatMeasurementResults/{group}/dns'
    else:
        minus = 3
        group = obtain_dictionary_key(matrix_groups,int(sys.argv[1][minus:-4]))
        data_type_matrix = "Int"
        #matrix_result_output_folder = f"matrixResults/int/dns{sys.argv[1][minus:-4]}"
        matrix_result_output_folder = f"matrixResults"
        csv_folder = f'intMeasurementResults/{group}/dns'
    
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  
    
    if rank == 0:
        # Especifica la ruta completa de los archivos .npy en la carpeta "testMatrix"
        matrix1_path = os.path.join("MatrixFiles", sys.argv[1])
        matrix2_path = os.path.join("MatrixFiles", sys.argv[2])
        # Cargar las matrices desde archivos .npy en la carpeta "testMatrix"
        matrix1 = np.load(matrix1_path)
        matrix2 = np.load(matrix2_path)
    else:
        matrix1 = None
        matrix2 = None

    matrix1 = comm.bcast(matrix1, root=0)
    matrix2 = comm.bcast(matrix2, root=0)
    exit_event = threading.Event()

    cpu_monitor_thread = threading.Thread(target=monitor_cpu_usage, args=(exit_event,))
    cpu_monitor_thread.start()

    # Registra el tiempo inicial
    tiempo_inicial = time.time()

    # Llama a la función dns_matrix_multiply para realizar la multiplicación de matrices
    result_matrix = dns_matrix_multiply(matrix1, matrix2)

    # Registra el tiempo final
    tiempo_final = time.time()
    
    # Terminamos el monitoreo
    exit_event.set()
    cpu_monitor_thread.join()

    # Agregamos el valor actual de nuestro procesador y el uso de memoria
    #cpu_total_usage.append(psutil.cpu_percent())
    #memory_usage.append(psutil.virtual_memory().used)
    
    # Proceso 0 traza la gráfica con@mpirun -n 8 python3 dnsMpi.py 'm1_8192.npy' 'm2_8192.npy' 20 los datos recopilados
    if rank == 0:

        # Finaliza MPI  
        MPI.Finalize()

        # Calcula el tiempo transcurrido
        total_time_elapsed = tiempo_final - tiempo_inicial
        print(f"Ejecucion finalizada: {total_time_elapsed}")

        avg_cpu =  np.mean(cpu_total_usage)
        # Calculamos en MB la memoria que se ha utilizado
        mb_memory_usage = [(i/1024/1024) for i in list(memory_usage)]
        initial_mem = (initial_mem/1024/1024)

        avg_memory = np.mean(mb_memory_usage ,axis=0)
        avg_memory = avg_memory-initial_mem

        #Guardamos la matriz resultante de la multiplicacion
        os.makedirs(matrix_result_output_folder, exist_ok=True)  # Crea la carpeta si no existe
        #output_file = os.path.join(matrix_result_output_folder, create_unique_filename(f'DNS_{sys.argv[1][minus:-4]}_matrix'))
        output_file = os.path.join(matrix_result_output_folder, f'DNS_{sys.argv[1][minus:-4]}_matrix')
        np.save(output_file, result_matrix)
        #np.savetxt(output_file+".txt", result_matrix, fmt=saving_format[data_type_matrix], delimiter=' ')

        try:   
            csv_output_file = os.path.join(csv_folder, f'{sys.argv[1][minus:-4]}{data_type_matrix}Table.csv')
            performanceDataFrame = pd.read_csv(csv_output_file)
            print(f'CSV LEN: {len(performanceDataFrame)}')
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
