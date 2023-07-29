from dtumathtools import *
from sympy import *
from spb import MB, PB, BB
import pytest
import numpy as np
import re

# remove sympy variable named "test"
test = 0
del test


def test_quiver():
    # matplotlib
    dtuplot.quiver(Matrix([1, 2, 3]), Matrix([4, 5, 6]), {"color": "red"}, show=False)
    dtuplot.quiver([1, 2, 3], [4, 5, 6], show=False)
    dtuplot.quiver([1, 2], [4, 5], show=False)
    dtuplot.quiver(Matrix([1, 2]), Matrix([4, 5]), show=False)
    dtuplot.quiver(1, 2, 0, 0, 0, 3, rendering_kw={"color": "orange"}, show=False)
    dtuplot.quiver(1, 2, 1, 2, show=False)
    dtuplot.quiver((1, 2), (1, 2), show=False)
    dtuplot.quiver(np.array([1, 2]), (1, 2), show=False)
    dtuplot.quiver(np.array([1, 2]), np.array([1, 2]), show=False)
    dtuplot.quiver(np.array([1, 2]), Matrix([1, 2]), show=False)
    dtuplot.quiver(np.array([1, 2, 3]), (1, 2, 3), show=False)
    dtuplot.quiver(np.array([1, 2, 3]), np.array([1, 2, 3]), show=False)
    dtuplot.quiver(np.array([1, 2, 3]), Matrix([1, 2, 3]), show=False)
    dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label="123", show=False)
    dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label=["123"], show=False)
    # plotly
    dtuplot.quiver(
        Matrix([1, 2, 3]), Matrix([4, 5, 6]), show=False, backend=PB
    )
    dtuplot.quiver([1, 2, 3], [4, 5, 6], backend=PB, show=False)
    dtuplot.quiver([1, 2], [4, 5], backend=PB, show=False)
    dtuplot.quiver(Matrix([1, 2]), Matrix([4, 5]), backend=PB, show=False)
    dtuplot.quiver(
        1, 2, 0, 0, 0, 3, backend=PB, show=False
    )
    dtuplot.quiver(1, 2, 1, 2, backend=PB, show=False)
    dtuplot.quiver((1, 2), (1, 2), backend=PB, show=False)
    dtuplot.quiver(np.array([1, 2]), (1, 2), backend=PB, show=False)
    dtuplot.quiver(np.array([1, 2]), np.array([1, 2]), backend=PB, show=False)
    dtuplot.quiver(np.array([1, 2]), Matrix([1, 2]), backend=PB, show=False)
    dtuplot.quiver(np.array([1, 2, 3]), (1, 2, 3), backend=PB, show=False)
    dtuplot.quiver(np.array([1, 2, 3]), np.array([1, 2, 3]), backend=PB, show=False)
    dtuplot.quiver(np.array([1, 2, 3]), Matrix([1, 2, 3]), backend=PB, show=False)
    dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label="123", backend=PB, show=False)
    dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label=["123"], backend=PB, show=False)
    # bokeh
    dtuplot.quiver([1, 2], [4, 5], backend=BB, show=False)
    dtuplot.quiver(Matrix([1, 2]), Matrix([4, 5]), backend=BB, show=False)
    dtuplot.quiver(1, 2, 1, 2, backend=BB, show=False)
    dtuplot.quiver((1, 2), (1, 2), backend=BB, show=False)
    dtuplot.quiver(np.array([1, 2]), (1, 2), backend=BB, show=False)
    dtuplot.quiver(np.array([1, 2]), np.array([1, 2]), backend=BB, show=False)
    dtuplot.quiver(np.array([1, 2]), Matrix([1, 2]), backend=BB, show=False)
    
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Error! Wrong format used in quiver. Got [1. 2. 3. 4.] as starting point(s) and [4. 5. 6. 7.] as ending point(s)!"
        ),
    ):
        dtuplot.quiver(Matrix([1, 2, 3, 4]), Matrix([4, 5, 6, 7]), show=False)

    with pytest.raises(
        Exception,
        match="Error! Wrong format used in quiver. Got 7 arguments that could be start or direction vector coordinates!",
    ):
        dtuplot.quiver(1, 2, 3, 4, 5, 6, 7, show=False)

    with pytest.raises(
        Exception,
        match="Error! Wrong format used in quiver. Got 5 arguments that could be start or direction vector coordinates!",
    ):
        dtuplot.quiver(1, 2, 3, 4, 5, show=False)

    with pytest.raises(
        Exception,
        match="Error! Wrong format used in quiver. Got 3 arguments that could be start or direction vector coordinates!",
    ):
        dtuplot.quiver(1, 2, 3, show=False)

    with pytest.raises(
        AssertionError,
        match=re.escape(
            "Error! Start and direction vectors must be provided (only two vectors)!"
        ),
    ):
        dtuplot.quiver([1, 2], [3, 4], [5, 6], show=False)

    with pytest.raises(
        AssertionError,
        match=re.escape(
            "Error! Start and direction vectors must be provided (only two vectors)!"
        ),
    ):
        dtuplot.quiver([1, 2], show=False)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Error! Wrong format used in quiver. Got [1.] as starting point(s) and [2.] as ending point(s)!"
        ),
    ):
        dtuplot.quiver([1], [2], show=False)

    with pytest.raises(
        AssertionError,
        match="Error! Number of labels must be equal to number of arrows, or empty list!",
    ):
        dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label=["123", "456"], show=False)

    with pytest.raises(
        AssertionError, match="Error! Label must be a list or a string!"
    ):
        dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label=123, show=False)

    with pytest.raises(
        NotImplementedError, match="Interactive quiver plots are not yet implemented!"
    ):
        dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), params=123, show=False)


def test_boundary():
    x, y, u, v = symbols("x y u v")
    param_func = Matrix([u, (1 - abs(u)) ** 2 * v])
    ulim = (u, -1.5, 1.5)
    vlim = (v, 0.5, 1)

    p0 = dtuplot.plot_boundary(
        param_func,
        ulim,
        vlim,
        rendering_kw={"color": "red", "linewidth": 5},
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
    assert p0._series[0].expr_y == 0.25 * v
    assert p0._series[0].var == v
    assert p0._series[0].start == 0.5
    assert p0._series[0].end == 1.0

    # testing errors
    with pytest.raises(
        ValueError, match="For 2D-areas two variables are needed to plot boundary"
    ):
        w = symbols("w)")
        wlim = (w, -1, 1)
        p0 = dtuplot.plot_boundary(
            param_func,
            ulim,
            vlim,
            wlim,
            rendering_kw={"color": "red", "linewidth": 5},
            xlabel="some",
            ylabel="thing",
            zlabel="here",
            show=False,
        )

    with pytest.raises(
        NotImplementedError, match="Volume boundary plots are not yet implemented"
    ):
        param_func = Matrix([u, (1 - abs(u)) ** 2 * v, v])  # *u/abs(u)

        p0 = dtuplot.plot_boundary(
            param_func,
            ulim,
            vlim,
            rendering_kw={"color": "red", "linewidth": 5},
            xlabel="some",
            ylabel="thing",
            zlabel="here",
            show=False,
        )


def test_scatterplot():
    dtuplot.scatter(1, 2, show=False)
    dtuplot.scatter(1, 2, 3, show=False)
    dtuplot.scatter([1], [2], show=False)
    dtuplot.scatter([[1]], [[2]], show=False)
    dtuplot.scatter([1, 2, 3], [4, 5, 6], show=False)
    dtuplot.scatter([1, 2, 3], [4, 5, 6], [7, 8, 9], show=False)
    dtuplot.scatter(
        np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9]), show=False
    )
    dtuplot.scatter(np.array([1]), np.array([4]), np.array([7]), show=False)
    dtuplot.scatter(np.array([1, 2, 3]), np.array([4, 5, 6]), show=False)
    with pytest.warns(match="np.array with more than 1 dimension"):
        dtuplot.scatter(np.array([[1, 2, 3]]), np.array([[4, 5, 6]]), show=False)
    with pytest.warns(match="np.array with more than 1 dimension"):
        dtuplot.scatter(
            np.array([[1, 2, 3], [7, 8, 9]]),
            np.array([[4, 5, 6], [4, 5, 6]]),
            show=False,
        )
    dtuplot.scatter(np.array([1]), np.array([4]), show=False)
    dtuplot.scatter(
        Matrix([1, 2, 3]), Matrix([4, 5, 6]), show=False
    )  # different behavior to the np.array version
    dtuplot.scatter(Matrix([1, 2]), Matrix([4, 5]), show=False)
    with pytest.raises(
        AssertionError, match="scatterplot only supports 2D and 3D plots"
    ):
        dtuplot.scatter(1, 2, 3, 4, show=False)
    with pytest.raises(
        AssertionError, match="scatterplot only supports 2D and 3D plots"
    ):
        dtuplot.scatter(1, show=False)

    # testing arguments
    dtuplot.scatter(
        1, 2, 3, rendering_kw={"alpha": 1, "s": 100, "color": "black"}, show=False
    )
    dtuplot.scatter(1, -1, rendering_kw={"color": "black", "s": 10}, show=False)
    dtuplot.scatter(
        1,
        2,
        rendering_kw={"markersize": 10, "color": "r"},
        xlim=[-2, 2],
        ylim=[-2, 2],
        show=False,
    )

    # test assertions
    with pytest.raises(
        AssertionError, match="Cannot mix matrix and non-matrix arguments!"
    ):
        dtuplot.scatter(Matrix([1, 2]), [3, 4], show=False)

    with pytest.raises(
        AssertionError,
        match="Matrix must not have multiple dimensions different from size 1!",
    ):
        dtuplot.scatter(Matrix([[1, 2, 3], [1, 2, 3]]), Matrix([[1, 2, 3]]), show=False)

    with pytest.raises(AssertionError, match="All matrices must have the same shape!"):
        dtuplot.scatter(
            Matrix([1, 2]),
            Matrix([[1, 2], [2, 3]]),
            Matrix([[1, 2], [2, 3]]),
            show=False,
        )

    with pytest.warns(match="non-Expr objects in a Matrix is deprecated."):
        item = Matrix([[[1, 2]]])
    with pytest.raises(
        AssertionError, match="scatterplot only supports 2D and 3D plots"
    ):
        dtuplot.scatter(item, item, item, item, show=False)
