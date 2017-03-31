from copy import deepcopy

class CSP:
    def __init__(self, name, board):
        self.name, self.board = name, board
        self.constraints = []
        self.variables = {}
        self.open_space = []
        max_val = len(board)*len(board[0])
        for i in range(1, max_val + 1):
            self.variables[i] = Variable('Var-' + str(i), i)
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell is None:
                    self.open_space.push((row_index, col_index))
                else:
                    self.variables[cell].coord = (row_index, col_index)
                    self.variables[cell].fixed = True
                    board[row_index][col_index] = self.variables[cell]
        for i in self.variables:
            self.variables[i].cur_dom = self.open_space
        for i in range(1, max_val):
            self.constraints.append(Constraint(self.variables[i], self.variables[i+1]))

        self._constraints = deepcopy(self.constraints)
        self._variables = deepcopy(self.variables)
        self._open_space = deepcopy(self.open_space)

    def get_cons_with_var(self, var):
        return [c for c in self.constraints if var is c.start or var is s.end]

    def get_all_cons(self):
        return self.constraints

    def check_done(self):
        return len(self.open_space) is 0

    def restore_vars(self):
        self.constraints = deepcopy(self._constraints)
        self.variables = deepcopy(self._variables)
        self.open_space = deepcopy(self._open_space)


class Variable:
    def __init__(self, name, value):
        self.name, self.value, self.fixed, self.cur_dom = name, value, False, []

    def __repr__(self):
        return self.name


class Constraint:
    def __init__(self, start, end):
        self.start, self.end = start, end

    def __repr__(self):
        return 'Con-from-' + str(self.start) + '-to-' + str(self.end)




csp = CSP('lol', [[1,2,3],[4,5,6]])
