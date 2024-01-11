from sympy import *
from sympy import dsolve as sym_dsolve
from functools import reduce
from typing import Union, Optional, List
import warnings
from sympy.core import Symbol, Expr
from sympy.matrices import MatrixBase
import inspect


def _extract_vars(expr: Expr) -> (List[Symbol]):
    """From a sympy expression, extract the free variables sorted by their name.

    Args:
        expr (Expr): Sympy expression to find free variables in.

    Returns:
        List[Symbol]: Sorted list of symbols
    """
    return [e[1] for e in sorted(list(map(lambda x: (str(x), x), expr.free_symbols)))]


def taylor(expr: Expr, vars: List[Symbol], degree: int) -> (Expr):
    """Find the taylor expansion of an expression.

    Args:
        expr (Expr): Sympy expression to do taylor expansion on.
        vars (List[Symbol]): List of symbols to expand on.
        degree (int): Degree of the taylor expansion

    Raises:
        Exception: This function is only defined for one or two variables.

    Returns:
        Expr: The given expression taylor expanded.
    """
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


def gradient(expr: Expr, var: Optional[List[Symbol]] = None) -> (MatrixBase):
    """Find the gradient of an expression.

    Args:
        expr (Expr): The sympy expression to find the gradient off.
        var (List[Symbol], optional): List of variables to take the gradient with respect to. Defaults to None.

    Returns:
        MatrixBase: The gradient of the expression for the given variables.
    """
    var = _extract_vars(expr) if var is None else var
    if len(var) == 1:
        return expr.diff(var[0])
    return Matrix([expr.diff(v) for v in var])


def hessian(expr: Expr, var: Optional[Symbol] = None) -> (MatrixBase):
    """Find the hessian of an expression.

    Args:
        expr (Expr): The sympy expression to find the hessian off.
        var (list[Symbol], optional): List of variables to find the hessian with respect to. Defaults to estimating them from expr.

    Returns:
        MatrixBase: The hessian of the expression for the given variables.
    """
    var = _extract_vars(expr) if var is None else var
    return Matrix(
        [[reduce(lambda e, s: e.diff(s), [x, y], expr) for x in var] for y in var]
    )


def _extract_field_vars(
    V: MatrixBase, var: Union[List[Symbol], None], namefunc: str
) -> (List[Symbol]):
    """Extract variables used for field (3D) functions.

    Args:
        V (MatrixBase): 3D matrix representing a vector field spanning the variables.
        var (List[Symbol] | None): The 3 variables which the vector field spans. Defaults to estimating them from V.

    Raises:
        AssertionError: Exactly 3 variables (or None) must be specified.

    Returns:
        List[Symbol]: The stated or extracted variables that V spans.
    """

    if var is None:
        var = _extract_vars(V)

        _x, _y, _z = symbols("x,y,z")
        _u, _v, _w = symbols("u,v,w")

        error_str = f"ERROR! Could not guess the variables used. Please specify the variables using {namefunc}(V, var=[x,y,z])."
        warning_str = (
            f"Warning! Variables were not specified. Assuming variables are {var}!"
        )
        assert all(v in [_x, _y, _z, _u, _v, _w] for v in var), error_str

        if all(v in [_x, _y, _z] for v in var):
            var = [_x, _y, _z]
            warnings.warn(warning_str, UserWarning)
        elif all(v in [_u, _v, _w] for v in var):
            var = [_u, _v, _w]
            warnings.warn(warning_str, UserWarning)
        else:
            raise AssertionError(error_str)

    assert len(var) == 3, "Exactly 3 variables must be specified!"

    return var


def div(V: MatrixBase, var: Optional[List[Symbol]] = None) -> (Expr):
    """Find the divergence of a vector field

    Args:
        V (MatrixBase): 3D matrix representing a vector field spanning the variables.
        var (List[Symbol], optional): The 3 variables which the vector field spans. Defaults to estimating them from V.

    Returns:
        Expr: The divergence of the vector field with respect to the given variables.
    """

    var = _extract_field_vars(V, var, "div")

    return sum([V[i].diff(f) for i, f in enumerate(var)])


def rot(V: MatrixBase, var: Optional[List[Symbol]] = None) -> (MatrixBase):
    """Find the rotation of a vector field

    Args:
        V (MatrixBase): 3D matrix representing a vector field spanning the variables.
        var (List[Symbol], optional): The 3 variables which the vector field spans. Defaults to estimating them from V.

    Returns:
        MatrixBase: The rotation of the vector field with respect to the given variables.
    """
    var = _extract_field_vars(V, var, "rot")

    return Matrix(
        [
            V[2].diff(var[1]) - V[1].diff(var[2]),
            V[0].diff(var[2]) - V[2].diff(var[0]),
            V[1].diff(var[0]) - V[0].diff(var[1]),
        ]
    )


def dsolve(ODE: Union[Eq, list, Matrix], ics: Optional[dict] = None) -> (dict):
    """A wrapper for the sympy dsolve-function. Instead of a list of equations denoting the solution, this function returns a dictionary of solutions. This makes it easier to substitute solution in the places it's needed

    Args:
        ODE (Eq, list, Matrix): one or multiple differential equations to be solved by sympy.
        ics (dict, optional): initial/boundary conditions for the differential equation.

    Returns:
        dict: a dictionary containing solutions to 'ODE'
    """

    # Common problem for people is making an single equation, but with both sides
    # being Matrices. This alleviates that issue, and lets users think less
    if (
        type(ODE) == Eq
        and isinstance(ODE.lhs, MatrixBase)
        and isinstance(ODE.rhs, MatrixBase)
    ):
        sol = sym_dsolve(ODE.lhs - ODE.rhs, ics=ics)
    else:
        sol = sym_dsolve(ODE, ics=ics)

    return {eq.lhs: eq.rhs for eq in sol}


def l2_norm(v: MatrixBase) -> (Expr):
    """Computes the l2-norm for a Matrix-class object, without using absolute values on entries, for easier simplification and integration

    Args:
        v (MatrixBase): A sympy Matrix

    Returns:
        Expr: The L2 norm of the matrix
    """
    return sqrt(sum(x**2 for x in v))


def display_equality(lhs: str | Expr, rhs: str | Expr):
    """Displays two sympy expressions or symbols separated by the equality symbol"
    Args:
        lhs: The left hand side of the equality.
        rhs: The right hand side of the equality.
    Returns:
        Nothing
    """
    if type(lhs) is str:
        lhs =  Symbol(lhs)
    if type(rhs) is str:
        rhs =  Symbol(rhs)
    display(Eq(lhs, rhs))


def display_definition(varname: str, rhs: Optional[Expr] = None):
    """Displays an expression stored in a python variable varname as "varname = expression ...."
    Args:
        varname: The name of the python variable to be displayed on the left hand side.
        rhs: An optional sympy Expr to be displayed on the right hand side instead of the actual variable definition.
    Raises:
        NameError: name 'varname' is not defined.
    Returns:
        Nothing
    """
    if rhs == None:
        caller_vars = inspect.currentframe().f_back.f_locals
        if varname not in caller_vars:
            raise NameError(f"name '{varname}' is not defined")
        rhs = caller_vars[varname]
    display_equality(varname, rhs)
