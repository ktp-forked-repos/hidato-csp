class Variable:

    def __init__(self, val, list_of_vars):
        self.value, self.fixed, self.coord, self.cur_dom = val, False, None, []

    def prune(self, coord):
        self.cur_dom.remove(coord)
    
    def unprune(self, coord):
        self.cur_dom.append(coord)

class Constraint:

    def __init__(self, start, end):
        self.start, self.end = start, end

    def check(self):
        s, e = self.start.coord, self.end.coord
        return abs(s[0] - e[0]) <= 1 and abs(s[1] - e[1]) <= 1

    def has_support(self, var, coord):
        var.coord = coord
        result = self.check()
        var.coord = None
        return result

