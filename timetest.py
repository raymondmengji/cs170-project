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
import numpy as np

"""
    timetest.py

    Randomly generates graphs of size ARGV[1], ARGV[2] times
    and prints out the stats of the graphs that took the longest amount of time
"""

def prettyprint(happiness, stress):
    for key in happiness:
        for val in happiness[key]:
            print(key, val, happiness[key][val], stress[key][val])

def order(arr):
    '''
        Reorders optimal room array so it looks like the brute force output.
    '''
    num_rooms = -1
    for i in arr:
        num_rooms = max(num_rooms, arr[i])
    ordered_array = [[] for i in range(num_rooms + 1)]
    for key in arr:
        ordered_array[arr[key]].append(key)
    ordered_array.sort(key = lambda x: (x[0] if len(x) > 0 else None))
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

    average_diff = []
    error = []
    slowest_time = float("-inf")
    for i in range(num_repetitions):
        #generate graph
        s = round(random.uniform(65, 90), 3)
        for u in range(n):
            happiness[u] = {}
            stress[u] = {}
            for v in range(u + 1, n):
                happiness[u][v] = round(random.uniform(2, 5), 3)   #URV [1, 5] is best
                #force everyone in their own groups by setting stress[u][v] to 101
                stress[u][v]    = round(random.uniform(5, 10), 3) #URV [1, 5] is best

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

        answer2 = -1
        groups2 = {}
        group_size2 = 0
        start_time = time.perf_counter()
        for k in range(1, n + 1):
            val, arr = lp.lp(happiness, stress, s, n, k, True, False)
            if val is not None and answer2 < val:
                answer2 = float(val)
                groups2 = arr
                group_size2 = k
        end_time = time.perf_counter()
        gurobi_time2 = end_time - start_time

        #Bruteforce Time
        if n <= 10:
            start_time = time.perf_counter()
            bf_arr, bf_val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
            end_time = time.perf_counter()
            bf_time = end_time - start_time
        
        if True or gurobi_time > slowest_time:
            print(n)
            print(s)
            print(prettyprint(happiness, stress))
            print("-------Stats-------")
            print("optimize happiness:", answer)
            print("normal   happiness:", answer2)
            print(groups, groups2)
            print("optimize groups:", order(groups))
            print("normal   groups:", order(groups2))
            if n <= 10:
                #assert round(bf_val, 3) == round(answer, 3), "Incorrect computation"
                print("brutef   groupings:", bf_arr)
                print("brutef   time:", bf_time)
            print("optimize time:", gurobi_time)
            print("normal   time:", gurobi_time2)
            #Error between optimal and actual 
            error.append(round((answer - answer2) / ((answer + answer2) / 2) * 100, 3))
            #Percentage difference between optimized and normal speeds
            speedup = round(((gurobi_time2 - gurobi_time) / ((gurobi_time + gurobi_time2)/2)) * 100, 2)
            average_diff.append(speedup)
            print("Difference:", speedup, "%")
            print("\n\n")
            slowest_time = gurobi_time
    print(error)
    print(average_diff)
    print("Average Error:    ", np.average(error))
    print("Variance of Error:", np.var(error))
    print("Average Difference:          ", np.average(average_diff))
    print("Variance of Speed Difference:", np.var(average_diff))

if __name__ == "__main__":
    assert len(sys.argv) >= 2, \
        "Must have at least two arguments (run python3 timetest.py #nodes (#repetitions))"
    if len(sys.argv) == 3:
        timeTest(int(sys.argv[1]), int(sys.argv[2]))
    else:
        timeTest(int(sys.argv[1]))