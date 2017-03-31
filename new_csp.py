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
        self.coord = coord
        self.board[coord[0]][coord[1]] = self

    def unassign(self):
        self.board[self.coord[0]][self.coord[1]] = None
        self.coord = None

class Constraint2:
    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Con-(' + str(self.x) + ', ' + str(self.y) + ')'

    def check(self):
        x = self.x
        y = self.y
        board_len = len(self.board)*len(self.board[0])
        if not self.board[x][y]: return True
        keystone = self.board[x][y].value
        neighbours = get_neighbours(x, y, self.board)
        if self.board[x][y].value is 1:
            return len([x for x in neighbours if x.value is 2]) is 1
        if self.board[x][y].value is board_len:
            return len([x for x in neighbours if x and x.value is board_len-1]) is 1
        free_space = len([x for x in neighbours if x is None])
        next_to_pre = len([x for x in neighbours if x and x.value is keystone-1]) is 1
        next_to_suc = len([x for x in neighbours if x and x.value is keystone+1]) is 1
        if free_space >= 2: return True
        if free_space is 1 and not next_to_pre and not next_to_suc: return False
        if free_space is 0 and (not next_to_pre or not next_to_suc): return False
        return True

    def has_support(self, var, coord):
        var.coord = coord
        result = self.check()
        var.coord = None
        return result

    def get_unasgn_vars(self):
        if self.board[self.x][self.y] is None: return []
        keystone = self.board[self.x][self.y].value
        return [x for x in get_neighbours(self.x, self.y, self.board) if x and (x.value is keystone-1 or x.value is keystone+1)]

    def get_n_unasgn(self):
        return len(self.get_unasgn_vars())

class Constraint:
    def __init__(self, start, end):
        self.start, self.end = start, end

    def __repr__(self):
        return 'Con-from-' + str(self.start) + '-to-' + str(self.end)

    def check(self):
        if not self.start.coord and not self.end.coord: return True
        s, e = self.start.coord, self.end.coord
        return abs(s[0] - e[0]) <= 1 and abs(s[1] - e[1]) <= 1 and not s == e

    def has_support(self, var, coord):
        var.coord = coord
        result = self.check()
        var.coord = None
        return result

    def get_unasgn_vars(self):
        return [x for x in [self.start, self.end] if not x.coord]

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
                    self.board[row_index][col_index] = self.variables[cell]
        for i in self.variables:
            self.variables[i].cur_dom = deepcopy(open_space)
        for i in range(1, max_val):
            self.constraints.append(Constraint(self.variables[i], self.variables[i+1]))
        #
        # for row_index, row in enumerate(board):
        #     for col_index, cell in enumerate(row):
        #         self.constraints.append(Constraint2(self.board, row_index, col_index))

        self._constraints = deepcopy(self.constraints)
        self._variables = deepcopy(self.variables)

    def get_cons_with_var(self, var):
        return [c for c in self.constraints if var.value in (c.start.value, c.end.value)]

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
        print('BEGINNING A BT_RECURSE -------------------------------------')
        if not self.unasgn_vars:
            return True
        else:
            variables = self.csp.variables
            var = min([var for var in self.unasgn_vars if not var.coord], key = lambda t: len(t.cur_dom))
            self.unasgn_vars.remove(var)
            print(var, 'cur_dom', var.cur_dom)
            for coord in var.cur_dom:
                var.assign(coord)
                print(var, 'assigns', coord)
                for vv in self.unasgn_vars:
                    vv.prune(coord)
                self.num_vassigns += 1
                status, prunings = propagator(self.csp, var)
                print('propagator says ', status)
                self.total_prunings += len(prunings)
                print_hidato_soln(self.csp.board)
                print()
                if status:
                    if self.bt_recurse(propagator, level + 1):
                        return True
                self.restore_coords(prunings)
                var.unassign()
                print(var, 'unassigns', coord)
                for v in self.unasgn_vars:
                    v.unprune(coord)
            self.unasgn_vars.append(var)
            return False

def print_hidato_soln(var_array):
    for row in var_array:
        print([item for item in row])
