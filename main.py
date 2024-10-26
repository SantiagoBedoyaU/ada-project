import numpy as np
from pyemd import emd
from numpy . typing import NDArray
import csv
import math
import texttable

def read_csv(filename: str):
    lines:list[list[str]] = []
    with open(filename, "r") as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            lines.append(line)
    return lines

def active_variables(subsystem: str):
    active_variable = {}
    for idx, variable in enumerate(subsystem):
        active_variable[int(math.pow(2, idx))] = variable == "1"
    return active_variable

def cut_matrix(matrix: np.ndarray, key: int, row: int, add: int, len: int, axis: int):
    delete_rows = []
    while row < len:
        delete_rows = delete_rows + [x for x in range(row, add)]
        row += key * 2
        add += key * 2
    matrix = np.delete(matrix, delete_rows, axis)
    return matrix

def cut_rows_or_cols(matrix: np.ndarray, initial_state: str, active_variable: {bool}, axis: int):
    for key, value in reversed(list(active_variable.items())):
        if not value:
            if axis == 0:
                lenMatrix = len(matrix)
            else:
                lenMatrix = len(matrix[0])
                
            if initial_state[int(math.log2(key))] == "1":
                row = 0
                add = key
                matrix = cut_matrix(matrix, key, row, add, lenMatrix, axis)
            else:
                row = key
                add = key * 2
                matrix = cut_matrix(matrix, key, row, add, lenMatrix, axis)
    return matrix

def background_conditions(
    matrix: np.ndarray, initial_state: str, candidate_system: str
):
    active_variable = active_variables(candidate_system)
    matrix = cut_rows_or_cols(matrix, initial_state, active_variable, 0)
    matrix = cut_rows_or_cols(matrix, initial_state, active_variable, 1)
    return matrix

def marginalize_rows_or_cols(matrix: np.ndarray, subsystem: str, axis: int):
    active_variable = active_variables(subsystem)

    for key, value in reversed(list(active_variable.items())):
        if not value:
            matrix = group_rows_or_cols(matrix, key, axis)
    return matrix

def group_rows_or_cols(matrix: np.ndarray, key: int, axis: int):
    matrix = np.array(matrix).astype(float)  # Convierte la matriz a tipo float
    to_delete = []
    pointer = 0
    if axis == 0:
        lenMatrix = len(matrix)
    else:
        lenMatrix = len(matrix[0])

    while (pointer < lenMatrix):
        for i in range(0, key):
            if axis == 0:
                subset = np.array([matrix[pointer], matrix[pointer+key]])
                matrix[pointer] = np.sum(subset, axis=0) # Sumas por filas
                matrix[pointer] = matrix[pointer] / 2
            else:
                subset = np.array([matrix[:,pointer], matrix[:,pointer+key]])
                matrix[:, pointer] = np.sum(subset, axis=0) # Sumas por columnas
            
            to_delete.append(pointer+key)
            pointer += 1
        pointer += key
    matrix = np.delete(matrix, to_delete, axis)
    return matrix

def tensor_product(matrix_1, matrix_2):
    # Número de filas
    m = matrix_1.shape[0]
    # Dimensiones de columnas de las matrices
    n1 = matrix_1.shape[1]
    n2 = matrix_2.shape[1]
    matrix = np.zeros((m, n1 * n2))
    
    for i in range(m):
        matrix[i] = np.kron(matrix_1[i], matrix_2[i])
        
    return matrix

def emd_pyphi (u: NDArray[np.float64], v: NDArray[np.float64]) -> float :
    """
    Calculate the Earth Mover's Distance (EMD) between two probability
    distributions u and v.
    The Hamming distance was used as the ground metric.
    """
    if not all(isinstance(arr, np.ndarray) for arr in [u,v]):
        raise TypeError("u and v must be numpy arrays.")
    n: int = len(u)
    costs : NDArray[np.float64] = np.empty((n,n))
    for i in range (n):
        costs [i, :i] = [hamming_distance(i,j) for j in range (i)]
        costs [:i, i] = costs [i, :i]
    np.fill_diagonal(costs, 0)
    cost_matrix : NDArray[np.float64] = np.array(costs, dtype =np.float64)
    return emd(u, v, cost_matrix)

def hamming_distance (a: int, b: int) -> int:
    return (a ^ b).bit_count()

def print_matrix(matrix):
    table = texttable.Texttable()
    for row in matrix:
        table.add_row(row)
    print(table.draw())

def main():
    [initial_state, candidate_system, future_subsystem, present_subsystem] = read_csv(
        "estructura.csv"
    )[0]
    matrix = np.array(read_csv("matrizGuia.csv"))
    matrix = background_conditions(matrix, initial_state, candidate_system)
    old_matrix = matrix.copy()
    old_matrix = np.array(old_matrix).astype(float)
    # matrix = marginalize_rows_or_cols(matrix, present_subsystem, 0)
    matrix_1 = marginalize_rows_or_cols(matrix, '100', 1)
    matrix_2 = marginalize_rows_or_cols(matrix, '010', 1)
    matrix_3 = marginalize_rows_or_cols(matrix, '001', 1)
    matrix = tensor_product(matrix_1, matrix_2)
    matrix = tensor_product(matrix, matrix_3)
    print_matrix(matrix)
    print(emd_pyphi(matrix[7], old_matrix[5]))

main()
