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
    with open('experiment_results/propogator_results_please_rename.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['propogator'] + list(board_db.keys()))
        for propogator in [prop_BT, prop_FC, prop_GAC]:
            row = [propogator.__name__]
            for name, b in board_db.items():
                if (name in bt_safe_boards or not propogator.__name__ is 'prop_BT') and (name in fc_safe_boards or not propogator.__name__ is 'prop_FC') and (name in gac_safe_boards or not propogator.__name__ is 'prop_GAC'):
                    print('Trying', name)
                    board = deepcopy(b)
                    csp = CSP('CSP', board, smallest_cur_dom)
                    solver = Backtracking(csp)
                    with benchmark() as t:
                        solver.bt_search(propogator)
                    row.append(t.time)
            writer.writerow(row)
