import time
from copy import deepcopy
from tools import flatten

class Variable:
    def __init__(self, name, lookup_table, val_to_var, value=None):
        """ (self, str, dict int:bool) -> None
            Inits the variable.    The lookup table is a
            global table of possible vals for all variables
            in the game, storing whether they're available.
        """
        self.name = name
        self.value = value
        self.l_table = lookup_table
        self.v_to_var = val_to_var
        self.cur_dom = [val for val, pres in self.l_table.items() if pres]
        self.fixed = False

    def __repr__(self):
        return self.name + ":" + str(self.value)

    def assign(self, val):
        """ (self, int) -> None
            Assigns val to the variable.
        """
        if self.l_table[val] and not self.fixed:
            self.value = val
            self.l_table[val] = False
            self.v_to_var[val] = self
        else:
            return False

    def unassign(self):
        """ (self) -> None
            Unassigns the current value and marks it free
            in the lookup table.
        """
        if not self.fixed and self.value:
            self.v_to_var[self.value] = None
            self.l_table[self.value] = True
            self.value = None

    def prune_value(self, value):
        """ (self, int) -> None
        Removes value from the vars curdom.
        """
        self.cur_dom.remove(value)

    def unprune_value(self, value):
        """ Undoes the last thing. """
        self.cur_dom.append(value)


class Constraint:
    def __init__(self, name, keystone, scope):
        """ (self, str, variable, iterable of variables, fn)
            Inits the constraint. Keystone refers to the stone
            that the constraint revolves around.
        """
        self.name = name
        self.scope = scope # list of vars
        self.keystone = keystone # center var

    def __repr__(self):
        return self.name

    def check(self):
        l_table = self.keystone.l_table
        center = self.keystone.value

        if center is None:
            return True

        number_of_open_adj = len([x for x in self.scope if x.value is None])
        if self.keystone.value is 1:
            for neighbour in self.scope:
                if neighbour.value is 2:
                    return True
            if not l_table[2]:
                return False
            if number_of_open_adj is 0:
                return False
            return True

        # TODO: FIX THIS SHIT
        if center is 9:
            for neighbour in self.scope:
                if neighbour.value is 8:
                    return True
            if not l_table[8]:
                return False
            if number_of_open_adj is 0:
                return False
            return True

        predecessor, successor = center - 1, center + 1
        p, s = True, True
        for neighbour in self.scope:
            if neighbour.value is predecessor:
                p = False
            if neighbour.value is successor:
                s = False
        if p and s:
            if number_of_open_adj < 2:
                return False
            if not (l_table[predecessor] and l_table[successor]):
                return False
        elif p or s:
            if number_of_open_adj is 0:
                return False
            if p and not l_table[predecessor]:
                return False
            if s and not l_table[successor]:
                return False
        return True

    def has_support(self, var, val):
        """ (self, Variable, int) -> Bool
        Returns True if var can support val under the constraint,
        False otherwise.
        """
        # Dicks out
        var.assign(val)
        evaluated = self.check()
        var.unassign()
        return evaluated

    def get_unasgn_vars(self):
        """ (self) -> list of var
            Returns all unassigned variables.
        """
        return [var for var in self.scope if var.value is None]

    def get_n_unasgn(self):
        """ (self) -> int
        Returns the number of unassigned variables
        """
        return len(self.get_unasgn_vars())

class CSP:
    def __init__(self, name, initial_board, constraints, lookup_table):
        """ (self, str, lst of lst of variables, lst of constraints) -> None
            Inits the CSP. Initial board is a lst-lst of variables
            determining the board's initial config.
        """
        self.name, self.board, self.lookup_table = name, initial_board, lookup_table
        self.variables = flatten(initial_board)
        self.constraints = constraints

        c_max = self.get_max_val()
        fixed = self.get_preassigned()

        self.val_to_var = {x: None for x in range(1,c_max+1)}

        # Set both dictionaries
        for val in self.lookup_table:
            result = [(v, pos) for v, pos in fixed if v.value is val]
            if len(result):
                pos = result.pop()[1]
                self.lookup_table[val] = False
                self.variables[pos].assign(val)
                self.variables[pos].fixed = True
                self.val_to_var[val] = self.variables[pos]

        for var in self.variables:
            for fixed_var, _ in fixed:
                if not var.fixed:
                    var.prune_value(fixed_var.value)

        # Make backups for quicker restores
        self._lookup_table = deepcopy(self.lookup_table)
        self._val_to_var = deepcopy(self.val_to_var)

    def get_cons_with_var(self, var):
        """ (self, Variable) -> lst of Variable
            Returns a list of constraints with var in their scope.
        """
        return [c for c in self.constraints if var in c.scope]

    def get_all_cons(self):
        """ (self) -> list of Constraint
            Returns all constraints.
        """
        return self.constraints

    def check_done(self):
        """ (self) -> Bool
            Determines whether the game is over.
        """
        return True not in [x for x in self.lookup_table.values()]

    def get_max_val(self):
        """ (self) -> None
            Returns the largest value on the board.
            This is always predefined.
        """
        return len(flatten(self.board))

    def get_preassigned(self):
        """ (self) -> lst of tuples
            Gets all values (and their indices) fixed into the board.
        """
        return [(y, x) for x, y in enumerate(flatten(self.board)) if type(y.value) == int]

    def restore_vars(self):
        """ Restores the initial state of all variables """
        # Restore from backups, re-init vars
        self.lookup_table = deepcopy(self._lookup_table)
        self.val_to_var = deepcopy(self._val_to_var)

        for var in self.variables:
            var.l_table = self.lookup_table
            var.v_to_var = self.val_to_var
            var.unassign()


def flatten(board):
    """ (lst of lst) -> lst
        Flattens a list of lists into a single list.
    """
    return [item for l in board for item in l]


class Backtracking:
    """ This class takes a CSP, and then can be used to
    run a backtracking routine with different propogators. """

    def __init__(self, csp):
        """ (self, CSP) -> None
            Inits the backtracking routine, sets up stat tracking.
        """
        self.csp = csp
        self.num_vassigns = 0
        self.total_prunings = 0
        self.unasgned_vars = list()
        self.elapsed = 0

    def clear_stats(self):
        """ (self) -> None
            Resets all stats.
        """
        self.num_vassigns, self.total_prunings, self.elapsed = 0, 0, 0

    def print_stats(self):
        """ (self) -> None """
        p1 = "Search made {}".format(self.num_vassigns)
        p2 = " variable assignments and pruned {}".format(self.total_prunings)
        p3 = " variable values"
        print(p1 + p2 + p3)

    def restore_values(self, prunings):
        """ Restore all values that were pruned. """
        for var, val in prunings:
            var.unprune_value(val)

    def restore_values(self, prunings):
        """ lst of tuples of var, val -> None
        Restores all prunings.
        """
        # Dicks out
        [var.unprune_value(val) for var, val in prunings]

    def bt_search(self, propagator):
        """ Backtrack like a mufucka """

        self.clear_stats()
        stime = time.process_time()

        self.csp.restore_vars()

        self.unasgn_vars = [var for var in self.csp.variables if var.value is None]

        status, prunings = propagator(self.csp)

        self.total_prunings += len(prunings)

        if status == False:
            print("Propogator detected an error at the current root.")
        else:
            status = self.bt_recurse(propagator, 1)

        self.restore_values(prunings)

        if status:
            print("Solved!")
        else:
            print("Shit..")

        self.print_stats()

    def bt_recurse(self, propogator, level):
        if not self.unasgn_vars:
            return True
        else:
            variables = self.csp.variables
            var = min([x for x in variables if not x.value], key = lambda t: len(t.cur_dom))
            self.unasgn_vars.remove(var)
   
            for val in var.cur_dom:

                var.assign(val)

                self.num_vassigns += 1
                status, prunings = propogator(self.csp, var)

                self.total_prunings += len(prunings)

                if status:
                    if self.bt_recurse(propogator, level + 1):
                        print(val, 'exiting')
                        return True

                # TODO Still need to do this
                self.restore_values(prunings)

                var.unassign()

            self.unasgn_vars.append(var)

            return False
