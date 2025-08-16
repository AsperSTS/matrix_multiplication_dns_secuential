import os
import pandas as pd

def calcular_promedio_en_subcarpetas(ruta):
    # Diccionario para almacenar DataFrames de cada grupo
    dataframes_por_grupo = {}

    # Recorre la estructura de carpetas de manera recursiva
    for directorio_raiz, directorios, archivos in os.walk(ruta):
        for archivo in archivos:
            if archivo.endswith(".csv") and "promedios" not in archivo:
                ruta_completa = os.path.join(directorio_raiz, archivo)

                # Determina el grupo basándote en la ruta completa
                grupo = None
                if "group1" in ruta_completa:
                    grupo = "Grupo1"
                elif "group2" in ruta_completa:
                    grupo = "Grupo2"
                elif "group3" in ruta_completa:
                    grupo = "Grupo3"
                algoritmo = None
                if "dns" in ruta_completa:
                    algoritmo = "Dns"
                if "secuential" in ruta_completa:
                    algoritmo = "Secuencial"
                # Si el grupo no existe en el diccionario, crea un nuevo DataFrame para ese grupo
                if grupo not in dataframes_por_grupo:
                    dataframes_por_grupo[grupo] = []

                # Carga el CSV en un DataFrame y lo agrega a la lista correspondiente al grupo
                dataframe_actual = pd.read_csv(ruta_completa)
                dataframe_actual['ALGORITMO'] = algoritmo
                dataframes_por_grupo[grupo].append(dataframe_actual)

    # Verifica si hay al menos un archivo CSV en las carpetas
    if dataframes_por_grupo:
        # Recorre el diccionario y guarda los resultados de cada grupo en un archivo CSV separado
        for grupo, dataframes_grupo in dataframes_por_grupo.items():
            dataframe_concatenado = pd.concat(dataframes_grupo, ignore_index=True)

            # Filtra los valores diferentes de 0 en todas las columnas, excepto 'ALGORITMO' y 'MATRIZ'
            promedio_por_archivo = dataframe_concatenado.groupby(['ALGORITMO', 'MATRIZ']).mean().reset_index()
            promedio_por_archivo.iloc[:, 2:] = promedio_por_archivo.iloc[:, 2:].replace(0, pd.NA)

            # Redondea los valores en todas las columnas, excepto 'ALGORITMO' y 'MATRIZ'
            promedio_por_archivo.iloc[:, 2:] = promedio_por_archivo.iloc[:, 2:].round(decimals=6)

            # Guarda el resultado en un nuevo archivo CSV específico para ese grupo
            resultado_csv = os.path.join(ruta, f'promedios_{grupo}.csv')
            promedio_por_archivo.to_csv(resultado_csv, index=False)

            print(f'Promedio de los archivos en {grupo}:')
            print(promedio_por_archivo)
            print(f'Resultado guardado en {resultado_csv}')
    else:
        print(f'No se encontraron archivos CSV en {ruta}')

# Calcula el promedio para las subcarpetas específicas de manera recursiva
calcular_promedio_en_subcarpetas('intMeasurementResults')
calcular_promedio_en_subcarpetas('floatMeasurementResults')
