import ast
import sys
import csv
import collections
from copy import deepcopy
from benchmark import benchmark
from cspbase import *
from propogators import *
from hb import *
from heuristics import *

def print_problem(board):
    for row in board:
        for cell in row:
            if cell:
                print(str(cell) + ' ' * (3 - len(str(cell))), end='')
            else:
                print('-' + ' ' * 2, end='')
        print()

def print_soln(board):
    for row in board:
        for cell in row:
            print(str(cell.value) + ' ' * (3 - len(str(cell.value))), end='')
        print()

if __name__ == "__main__":
    boards = sys.argv[1:]
    for board in boards:
        b = board_db[board]
        print('Problem Board')
        print_problem(b)
        csp = CSP('CSP', b, smallest_cur_dom)
        solver = Backtracking(csp)
        with benchmark() as t:
            solver.bt_search(prop_FC)
        print('Time:', t.time)
        print_soln(csp.board)
