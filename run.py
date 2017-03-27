from cspbase import *
from propogators import *
import ast
import sys

b1 = [
    [5, None, 2],
    [6, 1, None],
    [7, None, 9],
]

b2 = [
    [9, None, None],
    [7, None, None],
    [1, None, 5],
]


def print_hidato_soln(var_array):
    for row in var_array:
        print([var.value for var in row])

def flatten(board):
    """ (lst of lst) -> lst
        Flattens a list of lists into a single list.
    """
    return [item for l in board for item in l]


def get_neighbours(x, y, m):
    l = []
    for xx in [-1, 0, 1]:
        for yy in [-1, 0, 1]:
            if xx is 0 and yy is 0: continue
            if x + xx < 0 or y + yy < 0 or x + xx is len(m[0]) or y + yy is len(m):
                continue
            l.append(m[x+xx][y+yy])
    return l

def hitado_csp_model(initial_board):

    # Set up Variables
    max_val = len(flatten(initial_board))
    lookup_table = {x: True for x in range(1,max_val+1)}
    variables = []
    for row_index, row in enumerate(initial_board):
        for col_index, cell in enumerate(row):
            var = Variable('Var-' + str(row_index) + '-' + str(col_index), lookup_table, {}, cell)
            variables.append(var)
            initial_board[row_index][col_index] = var

    # Set up Constraints
    constraints = []
    for row_index, row in enumerate(initial_board):
        for col_index, var in enumerate(row):
            neighbours = get_neighbours(row_index, col_index, initial_board)
            con = Constraint('Con-' + str(row_index) + '-' + str(col_index), var, neighbours)
            constraints.append(con)

    csp = CSP('My CSP', initial_board, constraints, lookup_table)
    return csp, initial_board


if __name__ == "__main__":
    for b in [b1]:
        print("Solving board:")
        for row in b:
            print(row)
        csp, var_array = hitado_csp_model(b)
        solver = Backtracking(csp)
        print("=======================================================")
        print("FC")
        solver.bt_search(prop_FC)
        print("Solution")
        print_hidato_soln(var_array)
