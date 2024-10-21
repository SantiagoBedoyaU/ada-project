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

    """
        A -> []
        B -> []
        C -> []
        D -> []
    """
    print(active_variable)

    # for i in range(0, 17, 8):
        # print(i)
    
    new_matrix = matrix.copy()
    for key, value in active_variable.items():
        if not value:
            if initial_state[int(math.log2(key))] == "0":
                """
                    key = 1
                    for 0 to new_matrix.length do
                        new_matrix[key:key + key)] -> 1to2, 3to4, 5to6, 7to8
                        key += 2

                    key = 2
                    add = 2
                    for 0 to new_matrix.length do
                        new_matrix[key:key+add] -> 2to4, 4to6, 8to10
                        key += 2
                        
                """
                pass
    
    print(len(new_matrix))
    for row in new_matrix:
        print(row)




def main():
    [initial_state, candidate_system, future_subsystem, present_subsystem] = read_csv('estructura.csv')[0]

    matrix = read_csv("matrizGuia.csv") 
    background_conditions(matrix, initial_state, candidate_system)

main()
