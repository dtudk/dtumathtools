from sympy import *
from functools import reduce
from typing import Union

def _extract_vars(expr):
    return [e[1] for e in sorted(list(map(lambda x: (str(x),x), expr.free_symbols)))]


def taylor(expr, vars, degree):
    if len(vars) != 2 and len(vars) != 4:
        raise Exception("taylor is only defined for one or two variables")
    if len(vars) == 2:
        return series(expr, vars[0], vars[1], n=degree).removeO()
    P_n = S(0)
    x, x0, y, y0 = vars
    for i in range(degree):
        for j in range(degree - i):
            P_n += (
                expr.diff(x, i).diff(y, j).subs([(x, x0), (y, y0)])
                * (x - x0) ** i
                * (y - y0) ** j
                / (factorial(i) * factorial(j))
            )

    return P_n


def gradient(expr, var=None):
    var = _extract_vars(expr) if var is None else var
    if len(var) == 1:
        return expr.diff(var[0])
    return Matrix([expr.diff(v) for v in var])


def hessian(expr, var=None):
    var = _extract_vars(expr) if var is None else var
    return Matrix(
        [[reduce(lambda e, s: e.diff(s), [x, y], expr) for x in var] for y in var]
    )


def _extract_field_vars(V, var, namefunc):
    var = _extract_vars(V) if var is None else var
    
    # if 3 variables cannot be found, dummy variable is returned,
    # such that differentiating wrt. to it results in 0.
    while len(var) < 3:
        var.append(symbols("_dummy"))
        
    return var


def div(V, var=None):
    var = _extract_field_vars(V, var, "div")

    return sum([V[i].diff(f) for i, f in enumerate(var)])


def rot(V, var=None):
    var = _extract_field_vars(V, var, "rot")

    return Matrix(
        [
            V[2].diff(var[1]) - V[1].diff(var[2]),
            V[0].diff(var[2]) - V[2].diff(var[0]),
            V[1].diff(var[0]) - V[0].diff(var[1]),
        ]
    )


def dsolve(ODE: Union[Eq, list, Matrix], ics=None) -> dict:
    """ A wrapper for the sympy dsolve-function. Instead of a list of equations
        denoting the solution, this function returns a dictionary of solutions.

        // This makes it easier to substitute solution in the places it's needed

        ## Input:
            ODE: one or multiple differential equations to be solved by sympy

        ## Returns:
            sol: a dictionary containing solutions to 'ODE'
        
    """
    
    # Common problem for people is making an single equation, but with both sides
    # being Matrices. This alleviates that issue, and lets users think less
    if type(ODE) == Eq and type(ODE.lhs) == type(ODE.rhs) == Matrix:
            sol = dsolve(ODE.lhs - ODE.rhs, ics=ics)
    else:
        sol = dsolve(ODE, ics=ics)

    return {eq.lhs : eq.rhs for eq in sol}


def l2_norm( v: Matrix ):
    """ Computes the l2-norm for a Matrix-class object, without using
        absolute values on entries, for easier simplification and integration

        ## Input:
            v: A sympy Matrix
    """
    return sqrt(sum(x**2 for x in v))