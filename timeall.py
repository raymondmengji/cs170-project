import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, order, prettyprint
import sys
import glob
import os
import numpy as np
import bruteforce
import lp
import random
import time


"""    
    timeall.py

    Runs all input files and prints the time it takes to complete them.
    Useful to see which inputs are the slowest for a given size.
"""

times = []
def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    n = G.order()
    happiness = {}
    stress = {}
    for i in range(n):
        happiness[i] = {}
        stress[i]    = {}

    for i in range(n):
        for j in range(i + 1, n):
            happiness[i][j] = G.get_edge_data(i, j)['happiness']
            stress[i][j]    = G.get_edge_data(i, j)['stress']

    print("Input Size:", n)
    if n <= 10: #brute force approach
        start_time = time.perf_counter()
        bf_arr, bf_val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
        bf_val = round(bf_val, 3)
        end_time = time.perf_counter()
        print("Brute Force Approach Time:", end_time - start_time)

    #ILP 
    start_time = time.perf_counter()
    answer, rooms, best_k = lp.lp_solve(happiness, stress, s, n)
    end_time = time.perf_counter()
    times.append(end_time - start_time)
    print("Gurobi Approach Time:     ", end_time - start_time)
    print("Gurobi Answer:            ", answer)
    #print("Gurobi Rooms (raw):       ", rooms, best_k)
    print("Gurobi Rooms:", order(rooms)[0])
    if n <= 10:
        #assert bf_val == answer, "Incorrect computation"
        print("Brutef Rooms:", bf_arr)
        print("Brutef Answer:", bf_val)
    return rooms, order(rooms)[1]
    
# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('samples/inputs/*')
    for input_path in inputs:
        output_path = 'samples/outputs/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
        print("File Name:", os.path.basename(os.path.normpath(input_path)))
        G, s = read_input_file(input_path, 100)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        print("Total Happiness: {}".format(calculate_happiness(D, G)))
        print()
        write_output_file(D, output_path)
    print("Times:", times[:-1])
    print("Avg Times", np.mean(times[:-1]))