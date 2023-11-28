import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
def graphGroups(ruta):
    # Diccionario para almacenar DataFrames de cada group
    data_type = None
    origin_group = None
    if "float" in ruta:
        data_type = "FLOTANTES"
    elif "int" in ruta:
        data_type = "ENTEROS"

    mean_dataframes = {}

    # Recorre la estructura de carpetas de manera recursiva
    for root_directory, directorios, files in os.walk(ruta):
        for onefile in files:
            if onefile.endswith(".csv") and "promedios" in onefile:
                
                # Determina el group basándote en la ruta completa
                dataframe_key = None
                if "Grupo1" in onefile :
                    dataframe_key = "Grupo1"
                elif "Grupo2" in onefile:
                    dataframe_key = "Grupo2"
                elif "Grupo3" in onefile:
                    dataframe_key = "Grupo3"
                dataframe_key = dataframe_key+data_type


                complete_address = os.path.join(root_directory, onefile)

                # Carga el CSV en un DataFrame y lo agrega a la lista correspondiente al group
                actual_dataframe = pd.read_csv(complete_address)
                #mean_dataframes.append(actual_dataframe)
                mean_dataframes[dataframe_key] = actual_dataframe

    for key, dataframe in mean_dataframes.items():
        if "Grupo1" in key :
            origin_group = "GRUPO1"
        elif "Grupo2" in key:
            origin_group = "GRUPO2"
        elif "Grupo3" in key:
            origin_group = "GRUPO3"
        # Agrupa el DataFrame por el valor de la columna 'MATRIZ'
        # Crear subconjuntos de datos para cada columna (CPU, RAM, TIEMPO)
        actual_dataframe = dataframe

        matrix_sizes = actual_dataframe['MATRIZ'].unique()

        matrix_sizes_str = ", ".join([str(m) for m in matrix_sizes])


        #print(matrix_sizes)
        cpu_data = actual_dataframe.pivot(index='MATRIZ', columns='ALGORITMO', values='CPU')
        ram_data = actual_dataframe.pivot(index='MATRIZ', columns='ALGORITMO', values='RAM')
        tiempo_data = actual_dataframe.pivot(index='MATRIZ', columns='ALGORITMO', values='TIEMPO')

        # Crear subgráficas para CPU, RAM y TIEMPO
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

        plt.subplots_adjust(bottom=0.5, right=5, top=0.9)


        # Graficar CPU
        for i, col in enumerate(cpu_data.columns):
            for j, val in enumerate(cpu_data[col]):
                # Alternar la posición de las etiquetas de texto a la derecha e izquierda
                ha = 'right' if i % 2 == 0 else 'left'
                ax1.text(j + i * 0.2, val, f'{val:.2f} %', ha=ha, va='bottom')

        # Graficar CPU
        cpu_data.plot(kind='bar', ax=ax1, rot=0)
        ax1.set_title('CPU', fontweight='bold')
        ax1.set_ylabel('CPU: %')
        ax1.set_xlabel('')

        # Graficar RAM
        for i, col in enumerate(ram_data.columns):
            for j, val in enumerate(ram_data[col]):
                ha = 'right' if i % 2 == 0 else 'left'
                ax2.text(j + i * 0.2, val, f'{val:.2f} MB', ha=ha, va='bottom')
        # Graficar RAM
        ram_data.plot(kind='bar', ax=ax2, rot=0)
        ax2.set_title('RAM', fontweight='bold')
        ax2.set_ylabel('RAM: MB')
        ax2.set_xlabel('')
        # Graficar TIEMPO
        for i, col in enumerate(tiempo_data.columns):
            for j, val in enumerate(tiempo_data[col]):
                ha = 'right' if i % 2 == 0 else 'left'
                ax3.text(j + i * 0.2, val, f'{val:.4f} s', ha=ha, va='bottom')

        # Graficar TIEMPO
        tiempo_data.plot(kind='bar', ax=ax3, rot=0)
        ax3.set_title('TIEMPO', fontweight='bold')
        ax3.set_ylabel('Segundos')
        ax3.set_xlabel('')


        # Mover la leyenda a una posición específica
        ax1.legend(loc='best')
        ax2.legend(loc='best')
        ax3.legend(loc='best')

        # Mostrar un recuadro con información sobre la gráfica
        fig.text(0.02, 0.95, f'CPU: {sys.argv[1]}\n RAM: {sys.argv[2]}\n NCORES: {sys.argv[3]}\n SO: {sys.argv[4]}', bbox=dict(facecolor='white', edgecolor='black'))



        # Agregar un título general
        fig.suptitle(f"MATRICES DE {data_type } ({origin_group}) -> ({matrix_sizes_str})", fontsize=16)

        # Ajustar el diseño y mostrar la figura
        plt.tight_layout()
        os.makedirs("byGroupGraphs", exist_ok=True)  # Crea la carpeta si no existe
        output_file = os.path.join("byGroupGraphs", f"graficaMatrices{key}")
        plt.savefig(output_file)
       

# Calcula el promedio para las subcarpetas específicas de manera recursiva
graphGroups('intMeasurementResults')
graphGroups('floatMeasurementResults')
