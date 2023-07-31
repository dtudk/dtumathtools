import pytest
from sympy import *

from dtumathtools import *

# remove sympy variable named "test"
test = 0
del test


def test_taylor():
    x, y = symbols("x y")
    f = x**3 - 3 * x**2 + y**3 - 3 * y**2

    assert dtutools.taylor(f, [x, 0, y, 0], 3) == -3 * x**2 - 3 * y**2
    assert dtutools.taylor(f, [x, 0, y, 2], 3) == -3 * x**2 + 3 * (y - 2) ** 2 - 4
    assert dtutools.taylor(f, [x, 2, y, 0], 3) == -3 * y**2 + 3 * (x - 2) ** 2 - 4


def test_gradient():
    x, y, z = symbols("x y z")
    f = x**2 * sin(y) * z

    assert dtutools.gradient(f) == Matrix(
        [2 * x * z * sin(y), x**2 * z * cos(y), x**2 * sin(y)]
    )
    assert dtutools.gradient(f, [x, z]) == Matrix([2 * x * z * sin(y), x**2 * sin(y)])


def test_div():
    x, y, z = symbols("x y z")
    V = Matrix([x * y * sin(z), x * ln(y), -x * y * z**3])

    assert dtutools.div(V, var=[x, y, z]) == -3 * x * y * z**2 + x / y + y * sin(z)

    u, v, w = symbols("u v w")
    V2 = Matrix([u, w**2, u * sin(w)])

    assert dtutools.div(V2, var=[u, v, w]) == u * cos(w) + 1


# @pytest.mark.filterwarnings("ignore")
def test_warnings():
    x, y, z = symbols("x y z")
    V = Matrix([x * y * sin(z), x * ln(y), -x * y * z**3])

    u, v, w = symbols("u v w")
    V2 = Matrix([u, w**2, u * sin(w)])

    with pytest.warns(
        UserWarning, match="Warning! Variables were not specified."
    ):  #'Warning! Variables were not specified.'
        # Trigger a warning.
        dtutools.div(V)
        dtutools.div(V2)
        dtutools.rot(V)
        dtutools.rot(V2)


def test_errors():
    x, y, z = symbols("x y z")
    u, v, w = symbols("u v w")
    a, b, c = symbols("a b c")

    V = Matrix([x * y * sin(z), x * ln(y), -x * y * z**3])
    V2 = Matrix([u, w**2, u * sin(w)])
    V3 = Matrix([u * x, sin(y), (u - y) * x])
    V4 = Matrix([1, a * c, sin(b)])
    V5 = Matrix([x * y * sin(c), x * ln(y), -x * y * c**3])

    with pytest.raises(
        AssertionError, match="ERROR! Could not guess the variables used."
    ):
        # raise errors
        dtutools.div(V3)
        dtutools.div(V4)
        dtutools.div(V5)
        dtutools.rot(V3)
        dtutools.rot(V4)
        dtutools.rot(V5)

    with pytest.raises(AssertionError, match="Exactly 3 variables must be specified!"):
        dtutools.div(V, var=[])
        dtutools.div(V, var=[x])
        dtutools.div(V, var=[x, y, z, u, v, w])
        dtutools.div(V, var=[x, y, z, u])
        dtutools.div(V2, var=[u, w])
        dtutools.rot(V, var=[])
        dtutools.rot(V, var=[x])
        dtutools.rot(V, var=[x, y, z, u, v, w])
        dtutools.rot(V, var=[x, y, z, u])
        dtutools.rot(V2, var=[u, w])


def test_rot():
    x, y, z = symbols("x y z")
    V = Matrix([x * y * sin(z), x * ln(y), -x * y * z**3])

    assert dtutools.rot(V, var=[x, y, z]) == Matrix(
        [-x * z**3, x * y * cos(z) + y * z**3, -x * sin(z) + log(y)]
    )

    u, v, w = symbols("u v w")
    V2 = Matrix([u, w**2, u * sin(w)])

    assert dtutools.rot(V2, var=[u, v, w]) == Matrix([-2 * w, -sin(w), 0])


def test_hessian():
    x, y, z = symbols("x y z")
    f = x**4 + 4 * x**2 * y**2 + y**4 - 4 * x**3 - 4 * y**3 + 2

    assert dtutools.hessian(f) == Matrix(
        [
            [12 * x**2 - 24 * x + 8 * y**2, 16 * x * y],
            [16 * x * y, 8 * x**2 + 12 * y**2 - 24 * y],
        ]
    )
