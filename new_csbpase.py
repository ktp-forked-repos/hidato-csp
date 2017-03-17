class Variable:

	# Lookup table maps vals to Fale if on board else True 
	def __init__(self, name, lookup_table):
		self.name = name
		self.value = None
		self.l_table = lookup_table

	def get_curdom(self):
		return [val for val, pres in self.l_table if pres]

	def assign(val):
		if self.l_table[val]:
			self.value = val
			self.l_table[val] = False
		else:
			return False
	
	def unassign(val):
		self.value = None
		self.l_table[val] = True

class Constraint: 

	def __init__(self, name, keystone, scope, eval_fn):
		self.name = name
		self.scope = scope
		self.eval_fn = eval_fn
		self.keystone = keystone
	
	def evaluate(self):
		return self.eval_fn(self.keystone, self.scope)
	

class CSP:

	def __init__(self, name, variables, initial_board):
		self.name = name
		self.variables = variables
		self.board = initial_board

		c_max = self.get_max_val()
		nums = self.get_preassigned()

		self.lookup_table = {x: True for x in range(c_max)}
		for x in self.lookup_table:
			if x in nums:
				self.lookup_table[x] = False

	def check_done(self):
		return True not in [x for x in self.lookup_table.values()] 

	def get_max_val(self):
		""" Gets the max val in the board. """
		return len(flatten(self.board))

	def get_preassigned(self):
		""" Gets all values fixed into the board. """
		return [x for x in flatten(self.board) if type(x) == int]

	def set_initial_board: 


def flatten(board):
	return [item for l in board for item in l]

class Backtracking:
	pass
