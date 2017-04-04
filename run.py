from new_csp import *
from propogators import *
import ast
import sys
from copy import deepcopy

def print_hidato_soln(board):
    for row in board:
        print([item.value for item in row if item])

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
    max_val = len(flatten(initial_board))
    lookup_table = {x: True for x in range(1,max_val+1)}

    variables = []
    for row_index, row in enumerate(initial_board):
        for col_index, cell in enumerate(row):
            var = Variable('Var-' + str(row_index) + '-' + str(col_index), lookup_table, {}, cell)
            variables.append(var)
            initial_board[row_index][col_index] = var

    constraints = []
    for row_index, row in enumerate(initial_board):
        for col_index, var in enumerate(row):
            neighbours = get_neighbours(row_index, col_index, initial_board)
            con = Constraint('Con-' + str(row_index) + '-' + str(col_index), var, neighbours)
            constraints.append(con)

    csp = CSP('My CSP', initial_board, constraints, lookup_table)
    return csp, initial_board

if __name__ == "__main__":

    b1 = [
        [5, None, 2],
        [None, 1, None],
        [7, 8, 9],
    ]

    b2 = [
        [9, None, None],
        [7, None, None],
        [1, None, 5],
    ]

    b3 = [
        [1, 2, None, 4],
        [7, 6, 3, 11],
        [None, None, None, None],
        [16, 15, 14, 13],
    ]

    b4 = [
        [1, None, None, None],
        [None, 13, 3, 16],
        [12, None, 4, None],
        [None, None, None, 5],
    ]

    b5 = [
        [None, 15, 3, None],
        [16, None, 2, None],
        [10, None, None, 1],
        [None, None, None, 7],
    ]

    b6 = [
        [None, None, 15, 16],
        [12, None, 1, None],
        [11, None, 3, None],
        [None, None, None, 5],
    ]

    b7 = [
        [1, None, 7, None],
        [None, 2, 5, None],
        [None, 14, None, 11],
        [16, None, None, None],
    ]

    b8 = [
        [None, None, None, None],
        [None, None, None, 1],
        [None, 7, 15, None],
        [None, 8, 16, None],
    ]

    hard_board = [
    [61, None, None, None, None, None, None, None, None, None, None, 116],
    [None, 63, None, None, 68, None, None, 73, None, None, 118, None],
    [None, None, 57, None, None, None, None, None, None, 120, None, None],
    [None, None, None, None, 52, 77, 102, 105, None, None, None, None],
    [None, 40, None, 50, 51, None, None, 106, 109, None, 137, None],
    [None, None, None, 47, None, 79, 100, None, 108, None, None, None],
    [None, None, None, 44, None, 80, 99, None, 95, None, None, None],
    [None, 33, None, 31, 30, None, None, 97, 94, None, 134, None],
    [None, None, None, None, 29, 82, 87, 88, None, None, None, None],
    [None, None, 22, None, None, None, None, None, None, 131, None, None],
    [None, 16, None, None, 19, None, None, 90, None, None, 3, None],
    [14, None, None, None, None, None, None, None, None, None, None, 1]
    ]

    print("Solving board:")
    for row in hard_board:
        for cell in row:
            print(str(cell) + '\t', end='')
        print()

    csp = CSP('FUCK this FUCKING SHITE', hard_board)
    solver = Backtracking(csp)
    solver.bt_search(prop_GAC)
    print_hidato_soln(csp.board)

    # for b in [b1, b2, b3, b4, b5, b6, b7, b8]:
    #     print("Solving board:")
    #     for row in b:
    #         print(row)
    #
    #     print("=======================================================")
    #     csp = CSP('Fucking csp', deepcopy(b))
    #     solver = Backtracking(csp)
    #
    #     solver.bt_search(prop_FC)
    #     print_hidato_soln(csp.board)
    #
    #     print("=======================================================")
    #     csp2 = CSP('Fucking csp', deepcopy(b))
    #     solver = Backtracking(csp2)
    #
    #     print("GAC")
    #     solver.bt_search(prop_GAC)
    #     print_hidato_soln(csp2.board)
