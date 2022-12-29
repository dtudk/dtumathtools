from sympy import *
from functools import reduce


def __extract_vars(expr):
    return sorted(list(map(lambda x : str(x),expr.free_symbols)))

def taylor(expr,vars,degree):
    if len(vars) != 2 and len(vars) != 4:
        raise Exception("taylor is only defined for one or two variables")
    if len(vars) == 2: return series(expr,vars[0],vars[1],n=degree).removeO()
    P_n = S(0)
    x,x0,y,y0 = vars
    for i in range(degree):
        for j in range(degree - i):
            P_n += expr.diff(x,i).diff(y,j).subs([(x,x0),(y,y0)]) * (x - x0) ** i * (y - y0) ** j / (factorial(i)  * factorial(j))

    return P_n


def gradient(expr):
    var = __extract_vars(expr)
    if(len(var) == 1):
        return expr.diff(var[0])
    return Matrix([expr.diff(v) for v in var])

def hessian(expr,var= None):
    var = __extract_vars(expr) if var is None else var
    return Matrix([[reduce(lambda e,s : e.diff(s),[x,y],expr) for x in var] for y in var])




