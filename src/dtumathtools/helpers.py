from sympy import *
from functools import reduce


def _extract_vars(expr):
    return sorted(list(map(str, expr.free_symbols)))


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
    if len(var) < 3 and all([f in ["x", "y", "z"] for f in var]):
        x, y, z = symbols("x,y,z")
        var = [x, y, z]
    elif len(var) != 3:
        raise Exception(
            f"{namefunc} found the variables {var}, but expected 3 variables. \n" +
            f"Try specifying the variables using the 'var' keyword argument like: {namefunc}(V, var=(x,y,z))."
        )
    return var


def div(V, var=None):
    if var is None:
        var = _extract_field_vars(V, var, "div")

    return sum([V[i].diff(f) for i, f in enumerate(var)])


def rot(V, var=None):
    if var is None:
        var = _extract_field_vars(V, var, "rot")

    return Matrix(
        [
            V[2].diff(var[1]) - V[1].diff(var[2]),
            V[0].diff(var[2]) - V[2].diff(var[0]),
            V[1].diff(var[0]) - V[0].diff(var[1]),
        ]
    )

if __name__ == "__main__":
    x, y, z = symbols("x y z")
    ## Example 1
    U = Matrix([x, y, z])
    V = Matrix([-y, x, 1])
    print(div(U))
    print(div(V))

    ## Example 2
    U = Matrix([x, y, z])
    V = Matrix([-y, x, 1])
    print(div(U, var=[x, y, z]))
    print(div(V, var=[x, y]))