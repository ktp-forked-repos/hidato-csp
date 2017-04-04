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

def next_to(coord1, coord2):
    val = abs(coord1[0] - coord2[0]) <= 1 and abs(coord1[1] - coord2[1]) <= 1 and not coord1 == coord2
    return val

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
        if coord not in self.cur_dom: self.cur_dom.append(coord)

    def assign(self, coord):
        self.fixed = True
        self.coord = coord
        self.board[coord[0]][coord[1]] = self

    def unassign(self):
        self.fixed = False
        self.board[self.coord[0]][self.coord[1]] = None
        self.coord = None

class Constraint:
    def __init__(self, start, middle, end):
        self.start = start
        self.middle = middle
        self.end = end
        self.scope = (self.start, self.middle, self.end)

    def __repr__(self):
        return 'Con-' + str(self.start) + '-' + str(self.middle)+ '-' + str(self.end)

    def check(self):

        if not (self.start.coord and self.middle.coord and self.end.coord): return True
        s, m, e = self.start.coord, self.middle.coord, self.end.coord

        return next_to(s,m) and next_to(m,e) and s != e and s != m and m != e

    def has_support(self, var, coord):

        var.assign(coord)
        result = self.check()
        var.unassign()

        return result

    def get_unasgn_vars(self):
        return [x for x in self.scope if not x.coord]

    def get_n_unasgn(self):
        return len(self.get_unasgn_vars())

class CSP:

    def __init__(self, name, board):
        self.name, self.board = name, board
        self.constraints = []
        self.variables = {}

        open_space = []
        max_val = len(board)*len(board[0])

        for i in range(1, max_val + 1):
            self.variables[i] = Variable('Var-' + str(i), i, self.board)

        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell == None:
                    open_space.append((row_index, col_index))
                else:
                    self.variables[cell].coord = (row_index, col_index)
                    self.variables[cell].fixed = True
                    self.variables[cell].cur_dom = [(row_index, col_index)]
                    self.board[row_index][col_index] = self.variables[cell]

        for i in self.variables:
            if not self.variables[i].fixed:
                self.variables[i].cur_dom = open_space[:]

        for i in range(1, max_val-1):
            self.constraints.append(Constraint(self.variables[i], self.variables[i+1], self.variables[i+2]))

        self._constraints = deepcopy(self.constraints)
        self._variables = deepcopy(self.variables)

    def verify(self):
        pos, remaining, cont = 1, len(self.variables) - 1, True 
        var = self.variables[1]

        while cont:
            cur, nxt = self.variables[pos], self.variables[pos+1] 
            if next_to(cur.coord, nxt.coord):
                cur += 1; remaining -= 1
                if not remaining:
                    cont = False
            else:
                cont = False

        return "Success" if not remaining else "Failure"
        
    def get_cons_with_var(self, var):

        val = var.value

        ret = []
        for constraint in self.constraints:
            if var in constraint.scope:
                ret.append(constraint)

        return ret[:]

    def get_all_cons(self):
        return self.constraints[:]

class Backtracking:
    def __init__(self, csp):
        self.csp = csp
        self.num_vassigns = 0
        self.total_prunings = 0
        self.unasgned_vars = list()
        self.elapsed = 0

    def clear_stats(self):
        self.num_vassigns, self.total_prunings, self.elapsed = 0, 0, 0

    def restore_coords(self, prunings):
        for var, coord in prunings:
            var.unprune(coord)

    def bt_search(self, propagator):
        self.clear_stats()
        stime = time.process_time()
        self.unasgn_vars = [v for v in self.csp.variables.values() if v.coord is None]

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

    def bt_recurse(self, propagator, level):
        if not self.unasgn_vars:
            return True
        else:

            var = min([var for var in self.unasgn_vars if not var.coord], key = lambda t: len(t.cur_dom))

            self.unasgn_vars.remove(var)

            for coord in var.cur_dom:
                var.assign(coord)
                prunes = []

                for vv in self.unasgn_vars:
                    prunes.append((vv, coord))
                    vv.prune(coord)

                self.num_vassigns += 1
                status, prunings = propagator(self.csp, var)

                self.total_prunings += len(prunings)

                if status:
                    if self.bt_recurse(propagator, level + 1):
                        return True

                self.restore_coords(prunings + prunes)

                var.unassign()

            self.unasgn_vars.append(var)

            return False
