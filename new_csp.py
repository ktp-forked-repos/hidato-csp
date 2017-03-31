import time
from copy import deepcopy, copy

def get_neighbours(x, y, m):
    l = []
    for xx in [-1, 0, 1]:
        for yy in [-1, 0, 1]:
            if xx is 0 and yy is 0: continue
            if x + xx < 0 or y + yy < 0 or x + xx is len(m[0]) or y + yy is len(m):
                continue
            l.append(m[x+xx][y+yy])
    return l

class Variable:
    def __init__(self, name, value, board):
        self.name = name
        self.value = value
        self.board = board
        self.fixed = False
        self.coord = None
        self.cur_dom = []

    def __repr__(self):
        return self.name

    def prune(self, coord):
        if coord in self.cur_dom: self.cur_dom.remove(coord)

    def unprune(self, coord):
        self.cur_dom.append(coord)

    def assign(self, coord):
        # print(self, 'assigns', coord)
        # for row in self.board:
        #     print(row)
        self.coord = coord
        self.board[coord[0]][coord[1]] = self

    def unassign(self):
        # print(self, 'unassigns')
        self.board[self.coord[0]][self.coord[1]] = None
        self.coord = None

def next_to(coord1, coord2):
    return abs(coord1[0] - coord2[0]) <= 1 and abs(coord1[1] - coord2[1]) <= 1 and not coord1 == coord2

class Constraint:
    def __init__(self, start, middle, end):
        self.start = start
        self.middle = middle
        self.end = end
        self.scope = [self.start, self.middle, self.end]

    def __repr__(self):
        return 'Con-' + str(self.start) + '-' + str(self.middle)+ '-' + str(self.end)

    def check(self):
        if not self.start.coord or not self.middle.coord or not self.end.coord: return True
        s, m, e = self.start.coord, self.middle.coord, self.end.coord
        return next_to(s,m) and next_to(m,e) and s is not e

    def has_support(self, var, coord):
        oldvar = var.board[coord[0]][coord[1]]
        var.assign(coord)
        result = self.check()
        var.unassign()
        if oldvar: oldvar.assign(coord)
        return result

    def get_unasgn_vars(self):
        return [x for x in [self.start, self.middle, self.end] if not x.coord]

    def get_n_unasgn(self):
        return len(self.get_unasgn_vars())


class CSP:
    def __init__(self, name, board):
        self.name, self.board = name, deepcopy(board)
        self.constraints = []
        self.variables = {}
        open_space = []
        max_val = len(board)*len(board[0])
        for i in range(1, max_val + 1):
            self.variables[i] = Variable('Var-' + str(i), i, copy(self.board))
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell is None:
                    open_space.append((row_index, col_index))
                else:
                    self.variables[cell].coord = (row_index, col_index)
                    self.variables[cell].fixed = True
                    self.variables[cell].cur_dom = [(row_index, col_index)]
                    self.board[row_index][col_index] = self.variables[cell]
        for i in self.variables:
            if not self.variables[i].fixed:
                self.variables[i].cur_dom = deepcopy(open_space)
        for i in range(1, max_val-1):
            self.constraints.append(Constraint(self.variables[i], self.variables[i+1], self.variables[i+2]))
        #
        # for row_index, row in enumerate(board):
        #     for col_index, cell in enumerate(row):
        #         self.constraints.append(Constraint2(self.board, row_index, col_index))

        self._constraints = deepcopy(self.constraints)
        self._variables = deepcopy(self.variables)

    def get_cons_with_var(self, var):
        return [c for c in self.constraints if var.value in (c.start.value, c.middle.value, c.end.value)]

    def get_all_cons(self):
        return self.constraints


class Backtracking:
    def __init__(self, csp):
        self.csp = csp
        self.num_vassigns = 0
        self.total_prunings = 0
        self.unasgned_vars = list()
        self.elapsed = 0

    def clear_stats(self):
        self.num_vassigns, self.total_prunings, self.elapsed = 0, 0, 0

    def print_stats(self):
        p1 = "Search made {}".format(self.num_vassigns)
        p2 = " variable assignments and pruned {}".format(self.total_prunings)
        p3 = " variable values"
        print(p1 + p2 + p3)

    def restore_coords(self, prunings):
        for var, coord in prunings:
            var.unprune(coord)

    def bt_search(self, propagator):
        self.clear_stats()
        stime = time.process_time()
        self.unasgn_vars = [v for i,v in self.csp.variables.items() if v.coord is None]
        status, prunings = propagator(self.csp)
        # print('init prunings', prunings)
        self.total_prunings += len(prunings)
        if status:
            status = self.bt_recurse(propagator, 1)
        else:
            print("Propogator detected an error at the current root.")
        self.restore_coords(prunings)
        if status:
            print('Solved!')
        else:
            print('Not Solved :(')
        # self.print_stats()

    def bt_recurse(self, propagator, level):
        # print('BEGINNING A BT_RECURSE -------------------------------------')
        # for i, v in self.csp.variables.items():
        #     print(v, v.cur_dom)
        if not self.unasgn_vars:
            return True
        else:
            variables = self.csp.variables
            var = min([var for var in self.unasgn_vars if not var.coord], key = lambda t: len(t.cur_dom))
            self.unasgn_vars.remove(var)
            # print(var, 'cur_dom', var.cur_dom)
            for coord in var.cur_dom:
                var.assign(coord)
                # print(var, 'assigns', coord)
                for vv in self.unasgn_vars:
                    vv.prune(coord)
                self.num_vassigns += 1
                status, prunings = propagator(self.csp, var)
                # print('propagator says ', status)
                self.total_prunings += len(prunings)
                # print_hidato_soln(self.csp.board)
                # print()
                if status:
                    if self.bt_recurse(propagator, level + 1):
                        return True
                self.restore_coords(prunings)
                var.unassign()
                # print(var, 'unassigns', coord)
                for v in self.unasgn_vars:
                    v.unprune(coord)
            self.unasgn_vars.append(var)
            return False

def print_hidato_soln(var_array):
    for row in var_array:
        print([item for item in row])
