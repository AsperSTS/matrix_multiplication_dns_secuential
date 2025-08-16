# DNS and Sequential Algorithms Comparison

A performance comparison project between DNS (Divide and Conquer) and Sequential matrix multiplication algorithms, developed for Operating Systems class.

## Overview

This project implements and benchmarks two matrix multiplication algorithms:
- **DNS Algorithm**: Divide and conquer approach for matrix multiplication
- **Sequential Algorithm**: Traditional iterative matrix multiplication

The comparison is performed across multiple matrix dimensions (64×64 to 8192×8192) using both integer and floating-point matrices.

## Technologies Used

- **Python**: Core implementation and data processing
- **NumPy**: Matrix operations and file handling
- **Matplotlib**: Data visualization and graph generation
- **Make**: Build automation and task management

## Project Structure

### Core Algorithm Files
- `dnsMpy.py` - DNS (Divide and Conquer) algorithm implementation
- `secuencial.py` - Sequential algorithm implementation
- `store-pid.py` - Process ID management for memory cleanup between executions

### Matrix Generation
- `genMatrix.py` - Integer matrix generator
- `genMatrixFloat.py` - Floating-point matrix generator
- `MatrixFiles/` - Directory containing generated .npy matrix files

### Analysis and Visualization
- `checkMatrix.py` - Matrix result comparison and validation
- `resultsMean.py` - Calculate execution time averages from CSV results
- `genTables.py` - Generate performance comparison tables
- `graphByDimension.py` - Create individual graphs per data type and dimension
- `graphByGroup.py` - Generate grouped comparison graphs

### Build System
- `Makefile` - Automated execution and analysis tasks

## Matrix Dimensions Tested

The algorithms are benchmarked across the following matrix sizes:
- 64×64, 128×128, 256×256, 512×512
- 1024×1024, 2048×2048, 4096×4096, 8192×8192

## Usage

### Generate Matrices
```bash
# Generate integer matrices
make genMatrix

# Generate floating-point matrices
make genMatrixFloat

# Generate both types
make genAllMatrix
```

### Run Algorithms
```bash
# Execute performance tests for specific dimensions
make 64matrix    # For 64×64 matrices
make 128matrix  # For 128×128 matrices
# ... up to run-8192
```

### Generate Analysis
```bash

# Create visualization graphs
make genAllGraphs
```

## Results Structure

- `intMeasurementResults/` - Integer matrix execution results (CSV format)
- `floatMeasurementResults/` - Floating-point matrix execution results (CSV format)

## Key Features

- **Algorithm Validation**: Matrix result verification between DNS and sequential methods
- **Performance Metrics**: Execution time measurement
- **Memory Management**: Process isolation to prevent memory interference
- **Automated Testing**: Complete pipeline from matrix generation to result visualization
- **Comprehensive Analysis**: Tables and graphs for performance comparison

## Academic Context

This project demonstrates:
- Algorithm complexity analysis (O(n³) vs divide-and-conquer approaches)
- Performance measurement methodologies
- Statistical analysis of computational results
- System-level programming concepts for operating systems coursework

---

*Developed as coursework for Operating Systems class*