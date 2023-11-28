import os
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from pandas.plotting import table
import plotly.figure_factory as ff
import sys

# Inicializar DataFrames finales
cpu_final_dataframe = None
ram_final_dataframe = None
tiempo_final_dataframe = None

def obtenerDataFrames(dataframes):
    global cpu_final_dataframe
    global ram_final_dataframe
    global tiempo_final_dataframe
    
    # Crear DataFrames separados para cada columna
    cpu_dataframe = None
    tiempo_dataframe = None
    ram_dataframe = None
    
    # Obtener las primeras 10 filas para cada DataFrame
    for dataframe in dataframes:
        primer_elemento = dataframe['MATRIZ'].iloc[0]
        primeros_10 = dataframe.head(10)

        # Concatenar las columnas de CPU
        cpu_dataframe = pd.concat([cpu_dataframe, primeros_10[['CPU']].rename(columns={'CPU': primer_elemento})], axis=1)
        cpu_dataframe.sort_index(axis=1, inplace=True)
        
        # Concatenar las columnas de Tiempo
        tiempo_dataframe = pd.concat([tiempo_dataframe, primeros_10[['TIEMPO']].rename(columns={'TIEMPO': primer_elemento})], axis=1)
        tiempo_dataframe.sort_index(axis=1, inplace=True)
        
        # Concatenar las columnas de RAM
        ram_dataframe = pd.concat([ram_dataframe, primeros_10[['RAM']].rename(columns={'RAM': primer_elemento})], axis=1)
        ram_dataframe.sort_index(axis=1, inplace=True)
    
    # Concatenar los DataFrames finales
    aux = cpu_final_dataframe
    cpu_final_dataframe = pd.concat([aux, cpu_dataframe], axis=1)
    
    aux = ram_final_dataframe
    ram_final_dataframe = pd.concat([aux, ram_dataframe], axis=1)

    aux = tiempo_final_dataframe
    tiempo_final_dataframe = pd.concat([aux, tiempo_dataframe], axis=1)
    return 

def obtener_primeros_10_en_subcarpetas(ruta, grupo, path):
    # Listas para almacenar DataFrames de cada grupo
    secDataframes = []  
    dnsDataframes = []

    # Recorrer la estructura de carpetas de manera recursiva
    for root_directory, directorios, files in os.walk(ruta):
        for onefile in files:
            # Verificar si el archivo es un CSV y no contiene "promedios" en el nombre
            if onefile.endswith(".csv") and not "promedios" in onefile and grupo in root_directory:
                complete_address = os.path.join(root_directory, onefile)
                
                # Cargar el CSV en un DataFrame y agregarlo a la lista correspondiente al grupo
                actual_dataframe = pd.read_csv(complete_address)

                # Determinar la clave del grupo basándose en la ruta completa
                dataframe_key = ''
                if "group1" in root_directory:
                    dataframe_key = "Grupo1"
                elif "group2" in root_directory:
                    dataframe_key = "Grupo2"
                elif "group3" in root_directory:
                    dataframe_key = "Grupo3"

                if "int" in root_directory:
                    dataframe_key = dataframe_key + "Int"
                elif "float" in root_directory:
                    dataframe_key = dataframe_key + "Float"

                if "secuential" in root_directory:
                    dataframe_key = dataframe_key + "Secuencial"
                    secDataframes.append(actual_dataframe)
                elif "dns" in root_directory:
                    dataframe_key = dataframe_key + "Dns"
                    dnsDataframes.append(actual_dataframe)

    # Obtener DataFrames para cada grupo
    obtenerDataFrames(secDataframes)
    obtenerDataFrames(dnsDataframes)

    # Redondear los valores en los DataFrames finales
    ram_final_dataframes_rounded = ram_final_dataframe.round(3) 
    dir = "tablasReporte/" + path
    
    # Crear tabla y guardarla como imagen PNG para la RAM
    fig = ff.create_table(ram_final_dataframes_rounded)
    fig.update_layout(
        autosize=False,
        width=500,
        height=200,
    )
    os.makedirs(dir, exist_ok=True)
    resultado_png = os.path.join(dir, "ram.png")
    fig.write_image(resultado_png, scale=2)
   
    # Redondear los valores en los DataFrames finales
    tiempo_final_dataframes_rounded = tiempo_final_dataframe.round(7)
    fig = ff.create_table(tiempo_final_dataframes_rounded)
    fig.update_layout(
        autosize=False,
        width=500,
        height=200,
    )

    # Crear tabla y guardarla como imagen PNG para el Tiempo
    resultado_png = os.path.join(dir, "tiempo.png")
    fig.write_image(resultado_png, scale=2)

    # Redondear los valores en los DataFrames finales
    cpu_final_dataframes_rounded = cpu_final_dataframe.round(5) 
    fig = ff.create_table(cpu_final_dataframes_rounded)
    fig.update_layout(
        title_text="Tabla de Ejemplo",
        title_x=0.5,  # Posición horizontal del título
        autosize=False,
        width=500,
        height=200,
    )

    # Crear tabla y guardarla como imagen PNG para la CPU
    resultado_png = os.path.join(dir, "cpu.png")
    fig.write_image(resultado_png, scale=2)

# Obtener las primeras 10 filas para las subcarpetas específicas de manera recursiva
obtener_primeros_10_en_subcarpetas(sys.argv[1], sys.argv[2], sys.argv[3])
