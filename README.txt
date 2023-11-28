
DESCRIPCION DE LOS ARCHIVOS Y CARPETAS DENTRO DE LA CARPETA DE CODIGO

/MatrixFiles - Es la carpeta contenedora de los archivos npy de las matrices con las que se hicieron las pruebas, son pesadas entonces se puede omitir su descarga, se pueden generar mediante las tareas genMatrix y genMatrixFloat del makefile, para generar ambos tipos de matrices esta la tarea genAllMatrix

checkMatrix.py - Es un script de python que su unica funcion es comparar dos matrices resultantes, ejemplo la matriz resultante del algoritmo secuencial y la del dns, itera sobre  cada elemento de de ambas matrices en busqueda de elementos que sean muy diferentes de los de la otra matriz.

dnsMpy.py - Es el script del algoritmo DNS

genMatrix.py - Script encargado de generar las matrices enteras

genMatrixFloat.py - Script encargado de generar las matrices flotantes

genTables.py - Script de python que genera las tablas basandose en los archivos csv con los promedios de todas las ejecuciones, los promedios se generan con el script resultsMean.py

graphByDimension.py - Script que genera las graficas individuales para cada tipo de dato y dimension de matriz, se grafica basandose en el promedio generado por resultsMean.py

graphByGroup.py - Script que genera las graficas por grupo, se grafica basandose en el promedio generado por resultsMean.py

Makefile - Archivo para automatizar la ejecucion de los algoritmos y tareas para el tratado de los resultados

resultsMean.py - Script para calcular el promedio de todas las ejecuciones, accede a cada archivo csv de los resultados contenidos en los subdirectorios de intMeasurementResults y floatMeasurementResults respectivamente

secuencial.py - Script del algoritmo secuencial con el que comparamos dns

store-pid.py - Script que nos sirve para almacenar el process id de las ejecuciones del algoritmo secuencial para liberar memoria entre ejecuciones secuenciales, y no afectar las mediciones

