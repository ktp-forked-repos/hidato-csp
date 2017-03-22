import time 
from copy import deepcopy

class Variable:

	# Lookup table maps vals to Fale if on board else True 
	def __init__(self, name, lookup_table, val_to_var):
		""" (self, str, dict int:bool) -> None 
			Inits the variable.	The lookup table is a
			global table of possible vals for all variables
			in the game, storing whether they're available.
		"""
		self.name = name
		self.value = None
		self.l_table = lookup_table
		self.v_to_var = val_to_var
		self.cur_dom = get_curdom()
		self.fixed = False

	def get_curdom(self):
		""" (self) -> None
			Returns vals in the vars current domain.
		"""
		return [val for val, pres in self.l_table if pres]

	def assign(self, val):
		""" (self, int) -> None
			Assigns val to the variable.
		"""
		if self.l_table[val]:
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
		if not self.fixed():
			self.v_to_var[self.value] = None
			self.l_table[self.value] = True
			self.value = None
	
	def prune_val(self, value):
		""" (self, int) -> None
		Removes value from the vars curdom. 
		"""
		self.cur_dom.remove(value)
		
	def unprune_val(self, value):
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

	def check(self):
		# TODO: edge case for first and last variables
		l_table = self.keystone.l_table
		center = self.keystone.value
		if center is None: return True
		predecessor, successor = center - 1, center + 1
		number_of_open_adj = len([x for x in self.scope if x is None])
		p, s = True, True
		for neighbour in self.scope:
			if neighbour.value is predecessor: p = False
			if neighbour.value is successor: s = False
		if p and s:
			if number_of_open_adj < 2: return False
			if not (l_table[predecessor] and l_table[successor]): return False
		else if p or s:
			if not number_of_open_adj: return False
			if p and not l_table[predecessor]: return False
			if s and not l_table[successor]: return False
		return True

class CSP:

	def __init__(self, name, variables, initial_board):
		""" (self, str, iterable of variables, lst of lst) -> None
			Inits the CSP. Initial board is a lst-lst of ints and Nones
			determining the board's initial config.
		"""
		self.name, self.variables, self.board = name, variables, initial_board
		c_max = self.get_max_val()
		fixed = self.get_preassigned()

		self.val_to_var = {x: None for x i nrange(c_max)}
		self.lookup_table = {x: True for x in range(c_max)}

		# Set both dictionaries
		for val in self.lookup_table:
			result = [(v, pos) for v, pos in fixed if v == val]

			if len(result):
				pos = result[1][1]
				self.lookup_table[val] = False
				self.variables[pos].assign(val)
				self.variables[pos].fixed = True
				self.val_to_var[val] = self.variables[pos]

		# Make backups for quicker restores
		self._lookup_table = deepcopy(self.lookup_table)
		self._val_to_var = deepcopy(self.val_to_var)

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
		return [(y, x) for x, y in enumerate(flatten(self.board)) if type(y) == int]

	def restore_vars(self):
		""" Restores the initial state of all variables """ 
		# Restore from backups, re-init vars
		self.lookup_table = deepcopy(self._lookup_table)
		self.val_to_var = deepcopy(self._val_to_var)

		for var in self.variables():
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
		p2 " variable assignments and pruned {}".format(self.total_prunings)
		p3 = " variable values"
		print(p1 + p2 + p3)

	def restore_values(self, prunings):
		""" Restore all values that were pruned. """  
		for var, val in prunings:
			var.unprune_val(val)
	
	def restore_values(self, prunings):
		""" lst of tuples of var, val -> None
		Restores all prunings.	
		"""
		# Dicks out 
		[var.unprune_val(val) for var, val in prunings]
		
	def bt_search(self, propogator):
		""" Backtrack like a mufucka """
		self.clear_stats()
		stime = time.process_time()

		self.csp.restore_vars()

		self.unasgn_vars = [var for var in self.csp.variables if var.val is None]

		status, prunings = propagator(self.csp)
		self.total_prunings += prunings

		if status == False:
			print("Propogator detected an error at the current root.")
		else:
			status = self.bt_Recurse(propogator, 1)

		self.restore_values(prunings)

		print("Solved!") if status else print("Shit..")

		self.print_stats()

	def bt_recurse(self, propogator, level):

		if not self.unasgn_vars:
			return True
		else:
			variables = self.csp.variables()
			var = min([(len(x.cur_dom), x) for x in variables if not x.value])
			self.unasgn_vars.remove(var)

			for val in var.cur_domain():
				
				var.assign(val)
				self.num_vassigns += 1
				
				status, prunings = propogator(self.csp, var)
				self.total_prunings += len(prunings)

				if status:
					if self.bt_recurse(propogator, level + 1):
						return True

				# TODO Still need to do this 
				self.restore_values(prunings)

				var.unassign() 

			self.unasgn_vars.append(var)

			return False	

