# CS 170 Project Fall 2020

## Instructions

Run `pip install -r requirements.txt` to install all dependencies used.

## Team - Undecided
Julian Meyn, John Le, Raymond Ji 

## Problem Statment
2020 has been a stressful year, and CS 170 course staff is trying to reduce student stress and increase student happiness
as much as possible. Since school has been reduced to a series of awkward Zoom breakout rooms, we figured this is
a good place to start. We noticed that student stress and happiness fluctuate greatly depending on how they are split
into breakout rooms, so we are looking to find a way to divide up stressed 170 students to make them a little happier.
However, this sounds like a really difficult task, so we decided to outsource this to you.

Project Spec: https://cs170.org/assets/pdf/project_spec.pdf

## Approach
We attempted to solve this NP-Hard problem using Mixed Integer Programming. 

## Files
solver.py  - Runs all files in samples/inputs and prints the highest valid Total Happiness of each graph

timeall.py - Same as solver.py, but also prints diagnostic data about speed and room distributions for each file

timetest.py n k - Randomly generates k graphs with n nodes and prints diagnostic data about its performance. 
Useful to test hard inputs

## LP Solver
We used the Gurobi optimizer, which is freely available for students. 

## Resources Used
https://arxiv.org/pdf/1802.07144.pdf

https://codereview.stackexchange.com/questions/1526/

https://www.gurobi.com/

https://www.gurobi.com/documentation/9.1/refman/py_python_api_overview.html

https://cs.stackexchange.com/questions/12102/express-boolean-logic-operations-in-zero-one-integer-linear-programming-ilp

Algorithm by Gregory Morse from https://codereview.stackexchange.com/questions/1526/
