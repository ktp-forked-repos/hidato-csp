class Variable:

	# Lookup table maps vals to Fale if on board else True 
	def __init__(self, name, lookup_table):
		""" (self, str, dict int:bool) -> None 
			Inits the variable.	The lookup table is a
			global table of possible vals for all variables 
			in the game, storing whether they're available.
		"""
		self.name = name
		self.value = None
		self.l_table = lookup_table

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
		else:
			return False
	
	def unassign(self):
		""" (self) -> None 
			Unassigns the current value and marks it free
			in the lookup table.
		"""
		self.l_table[self.value] = True
		self.value = None

class Constraint: 

	# TODO: Is keystone a variable or coordinate?
	def __init__(self, name, keystone, scope, eval_fn):
		""" (self, str, variable, iterable of variables, fn) 
			Inits the constraint. Keystone refers to the stone
			that the constraint revolves around.
		"""
		self.name = name
		self.scope = scope
		self.eval_fn = eval_fn
		self.keystone = keystone
	
	def evaluate(self):
		""" (self) -> bool 
			Evaluates whether the constraint is satisfied.	
		"""
		return self.eval_fn(self.keystone, self.scope)
	
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

		for val in self.lookup_table:
			result = [(v, pos) for v, pos in fixed if v == val]

			if len(result):
				pos = result[1][1]
				self.lookup_table[val] = False
				self.variables[pos].assign(val)
				self.val_to_var[val] = self.variables[pos]

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
		pass
