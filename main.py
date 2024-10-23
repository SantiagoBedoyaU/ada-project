import numpy as np
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


def background_conditions(
    matrix: np.ndarray, initial_state: str, candidate_system: str
):
    active_variable = {}
    for idx, variable in enumerate(candidate_system):
        active_variable[int(math.pow(2, idx))] = variable == "1"

    for key, value in reversed(list(active_variable.items())):
        if not value:
            if initial_state[int(math.log2(key))] == "1":
                row = 0
                add = key
                delete_rows = []
                while row < len(matrix):
                    delete_rows = delete_rows + [x for x in range(row, add)]
                    row += key * 2
                    add += key * 2
                matrix = np.delete(matrix, delete_rows, 0)
            else:
                row = key
                add = key * 2
                delete_rows = []
                while row < len(matrix):
                    delete_rows = delete_rows + [x for x in range(row, add)]
                    row += key * 2
                    add += key * 2
                matrix = np.delete(matrix, delete_rows, 0)
    return matrix


def marginalize_cols(matrix: np.ndarray, initial_state: str, candidate_system: str):
    active_variable = {}
    for idx, variable in enumerate(candidate_system):
        active_variable[int(math.pow(2, idx))] = variable == "1"

    for key, value in reversed(list(active_variable.items())):
        if not value:
            if initial_state[int(math.log2(key))] == "1":
                row = 0
                add = key
                delete_rows = []
                while row < len(matrix[0]):
                    delete_rows = delete_rows + [x for x in range(row, add)]
                    row += key * 2
                    add += key * 2
                matrix = np.delete(matrix, delete_rows, 1)
            else:
                row = key
                add = key * 2
                delete_rows = []
                while row < len(matrix[0]):
                    delete_rows = delete_rows + [x for x in range(row, add)]
                    row += key * 2
                    add += key * 2
                matrix = np.delete(matrix, delete_rows, 1)
    return matrix

def marginalize_rows(matrix: np.ndarray, initial_state: str, candidate_system: str):
    active_variable = {}
    for idx, variable in enumerate(candidate_system):
        active_variable[int(math.pow(2, idx))] = variable == "1"

    for key, value in reversed(list(active_variable.items())):
        if not value:
            cont = int(math.log2(key) + 1)
            matrix = group_rows(matrix, key, cont)

    return matrix

def group_rows(matrix: np.ndarray, key: int, cont: int):
    matrix = np.array(matrix).astype(float)  # Convierte la matriz a tipo float
    rows_to_delete = []
    for i in range(0, key):
        array1 = matrix[i]
        array2 = matrix[i+key]
        subset = np.array([array1, array2])
        matrix[i] = np.sum(subset, axis=0)   # Sumas por columnas
        matrix[i] = matrix[i] / cont
        rows_to_delete.append(i+key)
    matrix = np.delete(matrix, rows_to_delete, 0)
    return matrix

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
    matrix = marginalize_cols(matrix, initial_state, candidate_system)
    matrix = marginalize_rows(matrix, initial_state, present_subsystem)
    print_matrix(matrix)

main()
