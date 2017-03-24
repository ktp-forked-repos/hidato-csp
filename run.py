from cspbase import *
from propogators import *
import ast
import sys

b1 = [
    [5, None, 2],
    [None, 1, None],
    [7, None, 9],
]

b2 = [
    [9, None, None],
    [7, None, None],
    [1, None, 5],
]


def print_hidato_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])


def hitado_csp_model(initial_board):
    return [], initial_board


if __name__ == "__main__":
    for b in [b1, b2]:
        print("Solving board:")
        for row in b:
            print(row)
        csp, var_array = hitado_csp_model(b)
        solver = Backtracking(csp)
        print("=======================================================")
        print("FC")
        # solver.bt_search(prop_FC)
        print("Solution")
        print_hidato_soln(var_array)
