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

def timeCompare():
    n = 11
    happiness = {}
    stress = {}
    for i in range(n):
        happiness[i] = {}
        stress[i]    = {}

    average_time_bf = 0
    average_time_gurobi = 0
    num = 200
    for i in range(num):
        #generate graph
        s = random.uniform(40, 60)
        for u in range(n):
            happiness[u] = {}
            stress[u] = {}
            for v in range(u + 1, n):
                happiness[u][v] = random.uniform(25, 75) #Uniform RV in [25, 75]
                stress[u][v]    = random.uniform(0, 30)  

        #ILP Time
        start_time = time.perf_counter()
        answer = 0
        for k in range(1, n + 1):
            val = lp.lp(happiness, stress, s, n, k)
            if val:
                answer = max(answer, val)
        end_time = time.perf_counter()
        gurobi_time = end_time - start_time
        #Bruteforce Time
        start_time = time.perf_counter()
        bf_arr, bf_val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
        end_time = time.perf_counter()
        bf_time = end_time - start_time

        assert round(bf_val, 4) == round(answer, 4), "Incorrect computation"
        print("BF_VAL:", bf_val, "GUROBI_VAL:", answer)
        print("Times:", bf_time, gurobi_time)
        print("Speed Difference:", bf_time / gurobi_time)
        print("------------------------------------------\n")
        average_time_bf += bf_time
        average_time_gurobi += gurobi_time
    print("averages:", average_time_bf / num, average_time_gurobi / num)