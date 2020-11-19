import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
import glob
import os
import gurobipy as gp
from gurobipy import GRB
import bruteforce
import lp
import random
import time

"""
    timetest.py

    Randomly generates graphs of size ARGV[1], ARGV[2] times
    and prints out the stats of the graphs that took the longest amount of time
"""

def prettyprint(happiness, stress):
    for key in happiness:
        for val in happiness[key]:
            print(key, val, happiness[key][val], stress[key][val])

def order(arr, size):
    '''
        Reorders optimal room array so it looks like the brute force output.
    '''
    ordered_array = [[] for i in range(size)]
    for key in arr:
        ordered_array[arr[key]].append(key)
    ordered_array.sort(key = lambda x: x[0])
    return ordered_array

def timeTest(n, num_repetitions=10):
    '''
        timeTest(n, num_repetitions)

        Runs NUM_REPETITIONS trials of our ILP solver on a randomly
        generated graph with N nodes. If N <= 10, the bruteforce
        method will also be called to verify optimality, though
        this can be changed by changing respective cases.
    '''
    happiness = {}
    stress = {}
    for i in range(n):
        happiness[i] = {}
        stress[i]    = {}

    slowest_time = float("-inf")
    for i in range(num_repetitions):
        #generate graph
        s = round(random.uniform(65, 90), 3)
        for u in range(n):
            happiness[u] = {}
            stress[u] = {}
            for v in range(u + 1, n):
                happiness[u][v] = round(random.uniform(1, 5), 3)   #URV [1, 5] is best
                #force everyone in their own groups by setting stress[u][v] to 101
                stress[u][v]    = round(random.uniform(100, 101), 3) #URV [1, 5] is best

        #ILP Time
        answer = -1
        bf_arr = []
        groups = {}
        group_size = 0
        start_time = time.perf_counter()
        for k in range(1, n + 1):
            val, arr = lp.lp(happiness, stress, s, n, k)
            if val is not None and answer < val:
                answer = float(val)
                groups = arr
                group_size = k
        end_time = time.perf_counter()
        gurobi_time = end_time - start_time
        #Bruteforce Time
        if n <= 10:
            start_time = time.perf_counter()
            bf_arr, bf_val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
            end_time = time.perf_counter()
            bf_time = end_time - start_time
        
        if gurobi_time > slowest_time:
            print(n)
            print(s)
            print(prettyprint(happiness, stress))
            print("-------Stats-------")
            print("max_happiness:", answer)
            print("groupings gurobi:", order(groups, group_size))
            if n <= 10:
                assert round(bf_val, 3) == round(answer, 3), "Incorrect computation"
                print("groupings brutef:", bf_arr)
                print("brutef time:", bf_time)
            print("gurobi_time:", gurobi_time)
            print("\n\n")
            slowest_time = gurobi_time

if __name__ == "__main__":
    assert len(sys.argv) >= 2, \
        "Must have at least two arguments (run python3 timetest.py #nodes (#repetitions))"
    if len(sys.argv) == 3:
        timeTest(int(sys.argv[1]), int(sys.argv[2]))
    else:
        timeTest(int(sys.argv[1]))