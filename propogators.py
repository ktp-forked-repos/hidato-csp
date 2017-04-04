from copy import deepcopy

def prop_BT(csp, newVar=None):

    if not newVar:
        return True, []
    for constraint in csp.get_cons_with_var(newVar):
        if constraint.get_n_unasgn() == 0:
            vals = []
            vars = constraint.scope
            for var in vars:
                vals.append(var.value)
            if not constraint.check():
                return False, []
    return True, []

def prop_FC(csp, newVar=None):

    pruned = []
    if newVar:
        cons = [x for x in csp.get_cons_with_var(newVar) if x.get_n_unasgn() is 1]
    else:
        cons = [x for x in csp.get_all_cons() if x.get_n_unasgn() is 1]

    for constraint in cons:
        var = constraint.get_unasgn_vars()[0]
        for coord in deepcopy(var.cur_dom):
            if not constraint.has_support(var, coord):
                var.prune(coord)
                pruned.append((var, coord))

        if len(var.cur_dom) is 0:
            return False, pruned
    return True, pruned

def prop_GAC(csp, newVar=None):

    pruned = []
    constraints = csp.get_all_cons() if not newVar else csp.get_cons_with_var(newVar)

    while constraints:
        constraint = constraints.pop(0)
        for var in constraint.scope[:]:
            for coord in var.cur_dom[:]:
                if not var.fixed:
                    if not constraint.has_support(var, coord):
                        var.prune(coord)
                        pruned.append((var, coord))

                        if not len(var.cur_dom):
                            return False, list(set(pruned))
                        else:
                            for v_cons in csp.get_cons_with_var(var):
                                if v_cons not in constraints:
                                    constraints.append(v_cons)
    return True, pruned
