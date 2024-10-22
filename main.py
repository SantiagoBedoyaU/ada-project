import numpy as np
import pandas as pd
import csv
import math


def read_csv(filename: str):
    lines = []
    with open(filename, "r") as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            lines.append(line)
    return lines


def background_conditions(
    matrix: np.ndarray, initial_state: int, candidate_system: str
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


def marginalize_cols(matrix: np.ndarray, initial_state: int, candidate_system: int):
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


def print_matrix(matrix: list[list[int]]):
    for row in matrix:
        print(row)


def main():
    [initial_state, candidate_system, future_subsystem, present_subsystem] = read_csv(
        "estructura.csv"
    )[0]
    matrix = np.array(read_csv("matrizGuia.csv"))
    matrix = background_conditions(matrix, initial_state, candidate_system)
    matrix = marginalize_cols(matrix, initial_state, candidate_system)
    group_rows(matrix)
    pass


main()
