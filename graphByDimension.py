import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
def calcular_promedio_en_subcarpetas(ruta):
    # Diccionario para almacenar DataFrames de cada grupo
    tipo_dato = None
    if "float" in ruta:
        tipo_dato = "FLOTANTES"
    elif "int" in ruta:
        tipo_dato = "ENTEROS"

    mean_dataframes = []    

     # Recorre la estructura de carpetas de manera recursiva
    for root_directory, directorios, files in os.walk(ruta):
        for onefile in files:
            if onefile.endswith(".csv") and "promedios" in onefile:
                complete_address = os.path.join(root_directory, onefile)

                # Carga el CSV en un DataFrame y lo agrega a la lista correspondiente al grupo
                actual_dataframe = pd.read_csv(complete_address)
                mean_dataframes.append(actual_dataframe)

    for dataframe in mean_dataframes:
        # Agrupa el DataFrame por el valor de la columna 'MATRIZ'

        grupos = dataframe.groupby('MATRIZ')
        
        # Almacena cada grupo en una lista
        listas_de_dataframes = [grupo for _, grupo in grupos]

        # Ahora, listas_de_dataframes contiene DataFrames separados por el valor de 'MATRIZ'
        for grupo in listas_de_dataframes:
            # Crear la figura y los ejes
            fig, (cpu, ram, tiempo) = plt.subplots(3, figsize=(10, 8))

            # Graficar las columnas 'CPU', 'RAM' y 'TIEMPO' con colores personalizados
            colors = ['blue', 'green', 'orange']

            # Reduce the width of the bars
            bar_width = 0.5

            cpu.bar(grupo['ALGORITMO'], grupo['CPU'], color=colors[0], label='CPU', width=bar_width)
            ram.bar(grupo['ALGORITMO'], grupo['RAM'], color=colors[1], label='RAM', width=bar_width)
            tiempo.bar(grupo['ALGORITMO'], grupo['TIEMPO'], color=colors[2], label='TIEMPO', width=bar_width)

            # Añadir etiquetas y leyendas
            cpu.set_title("CPU", fontweight='bold')
            ram.set_title("RAM", fontweight='bold')
            tiempo.set_title("TIEMPO", fontweight='bold')

            for ax, ylabel, column, unit in zip([cpu, ram, tiempo], ['CPU', 'RAM', 'TIEMPO'], ['CPU', 'RAM', 'TIEMPO'], ['%', 'MB', 'segundos']):
                ax.set_ylabel(f'{ylabel} ({unit})')

                # Mostrar el valor en el medio de cada barra
                for idx, value in enumerate(grupo[column]):
                    ax.text(idx, value, str(value)+" "+unit, ha='center', va='bottom', color='black', fontweight='bold')

            # Mostrar un recuadro con información sobre la gráfica
            fig.text(0.03, 0.92, f'CPU: {sys.argv[1]}\n RAM: {sys.argv[2]}\n NCORES: {sys.argv[3]}\n SO: {sys.argv[4]}', bbox=dict(facecolor='white', edgecolor='black'))

            # Agregar un título general
            fig.suptitle(f"GRAFICA DE MATRICES CON {tipo_dato } DE {grupo['MATRIZ'].mode().iloc[0]}x{grupo['MATRIZ'].mode().iloc[0]}", fontsize=16)

            # Ajustar el diseño y mostrar la figura
            plt.tight_layout()
            os.makedirs("byDimensionGraphs", exist_ok=True)  # Crea la carpeta si no existe
            output_file = os.path.join("byDimensionGraphs", f"graficaMatrices{(tipo_dato.lower().title()) }{grupo['MATRIZ'].mode().iloc[0]}")
            plt.savefig(output_file)
            #plt.savefig(f"graficaMatrices{(tipo_dato.lower().title()) }{grupo['MATRIZ'].mode().iloc[0]}")

# Calcula el promedio para las subcarpetas específicas de manera recursiva
calcular_promedio_en_subcarpetas('intMeasurementResults')
calcular_promedio_en_subcarpetas('floatMeasurementResults')
