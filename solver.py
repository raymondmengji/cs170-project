import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys

import bruteforce


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    # TODO: your code here!
    d = nx.to_dict_of_dicts(G)
    
    happiness = {}
    stress = {}
    for key1 in d.keys():
        happiness[key1] = {}
        stress[key1] = {}
        key_dict = d[key1]
        for key2 in key_dict.keys():
            happiness[key1][key2] = key_dict[key2]['happiness']
            stress[key1][key2] = key_dict[key2]['stress']

    arr = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
    
    assignments = {}
    for i in range(len(arr)):
        for person in arr[i]:
            assignments[person] = i

    print(assignments)
    return assignments, len(arr)




# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)