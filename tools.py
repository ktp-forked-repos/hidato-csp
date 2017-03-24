def flatten(board):
	""" (lst of lst) -> lst
		Flattens a list of lists into a single list.
	"""
	return [item for l in board for item in l]

