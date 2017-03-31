def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.scope
            for var in vars:
                vals.append(var.value)
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    pruned = []
    if newVar:
        cons = [x for x in csp.get_cons_with_var(newVar) if x.get_n_unasgn() is 1]
    else:
        cons = [x for x in csp.get_all_cons() if x.get_n_unasgn() is 1]

    for constraint in cons:
        var = constraint.get_unasgn_vars()[0]
        rem = []
        for coord in var.cur_dom:
            if not constraint.has_support(var, coord):
                pruned.append((var, coord))
                rem.append(coord)
        for coord in rem:
            var.prune(coord)
        for con in csp.get_all_cons():
            if not con.check():
                return False, pruned
        # if len(var.cur_dom) is 0:
        #     return False, pruned
    return True, pruned

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    pruned = []
    constraints = csp.get_all_cons() if not newVar else csp.get_cons_with_var(newVar)

    while constraints:
        constraint = constraints.pop(0)
        for var in constraint.scope:
            for val in var.cur_dom:
                if not constraint.has_support(var, val):
                    pruned.append((var, val))
                    var.prune_value(val)

                    if not len(var.cur_dom):
                        return False, pruned # Deadlock
                    else:
                        var_constraints = csp.get_cons_with_var(var)
                        for v_cons in var_constraints:
                            if v_cons not in constraints:
                                constraints.append(v_cons)

    return True, pruned
