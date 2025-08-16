import pandas as pd

# Cambia 'tu_archivo.csv' con la ruta correcta a tu archivo CSV
archivo_csv = '64Table.csv'

# Carga el CSV en un DataFrame de pandas
dataframe = pd.read_csv(archivo_csv)

# Calcula el promedio de las columnas 2, 3 y 4
promedio_columna_2 = dataframe['CPU'].mean()
promedio_columna_3 = dataframe['RAM'].mean()
promedio_columna_4 = dataframe['TIME'].mean()

# Imprime los resultados
print(f'Promedio de CPU: {promedio_columna_2}')
print(f'Promedio de RAM: {promedio_columna_3}')
print(f'Promedio de TIME: {promedio_columna_4}')
