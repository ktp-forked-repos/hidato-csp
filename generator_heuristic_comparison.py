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

if __name__ == '__main__':
    board_db = collections.OrderedDict(sorted(board_db.items()))
    with open('experiment_results/heuristic_results_please_rename.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['heuristic'] + list(board_db.keys()))
        for heur in [smallest_cur_dom, next_in_line]:
            row = [heur.__name__]
            for name, b in board_db.items():
                print('Trying', name)
                board = deepcopy(b)
                csp = CSP('CSP', board, heur)
                solver = Backtracking(csp)
                with benchmark() as t:
                    solver.bt_search(prop_FC)
                row.append(t.time)
            writer.writerow(row)
