import csv
import math

def read_csv(filename: str):
    lines = []
    with open(filename, 'r') as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            lines.append(line)
    return lines

def background_conditions(matrix: list[list[int]], initial_state: int, candidate_system: str):
    active_variable = {}
    for idx, variable in enumerate(candidate_system):
        active_variable[int(math.pow(2, idx))] = variable == "1"
        
    for key, value in reversed(list(active_variable.items())):
        if not value:
            if initial_state[int(math.log2(key))] == "0":
                row = 0
                add = key
                matrix = cut_matrix(matrix, row, add, key)
            else:
                row = key
                add = key*2
                matrix = cut_matrix(matrix, row, add, key) 

def cut_matrix(matrix: list[list[int]], row: int, add: int, key: int):
    new_matrix = []
    while row < len(matrix):
        new_matrix = new_matrix + matrix[row:add]
        row += (key*2)
        add += (key*2)
    return new_matrix

def marginalization_per_row(matrix: list[list[int]], subset: str):
    active_variable = {}
    for idx, variable in enumerate(subset):
        active_variable[int(math.pow(2, idx))] = variable == "1"
        
            
    

def main():
    [initial_state, candidate_system, future_subsystem, present_subsystem] = read_csv('estructura.csv')[0]

    matrix = read_csv("matrizGuia.csv") 
    background_conditions(matrix, initial_state, candidate_system)

main()
