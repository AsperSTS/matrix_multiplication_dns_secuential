import numpy as np
import sys
import os

# Obtén los argumentos de la línea de comandos
args1 = sys.argv[1]
args2 = int(sys.argv[2])  # Convierte el segundo argumento a entero

# Genera una matriz de args2 x args2 con números flotantes aleatorios en el rango de 1.0 a 100.0
matriz = np.random.uniform(1000.0, 2000.0, (args2, args2))

# Guarda la matriz en un archivo .npy y .txt
nombre_archivo = args1  # Concatena ".npy" al nombre del archivo
output_folder = "MatrixFiles"
os.makedirs(output_folder, exist_ok=True)  # Crea la carpeta si no existe

output_file_npy = os.path.join(output_folder, nombre_archivo)
output_file_txt = os.path.join(output_folder, f'{nombre_archivo[:-4]}.txt')

np.save(output_file_npy, matriz)
np.savetxt(output_file_txt, matriz, fmt='%.6f', delimiter=' ')

print("La matriz TXT de", args2, "se ha guardado en el archivo:", output_file_txt)
print("La matriz NPY de", args2, "se ha guardado en el archivo:", output_file_npy)
