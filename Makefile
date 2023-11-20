# Nombre del archivo para almacenar el PID
PID_FILE := .pidfile

# Tiempo de espera en segundos para asegurar que la memoria se libere
WAIT_TIME := 5

# Numero de cores para la ejecucion

CORES := 8

# Iteraciones para probar el grupo 1 

ITERS64 := 50

genMatrix:
	python3 genMatrix.py "m1_64.npy" 64
	python3 genMatrix.py "m2_64.npy" 64

	python3 genMatrix.py "m1_128.npy" 128
	python3 genMatrix.py "m2_128.npy" 128

	python3 genMatrix.py "m1_256.npy" 256
	python3 genMatrix.py "m2_256.npy" 256
	
	python3 genMatrix.py "m1_512.npy" 512
	python3 genMatrix.py "m2_512.npy" 512

	python3 genMatrix.py "m1_1024.npy" 1024
	python3 genMatrix.py "m2_1024.npy" 1024

	python3 genMatrix.py "m1_2048.npy" 2048
	python3 genMatrix.py "m2_2048.npy" 2048

	python3 genMatrix.py "m1_4096.npy" 4096
	python3 genMatrix.py "m2_4096.npy" 4096

	python3 genMatrix.py "m1_8192.npy" 8192
	python3 genMatrix.py "m2_8192.npy" 8192
	
	
genMatrixFloat:
	python3 genMatrixFloat.py "m1f_64.npy" 64
	python3 genMatrixFloat.py "m2f_64.npy" 64

	python3 genMatrixFloat.py "m1f_128.npy" 128
	python3 genMatrixFloat.py "m2f_128.npy" 128

	python3 genMatrixFloat.py "m1f_256.npy" 256
	python3 genMatrixFloat.py "m2f_256.npy" 256
	
	python3 genMatrixFloat.py "m1f_512.npy" 512
	python3 genMatrixFloat.py "m2f_512.npy" 512

	python3 genMatrixFloat.py "m1f_1024.npy" 1024
	python3 genMatrixFloat.py "m2f_1024.npy" 1024

	python3 genMatrixFloat.py "m1f_2048.npy" 2048
	python3 genMatrixFloat.py "m2f_2048.npy" 2048

	python3 genMatrixFloat.py "m1f_4096.npy" 4096
	python3 genMatrixFloat.py "m2f_4096.npy" 4096

	python3 genMatrixFloat.py "m1f_8192.npy" 8192
	python3 genMatrixFloat.py "m2f_8192.npy" 8192
testo:
	@echo "\nPRUEBAS CON MATRICES DE 512x512 \n"
	@make pre_test
	@python3 secuencial.py 'm1_512.npy' 'm2_512.npy' 0.01 
	@echo "\n"
	@make clean_memory 
	@sleep $(WAIT_TIME)
	@make pre_test
	@mpirun -n 8 python3 dnsMpi.py 'm1_512.npy' 'm2_512.npy' 0.01 

	@echo "\nPRUEBAS CON MATRICES DE 1024X1024 \n"
	@make clean_memory 
	@sleep $(WAIT_TIME)
	@make pre_test
	@python3 secuencial.py 'm1_1024.npy' 'm2_1024.npy' 0.1
	@echo "\n"
	@make clean_memory 
	@sleep $(WAIT_TIME)
	@make pre_test
	@mpirun -n 8 python3 dnsMpi.py 'm1_1024.npy' 'm2_1024.npy' 0.1

clean_memory:
	@echo "Liberando memoria del testeo anterior..."
	@-pkill -F $(PID_FILE)
	@rm -f $(PID_FILE)

# Tarea interna para ejecutar antes de cada prueba y almacenar el PID
pre_test:
	@echo "Almacenando el PID del proceso..."
	@python3 store_pid.py



64matrix:

	make pre_test
	python3 secuencial.py 'm1_64.npy' 'm2_64.npy' 0.0001
	make clean_memory
	sleep $(WAIT_TIME)

	make pre_test; 
	python3 secuencial.py 'm1f_64.npy' 'm2f_64.npy' 0.0001 
	make clean_memory 
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_64.npy' 'm2_64.npy' 0.0001
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_64.npy' 'm2f_64.npy' 0.0001
	sleep $(WAIT_TIME)


128matrix:

	make pre_test; 
	python3 secuencial.py 'm1f_128.npy' 'm2f_128.npy' 0.001
	make clean_memory 
	sleep $(WAIT_TIME)

	make pre_test; 
	python3 secuencial.py 'm1_128.npy' 'm2_128.npy' 0.001
	make clean_memory 
	sleep $(WAIT_TIME)
		
	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_128.npy' 'm2f_128.npy' 0.001
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_128.npy' 'm2_128.npy' 0.001
	sleep $(WAIT_TIME)
    
256matrix:

	make pre_test; 
	python3 secuencial.py 'm1f_256.npy' 'm2f_256.npy' 0.001
	make clean_memory 
	sleep $(WAIT_TIME)

	make pre_test; 
	python3 secuencial.py 'm1_256.npy' 'm2_256.npy' 0.001
	make clean_memory 
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_256.npy' 'm2f_256.npy' 0.001
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_256.npy' 'm2_256.npy' 0.001
	sleep $(WAIT_TIME)
    
512matrix:
	make pre_test; 
	python3 secuencial.py 'm1f_512.npy' 'm2f_512.npy' 0.01
	make clean_memory 
	sleep $(WAIT_TIME)

	make pre_test; 
	python3 secuencial.py 'm1_512.npy' 'm2_512.npy' 0.01
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_512.npy' 'm2f_512.npy' 0.01
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_512.npy' 'm2_512.npy' 0.01
	sleep $(WAIT_TIME)
1024matrix:
	make pre_test; 
	python3 secuencial.py 'm1f_1024.npy' 'm2f_1024.npy' 0.1
	make clean_memory 
	sleep $(WAIT_TIME)

	make pre_test; 
	python3 secuencial.py 'm1_1024.npy' 'm2_1024.npy' 0.1
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_1024.npy' 'm2f_1024.npy' 0.1
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_1024.npy' 'm2_1024.npy' 0.1
	sleep $(WAIT_TIME)
2048matrix:
	make pre_test; 
	python3 secuencial.py 'm1f_2048.npy' 'm2f_2048.npy' 0.5
	make clean_memory 
	sleep $(WAIT_TIME)

	make pre_test; 
	python3 secuencial.py 'm1_2048.npy' 'm2_2048.npy' 0.5
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_2048.npy' 'm2f_2048.npy' 0.5
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_2048.npy' 'm2_2048.npy' 0.5
	sleep $(WAIT_TIME)
4096matrix:
	make pre_test; 
	python3 secuencial.py 'm1f_4096.npy' 'm2f_4096.npy' 0.1
	make clean_memory 
	sleep $(WAIT_TIME)

	make pre_test; 
	python3 secuencial.py 'm1_4096.npy' 'm2_4096.npy' 10
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_4096.npy' 'm2f_4096.npy' 0.1
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_4096.npy' 'm2_4096.npy' 5
	sleep $(WAIT_TIME)


8192matrix1:
	make pre_test; 
	python3 secuencial.py 'm1_8192.npy' 'm2_8192.npy' 240
	sleep $(WAIT_TIME)

8192matrix2:
	make pre_test; 
	python3 secuencial.py 'm1f_8192.npy' 'm2f_8192.npy' 1
	make clean_memory 
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_8192.npy' 'm2f_8192.npy' 1
	sleep $(WAIT_TIME)

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_8192.npy' 'm2_8192.npy' 20
	sleep $(WAIT_TIME)

float64:
	for i in $$(seq 1 $(ITERS64)); do \
		python3 secuencial.py 'm1f_64.npy' 'm2f_64.npy' 0.0001 ; \
	done

floatt:
	for i in $$(seq 1 50); do \
		python3 secuencial.py 'm1_64.npy' 'm2_64.npy' 0.0001 ; \
	done
	for i in $$(seq 1 50); do \
		mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_128.npy' 'm2f_128.npy' 0.001; \
	done

sample:
	for i in $$(seq 1 $(ITERS64)); do \
		mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_64.npy' 'm2_64.npy' 0.0001;\
	done

	for i in $$(seq 1 $(ITERS64)); do \
		mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_64.npy' 'm2f_64.npy' 0.0001;\
	done

	for i in $$(seq 1 $(ITERS64)); do \
		mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_128.npy' 'm2_128.npy' 0.001;\
	done

	for i in $$(seq 1 $(ITERS64)); do \
		mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_128.npy' 'm2f_128.npy' 0.001;\
	done

	for i in $$(seq 1 $(ITERS64)); do \
		python3 secuencial.py 'm1_256.npy' 'm2_256.npy' 0.001;\
	done

	for i in $$(seq 1 $(ITERS64)); do \
		python3 secuencial.py 'm1f_256.npy' 'm2f_256.npy' 0.001;\
	done

testing1:

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_64.npy' 'm2_64.npy' 0.0001
	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_64.npy' 'm2f_64.npy' 0.0001
	python3 secTinyMatrix.py 'm1_64.npy' 'm2_64.npy' 0.0001
	python3 secTinyMatrix.py 'm1f_64.npy' 'm2f_64.npy' 0.0001

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_128.npy' 'm2_128.npy' 0.001
	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_128.npy' 'm2f_128.npy' 0.001
	python3 secTinyMatrix.py 'm1_128.npy' 'm2_128.npy' 0.001
	python3 secTinyMatrix.py 'm1f_128.npy' 'm2f_128.npy' 0.001

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_256.npy' 'm2_256.npy' 0.001
	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_256.npy' 'm2f_256.npy' 0.001
	python3 secuencial.py 'm1_256.npy' 'm2_256.npy' 0.001
	python3 secuencial.py 'm1f_256.npy' 'm2f_256.npy' 0.001


	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_512.npy' 'm2_512.npy' 0.01
	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_512.npy' 'm2f_512.npy' 0.01
	python3 secuencial.py 'm1_512.npy' 'm2_512.npy' 0.01
	python3 secuencial.py 'm1f_512.npy' 'm2f_512.npy' 0.01

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_1024.npy' 'm2_1024.npy' 0.1
	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_1024.npy' 'm2f_1024.npy' 0.1
	python3 secuencial.py 'm1_1024.npy' 'm2_1024.npy' 0.1
	python3 secuencial.py 'm1f_1024.npy' 'm2f_1024.npy' 0.1

	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1_2048.npy' 'm2_2048.npy' 1
	mpirun --host localhost:$(CORES) python3 dnsMpi.py 'm1f_2048.npy' 'm2f_2048.npy' 1
	python3 secuencial.py 'm1_2048.npy' 'm2_2048.npy' 1
	python3 secuencial.py 'm1f_2048.npy' 'm2f_2048.npy' 1


group1:
	for i in $$(seq 1 200); do \
		make 64matrix;\
		make 128matrix;\
		make 256matrix;\
	done
group2:
	for i in $$(seq 1 10); do \
		make 512matrix;\
		make 1024matrix;\
		make 2048matrix;\
	done
group31:
	make 8192matrix1
	make 8192matrix2
group3:
	for i in $$(seq 1 5); do \
		make 4096matrix;\
		make 8192matrix2;\
	done
finalTest:
	@make group1
	@make group2
	@make group3
