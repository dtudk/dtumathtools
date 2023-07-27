from dtumathtools import *
from sympy import *
from spb import MB

# remove sympy variable named "test"
test = 0
del test


def test_boundary():
    x,y,u,v = symbols("x y u v")
    param_func = Matrix([
        u, (1-abs(u))**2*v #*u/abs(u)
    ])
    ulim = (u,-1.5,1.5)
    vlim = (v,0.5,1)

    p0 = dtuplot.plot_boundary(
        param_func,
        ulim,
        vlim,
        rendering_kw={
            "color":"red",
            "linewidth":5
        },
        xlabel="some",
        ylabel="thing",
        zlabel="here",
        show=False,
    )

    assert type(p0) == MB
    assert p0._series[0].is_point == False
    assert p0._series[0].is_polar == False
    assert p0._series[0].is_filled == True
    assert p0._series[0].only_integers == False
    assert p0._series[0].show_in_legend == True
    assert p0._series[0].adaptive == False
    assert p0._series[0]._scales == ["linear", "linear", "linear"]
    assert p0._series[0]._label == "v"
    assert p0._series[0].expr_x == -1.5
    assert p0._series[0].expr_y == 0.25*v
    assert p0._series[0].var == v
    assert p0._series[0].start == 0.5
    assert p0._series[0].end == 1.0
