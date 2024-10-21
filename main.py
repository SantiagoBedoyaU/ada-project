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

    for key, value in active_variable.items():
        if not value:
            if initial_state[int(math.log2(key))] == "0":
                pass
            else:
                pass



    # print(active_variable)


def main():
    [initial_state, candidate_system, future_subsystem, present_subsystem] = read_csv('estructura.csv')[0]

    matrix = read_csv("matrizGuia.csv") 
    background_conditions(matrix, initial_state, candidate_system)

main()
