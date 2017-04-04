import ast
import sys
import csv
import collections
from copy import deepcopy
from benchmark import benchmark
from cspbase import *
from propogators import *
from hb import *

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
    board_db = collections.OrderedDict(sorted(board_db.items()))
    with open('results.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['propogator'] + list(board_db.keys()))
        for propogator in [prop_BT, prop_FC, prop_GAC]:
            row = [propogator.__name__]
            for name, b in board_db.items():
                if (name in bt_safe_boards or not propogator.__name__ is 'prop_BT') and (name in fc_safe_boards or not propogator.__name__ is 'prop_FC') and (name in gac_safe_boards or not propogator.__name__ is 'prop_GAC'):
                    print('Trying', name)
                    board = deepcopy(b)
                    csp = CSP('CSP', board)
                    solver = Backtracking(csp)
                    with benchmark() as b:
                        solver.bt_search(propogator)
                    row.append(b.time)
            spamwriter.writerow(row)
