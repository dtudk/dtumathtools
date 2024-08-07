from dtumathtools import *
from sympy import *
from spb import MB, PB, BB, KB, MAB
import pytest
import numpy as np
import re

# remove sympy variable named "test"
test = 0
del test

# Disable mayavi tests for github actions, as this fails
# Updating mayavi to 4.8.2 has solved many problems for windows and
# macos users, but requires additional packages for linux
# before pytest works. Reactivate if mayavi is to be better supported
# in the future...
test_mab = False


def test_quiver():
    # matplotlib
    dtuplot.quiver(
        Matrix([1, 2, 3]), Matrix([4, 5, 6]), {"color": "red"}, backend=MB, show=False
    )
    dtuplot.quiver([1, 2, 3], [4, 5, 6], backend=MB, show=False)
    dtuplot.quiver([1, 2], [4, 5], backend=MB, show=False)
    dtuplot.quiver(Matrix([1, 2]), Matrix([4, 5]), backend=MB, show=False)
    dtuplot.quiver(
        1, 2, 0, 0, 0, 3, rendering_kw={"color": "orange"}, backend=MB, show=False
    )
    dtuplot.quiver(1, 2, 1, 2, backend=MB, show=False)
    dtuplot.quiver((1, 2), (1, 2), backend=MB, show=False)
    dtuplot.quiver(np.array([1, 2]), (1, 2), backend=MB, show=False)
    dtuplot.quiver(np.array([1, 2]), np.array([1, 2]), backend=MB, show=False)
    dtuplot.quiver(np.array([1, 2]), Matrix([1, 2]), backend=MB, show=False)
    dtuplot.quiver(np.array([1, 2, 3]), (1, 2, 3), backend=MB, show=False)
    dtuplot.quiver(np.array([1, 2, 3]), np.array([1, 2, 3]), backend=MB, show=False)
    dtuplot.quiver(np.array([1, 2, 3]), Matrix([1, 2, 3]), backend=MB, show=False)
    dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label="123", backend=MB, show=False)
    dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label=["123"], backend=MB, show=False)
    dtuplot.quiver([1, 2, 3], [4, 5, 6], backend=MB, qlim=False, show=False)
    dtuplot.quiver([1, 2], [4, 5], backend=MB, qlim=False, show=False)
    # plotly
    dtuplot.quiver(Matrix([1, 2, 3]), Matrix([4, 5, 6]), show=False, backend=PB)
    dtuplot.quiver([1, 2, 3], [4, 5, 6], backend=PB, show=False)
    dtuplot.quiver([1, 2], [4, 5], backend=PB, show=False)
    dtuplot.quiver(Matrix([1, 2]), Matrix([4, 5]), backend=PB, show=False)
    dtuplot.quiver(1, 2, 0, 0, 0, 3, backend=PB, show=False)
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
    dtuplot.quiver([1, 2, 3], [4, 5, 6], backend=PB, qlim=False, show=False)
    dtuplot.quiver([1, 2], [4, 5], backend=PB, qlim=False, show=False)
    # bokeh
    dtuplot.quiver([1, 2], [4, 5], backend=BB, show=False)
    dtuplot.quiver(Matrix([1, 2]), Matrix([4, 5]), backend=BB, show=False)
    dtuplot.quiver(1, 2, 1, 2, backend=BB, show=False)
    dtuplot.quiver((1, 2), (1, 2), backend=BB, show=False)
    dtuplot.quiver(np.array([1, 2]), (1, 2), backend=BB, show=False)
    dtuplot.quiver(np.array([1, 2]), np.array([1, 2]), backend=BB, show=False)
    dtuplot.quiver(np.array([1, 2]), Matrix([1, 2]), backend=BB, show=False)
    dtuplot.quiver([1, 2], [4, 5], backend=BB, qlim=False, show=False)
    # k3d
    with pytest.warns(
        UserWarning, match="K3DBackend only works properly within Jupyter Notebook"
    ):
        dtuplot.quiver(Matrix([1, 2, 3]), Matrix([4, 5, 6]), backend=KB, show=False)
        dtuplot.quiver([1, 2, 3], [4, 5, 6], backend=KB, show=False)
        dtuplot.quiver(1, 2, 0, 0, 0, 3, backend=KB, show=False)
        dtuplot.quiver(np.array([1, 2, 3]), (1, 2, 3), backend=KB, show=False)
        dtuplot.quiver(np.array([1, 2, 3]), np.array([1, 2, 3]), backend=KB, show=False)
        dtuplot.quiver(np.array([1, 2, 3]), Matrix([1, 2, 3]), backend=KB, show=False)
        dtuplot.quiver(
            [1, 2, 3], Matrix([1, 2, 3]), label="123", backend=KB, show=False
        )
        dtuplot.quiver(
            [1, 2, 3], Matrix([1, 2, 3]), label=["123"], backend=KB, show=False
        )
        dtuplot.quiver([1, 2, 3], [4, 5, 6], backend=KB, qlim=False, show=False)
    # mayavi
    if test_mab:
        # A lot of things in the Mayavi toolbox is deprecated...
        with pytest.warns(DeprecationWarning):
            # # Options to hide screen popping up (commented out for github actions testing)
            # from mayavi import mlab  # used for the mayavi test to disable popups
            # mlab.options.offscreen = True
            dtuplot.quiver(
                Matrix([1, 2, 3]),
                Matrix([4, 5, 6]),
                backend=MAB,
                show=False,
                warning=False,
            )
            dtuplot.quiver([1, 2, 3], [4, 5, 6], backend=MAB, show=False, warning=False)
            dtuplot.quiver(1, 2, 0, 0, 0, 3, backend=MAB, show=False, warning=False)
            dtuplot.quiver(
                np.array([1, 2, 3]), (1, 2, 3), backend=MAB, show=False, warning=False
            )
            dtuplot.quiver(
                np.array([1, 2, 3]),
                np.array([1, 2, 3]),
                backend=MAB,
                show=False,
                warning=False,
            )
            dtuplot.quiver(
                np.array([1, 2, 3]),
                Matrix([1, 2, 3]),
                backend=MAB,
                show=False,
                warning=False,
            )
            dtuplot.quiver(
                [1, 2, 3],
                Matrix([1, 2, 3]),
                label="123",
                backend=MAB,
                show=False,
                warning=False,
            )
            dtuplot.quiver(
                [1, 2, 3],
                Matrix([1, 2, 3]),
                label=["123"],
                backend=MAB,
                show=False,
                warning=False,
            )
            dtuplot.quiver(
                [1, 2, 3], [4, 5, 6], backend=MAB, qlim=False, show=False, warning=False
            )

        with pytest.raises(
            NotImplementedError,
            match="Mayavi backend does not support 2D vector plots!",
        ):
            dtuplot.quiver([1, 2], [4, 5], backend=MAB, show=False, warning=False)

        with pytest.warns(
            UserWarning,
            match="Because of the Mayavi backend, the origin of the vector might be slightly off. To supress this warning, set 'warning=False'",
        ):
            dtuplot.quiver(
                Matrix([100, 100, 100]), Matrix([10, 20, 30]), backend=dtuplot.MAB
            )

    with pytest.raises(
        NotImplementedError, match="K3D backend does not support 2D vector plots!"
    ):
        dtuplot.quiver(Matrix([1, 2]), Matrix([0, 10]), backend=dtuplot.KB)

    with pytest.raises(
        NotImplementedError, match="Bokeh backend does not support 3D vector plots!"
    ):
        dtuplot.quiver(Matrix([1, 2, 3]), Matrix([0, 10, 100]), backend=dtuplot.BB)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Error! Wrong format used in quiver. Got [1. 2. 3. 4.] as starting point(s) and [4. 5. 6. 7.] as ending point(s)!"
        ),
    ):
        dtuplot.quiver(
            Matrix([1, 2, 3, 4]), Matrix([4, 5, 6, 7]), backend=MB, show=False
        )

    with pytest.raises(
        Exception,
        match="Error! Wrong format used in quiver. Got 7 arguments that could be start or direction vector coordinates!",
    ):
        dtuplot.quiver(1, 2, 3, 4, 5, 6, 7, backend=MB, show=False)

    with pytest.raises(
        Exception,
        match="Error! Wrong format used in quiver. Got 5 arguments that could be start or direction vector coordinates!",
    ):
        dtuplot.quiver(1, 2, 3, 4, 5, backend=MB, show=False)

    with pytest.raises(
        Exception,
        match="Error! Wrong format used in quiver. Got 3 arguments that could be start or direction vector coordinates!",
    ):
        dtuplot.quiver(1, 2, 3, backend=MB, show=False)

    with pytest.raises(
        AssertionError,
        match=re.escape(
            "Error! Start and direction vectors must be provided (only two vectors)!"
        ),
    ):
        dtuplot.quiver([1, 2], [3, 4], [5, 6], backend=MB, show=False)

    with pytest.raises(
        AssertionError,
        match=re.escape(
            "Error! Start and direction vectors must be provided (only two vectors)!"
        ),
    ):
        dtuplot.quiver([1, 2], backend=MB, show=False)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Error! Wrong format used in quiver. Got [1.] as starting point(s) and [2.] as ending point(s)!"
        ),
    ):
        dtuplot.quiver([1], [2], backend=MB, show=False)

    with pytest.raises(
        AssertionError,
        match="Error! Number of labels must be equal to number of arrows, or empty list!",
    ):
        dtuplot.quiver(
            [1, 2, 3], Matrix([1, 2, 3]), label=["123", "456"], backend=MB, show=False
        )

    with pytest.raises(
        AssertionError, match="Error! Label must be a list or a string!"
    ):
        dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), label=123, backend=MB, show=False)

    with pytest.raises(
        NotImplementedError, match="Interactive quiver plots are not yet implemented!"
    ):
        dtuplot.quiver([1, 2, 3], Matrix([1, 2, 3]), params=123, backend=MB, show=False)


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
        backend=MB,
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
            backend=MB,
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
            backend=MB,
        )


def test_scatterplot():
    # matplotlib
    dtuplot.scatter(1, 2, backend=MB, show=False)
    dtuplot.scatter(1, 2, 3, backend=MB, show=False)
    dtuplot.scatter([1], [2], backend=MB, show=False)
    dtuplot.scatter([[1]], [[2]], backend=MB, show=False)
    dtuplot.scatter([1, 2, 3], [4, 5, 6], backend=MB, show=False)
    dtuplot.scatter([1, 2, 3], [4, 5, 6], [7, 8, 9], backend=MB, show=False)
    dtuplot.scatter(
        np.array([1, 2, 3]),
        np.array([4, 5, 6]),
        np.array([7, 8, 9]),
        backend=MB,
        show=False,
    )
    dtuplot.scatter(np.array([1]), np.array([4]), np.array([7]), backend=MB, show=False)
    dtuplot.scatter(np.array([1, 2, 3]), np.array([4, 5, 6]), backend=MB, show=False)
    with pytest.warns(match="np.array with more than 1 dimension"):
        dtuplot.scatter(
            np.array([[1, 2, 3]]), np.array([[4, 5, 6]]), backend=MB, show=False
        )
    with pytest.warns(match="np.array with more than 1 dimension"):
        dtuplot.scatter(
            np.array([[1, 2, 3], [7, 8, 9]]),
            np.array([[4, 5, 6], [4, 5, 6]]),
            backend=MB,
            show=False,
        )
    dtuplot.scatter(np.array([1]), np.array([4]), backend=MB, show=False)
    dtuplot.scatter(Matrix([1, 2, 3]), Matrix([4, 5, 6]), backend=MB, show=False)
    dtuplot.scatter(Matrix([1, 2]), Matrix([4, 5]), backend=MB, show=False)

    dtuplot.scatter(Matrix([1, 2]).T, Matrix([4, 5]), backend=MB, show=False)
    dtuplot.scatter(np.array([1, 2]), Matrix([4, 5]), backend=MB, show=False)
    dtuplot.scatter(np.array([1, 2]), Matrix([4, 5]), [7, 8], backend=MB, show=False)
    dtuplot.scatter([1, 2], backend=MB, show=False)
    dtuplot.scatter((1, 2), backend=MB, show=False)
    dtuplot.scatter(Matrix([1, 2]), backend=MB, show=False)
    dtuplot.scatter([pi, 2 * pi], backend=MB, show=False)
    dtuplot.scatter(np.array([pi, 2 * pi]), backend=MB, show=False)
    dtuplot.scatter(Matrix([pi, 2 * pi]), backend=MB, show=False)
    dtuplot.scatter(Matrix([-1, 0, 1]), backend=MB, show=False)
    dtuplot.scatter(Matrix([0, 0, 0]), backend=MB, show=False)
    dtuplot.scatter(np.array([1, 2]), backend=MB, show=False)
    dtuplot.scatter([1, 2, 3], backend=MB, show=False)
    dtuplot.scatter((1, 2, 3), backend=MB, show=False)
    dtuplot.scatter(Matrix([1, 2, 3]), backend=MB, show=False)
    dtuplot.scatter(np.array([1, 2, 3]), backend=MB, show=False)
    dtuplot.scatter([[1, 2], [4, 5]], backend=MB, show=False)
    dtuplot.scatter([(1, 2), [4, 5]], backend=MB, show=False)
    dtuplot.scatter([Matrix([1, 2]), [4, 5]], backend=MB, show=False)
    dtuplot.scatter([Matrix([1, 2]), Matrix([4, 5])], backend=MB, show=False)
    dtuplot.scatter([np.array([1, 2]), [4, 5]], backend=MB, show=False)
    dtuplot.scatter([np.array([1, 2]), np.array([4, 5])], backend=MB, show=False)
    dtuplot.scatter(
        [Matrix([1, 2]), np.array([4, 5]), (7, 8), [3, 9]], backend=MB, show=False
    )
    dtuplot.scatter([[1, 2, 3], [4, 5, 6]], backend=MB, show=False)
    dtuplot.scatter([(1, 2, 3), [4, 5, 6]], backend=MB, show=False)
    dtuplot.scatter([Matrix([1, 2, 3]), [4, 5, 6]], backend=MB, show=False)
    dtuplot.scatter([Matrix([1, 2, 3]), Matrix([4, 5, 6])], backend=MB, show=False)
    dtuplot.scatter([np.array([1, 2, 3]), [4, 5, 6]], backend=MB, show=False)
    dtuplot.scatter([np.array([1, 2, 3]), np.array([4, 5, 6])], backend=MB, show=False)
    dtuplot.scatter(
        [Matrix([1, 2, 3]), [4, 5, 6], (7, 8, 9), np.array([-2, -1, 0])],
        backend=MB,
        show=False,
    )

    with pytest.raises(
        AssertionError, match="scatterplot only supports 2D and 3D plots"
    ):
        dtuplot.scatter(1, 2, 3, 4, backend=MB, show=False)
    with pytest.raises(
        AssertionError, match="scatterplot only supports 2D and 3D plots"
    ):
        dtuplot.scatter(1, backend=MB, show=False)
    # plotly
    dtuplot.scatter(1, 2, backend=PB, show=False)
    dtuplot.scatter(1, 2, 3, backend=PB, show=False)
    dtuplot.scatter([1], [2], backend=PB, show=False)
    dtuplot.scatter([[1]], [[2]], backend=PB, show=False)
    dtuplot.scatter([1, 2, 3], [4, 5, 6], backend=PB, show=False)
    dtuplot.scatter([1, 2, 3], [4, 5, 6], [7, 8, 9], backend=PB, show=False)
    dtuplot.scatter(
        np.array([1, 2, 3]),
        np.array([4, 5, 6]),
        np.array([7, 8, 9]),
        backend=PB,
        show=False,
    )
    dtuplot.scatter(np.array([1]), np.array([4]), np.array([7]), backend=PB, show=False)
    dtuplot.scatter(np.array([1, 2, 3]), np.array([4, 5, 6]), backend=PB, show=False)
    with pytest.warns(match="np.array with more than 1 dimension"):
        dtuplot.scatter(
            np.array([[1, 2, 3]]), np.array([[4, 5, 6]]), backend=PB, show=False
        )
    with pytest.warns(match="np.array with more than 1 dimension"):
        dtuplot.scatter(
            np.array([[1, 2, 3], [7, 8, 9]]),
            np.array([[4, 5, 6], [4, 5, 6]]),
            backend=PB,
            show=False,
        )
    dtuplot.scatter(np.array([1]), np.array([4]), backend=PB, show=False)
    dtuplot.scatter(
        Matrix([1, 2, 3]), Matrix([4, 5, 6]), backend=PB, show=False
    )  # different behavior to the np.array version
    dtuplot.scatter(Matrix([1, 2]), Matrix([4, 5]), backend=PB, show=False)
    with pytest.raises(
        AssertionError, match="scatterplot only supports 2D and 3D plots"
    ):
        dtuplot.scatter(1, 2, 3, 4, backend=PB, show=False)
    with pytest.raises(
        AssertionError, match="scatterplot only supports 2D and 3D plots"
    ):
        dtuplot.scatter(1, backend=PB, show=False)
    dtuplot.scatter(Matrix([1, 2]).T, Matrix([4, 5]), backend=PB, show=False)
    dtuplot.scatter(np.array([1, 2]), Matrix([4, 5]), backend=PB, show=False)
    dtuplot.scatter(np.array([1, 2]), Matrix([4, 5]), [7, 8], backend=PB, show=False)
    dtuplot.scatter([1, 2], backend=PB, show=False)
    dtuplot.scatter((1, 2), backend=PB, show=False)
    dtuplot.scatter(Matrix([1, 2]), backend=PB, show=False)
    dtuplot.scatter(Matrix([-1, 0, 1]), backend=PB, show=False)
    dtuplot.scatter(Matrix([0, 0, 0]), backend=PB, show=False)
    dtuplot.scatter(np.array([1, 2]), backend=PB, show=False)
    dtuplot.scatter([1, 2, 3], backend=PB, show=False)
    dtuplot.scatter((1, 2, 3), backend=PB, show=False)
    dtuplot.scatter(Matrix([1, 2, 3]), backend=PB, show=False)
    dtuplot.scatter(np.array([1, 2, 3]), backend=PB, show=False)
    dtuplot.scatter([[1, 2], [4, 5]], backend=PB, show=False)
    dtuplot.scatter([(1, 2), [4, 5]], backend=PB, show=False)
    dtuplot.scatter([Matrix([1, 2]), [4, 5]], backend=PB, show=False)
    dtuplot.scatter([Matrix([1, 2]), Matrix([4, 5])], backend=PB, show=False)
    dtuplot.scatter([np.array([1, 2]), [4, 5]], backend=PB, show=False)
    dtuplot.scatter([np.array([1, 2]), np.array([4, 5])], backend=PB, show=False)
    dtuplot.scatter(
        [Matrix([1, 2]), np.array([4, 5]), (7, 8), [3, 9]], backend=PB, show=False
    )
    dtuplot.scatter([[1, 2, 3], [4, 5, 6]], backend=PB, show=False)
    dtuplot.scatter([(1, 2, 3), [4, 5, 6]], backend=PB, show=False)
    dtuplot.scatter([Matrix([1, 2, 3]), [4, 5, 6]], backend=PB, show=False)
    dtuplot.scatter([Matrix([1, 2, 3]), Matrix([4, 5, 6])], backend=PB, show=False)
    dtuplot.scatter([np.array([1, 2, 3]), [4, 5, 6]], backend=PB, show=False)
    dtuplot.scatter([np.array([1, 2, 3]), np.array([4, 5, 6])], backend=PB, show=False)
    dtuplot.scatter(
        [Matrix([1, 2, 3]), [4, 5, 6], (7, 8, 9), np.array([-2, -1, 0])],
        backend=PB,
        show=False,
    )
    # bokeh
    dtuplot.scatter(1, 2, backend=BB, show=False)
    dtuplot.scatter([1], [2], backend=BB, show=False)
    dtuplot.scatter([[1]], [[2]], backend=BB, show=False)
    dtuplot.scatter([1, 2, 3], [4, 5, 6], backend=BB, show=False)
    dtuplot.scatter(np.array([1, 2, 3]), np.array([4, 5, 6]), backend=BB, show=False)
    dtuplot.scatter(np.array([1]), np.array([4]), backend=BB, show=False)
    dtuplot.scatter(Matrix([1, 2]), Matrix([4, 5]), backend=BB, show=False)
    dtuplot.scatter(Matrix([1, 2]).T, Matrix([4, 5]), backend=BB, show=False)
    dtuplot.scatter(np.array([1, 2]), Matrix([4, 5]), backend=BB, show=False)
    dtuplot.scatter(np.array([1, 2]), [7, 8], backend=BB, show=False)
    dtuplot.scatter([1, 2], backend=BB, show=False)
    dtuplot.scatter((1, 2), backend=BB, show=False)
    dtuplot.scatter(Matrix([1, 2]), backend=BB, show=False)
    dtuplot.scatter(Matrix([1.0, 2.0]), backend=BB, show=False)
    dtuplot.scatter(Matrix([-1, 0]), backend=BB, show=False)
    dtuplot.scatter(np.array([1, 2]), backend=BB, show=False)
    dtuplot.scatter([[1, 2], [4, 5]], backend=BB, show=False)
    dtuplot.scatter([(1, 2), [4, 5]], backend=BB, show=False)
    dtuplot.scatter([Matrix([1, 2]), [4, 5]], backend=BB, show=False)
    dtuplot.scatter([Matrix([1, 2]), Matrix([4, 5])], backend=BB, show=False)
    dtuplot.scatter([np.array([1, 2]), [4, 5]], backend=BB, show=False)
    dtuplot.scatter([np.array([1, 2]), np.array([4, 5])], backend=BB, show=False)
    dtuplot.scatter(
        [Matrix([1, 2]), np.array([4, 5]), (7, 8), [3, 9]], backend=BB, show=False
    )
    # k3d
    with pytest.warns(
        UserWarning, match="K3DBackend only works properly within Jupyter Notebook"
    ):
        dtuplot.scatter(1, 2, 3, backend=KB, show=False)
        dtuplot.scatter([1, 2, 3], [4, 5, 6], [7, 8, 9], backend=KB, show=False)
        dtuplot.scatter(
            np.array([1, 2, 3]),
            np.array([4, 5, 6]),
            np.array([7, 8, 9]),
            backend=KB,
            show=False,
        )
        dtuplot.scatter(
            np.array([1]), np.array([4]), np.array([7]), backend=KB, show=False
        )
        dtuplot.scatter(
            Matrix([1, 2, 3]).T,
            Matrix([4, 5, 6]),
            Matrix([[4], [5], [6]]),
            backend=KB,
            show=False,
        )
        dtuplot.scatter(
            np.array([1, 2, 3]), Matrix([4, 5, 6]), [7, 8, 9], backend=KB, show=False
        )
        dtuplot.scatter(Matrix([-1, 0, 1]), backend=KB, show=False)
        dtuplot.scatter(Matrix([0, 0, 0]), backend=KB, show=False)
        dtuplot.scatter([1, 2, 3], backend=KB, show=False)
        dtuplot.scatter((1, 2, 3), backend=KB, show=False)
        dtuplot.scatter(Matrix([1, 2, 3]), backend=KB, show=False)
        dtuplot.scatter(np.array([1, 2, 3]), backend=KB, show=False)
        dtuplot.scatter([[1, 2, 3], [4, 5, 6]], backend=KB, show=False)
        dtuplot.scatter([(1, 2, 3), [4, 5, 6]], backend=KB, show=False)
        dtuplot.scatter([Matrix([1, 2, 3]), [4, 5, 6]], backend=KB, show=False)
        dtuplot.scatter([Matrix([1, 2, 3]), Matrix([4, 5, 6])], backend=KB, show=False)
        dtuplot.scatter([np.array([1, 2, 3]), [4, 5, 6]], backend=KB, show=False)
        dtuplot.scatter(
            [np.array([1, 2, 3]), np.array([4, 5, 6])], backend=KB, show=False
        )
        dtuplot.scatter(
            [Matrix([1, 2, 3]), [4, 5, 6], (7, 8, 9), np.array([-2, -1, 0])],
            backend=KB,
            show=False,
        )
    # mayavi
    if test_mab:
        with pytest.warns(DeprecationWarning):
            dtuplot.scatter(1, 2, 3, backend=MAB, show=False)
            dtuplot.scatter([1, 2, 3], [4, 5, 6], [7, 8, 9], backend=MAB, show=False)
            dtuplot.scatter(
                np.array([1, 2, 3]),
                np.array([4, 5, 6]),
                np.array([7, 8, 9]),
                backend=MAB,
                show=False,
            )
            dtuplot.scatter(
                np.array([1]), np.array([4]), np.array([7]), backend=MAB, show=False
            )
            dtuplot.scatter(
                Matrix([1, 2, 3]).T,
                Matrix([4, 5, 6]),
                Matrix([[4], [5], [6]]),
                backend=MAB,
                show=False,
            )
            dtuplot.scatter(
                np.array([1, 2, 3]),
                Matrix([4, 5, 6]),
                [7, 8, 9],
                backend=MAB,
                show=False,
            )
            dtuplot.scatter(Matrix([-1, 0, 1]), backend=MAB, show=False)
            dtuplot.scatter(Matrix([0, 0, 0]), backend=MAB, show=False)
            dtuplot.scatter([1, 2, 3], backend=MAB, show=False)
            dtuplot.scatter((1, 2, 3), backend=MAB, show=False)
            dtuplot.scatter(Matrix([1, 2, 3]), backend=MAB, show=False)
            dtuplot.scatter(np.array([1, 2, 3]), backend=MAB, show=False)
            dtuplot.scatter([[1, 2, 3], [4, 5, 6]], backend=MAB, show=False)
            dtuplot.scatter([(1, 2, 3), [4, 5, 6]], backend=MAB, show=False)
            dtuplot.scatter([Matrix([1, 2, 3]), [4, 5, 6]], backend=MAB, show=False)
            dtuplot.scatter(
                [Matrix([1, 2, 3]), Matrix([4, 5, 6])], backend=MAB, show=False
            )
            dtuplot.scatter([np.array([1, 2, 3]), [4, 5, 6]], backend=MAB, show=False)
            dtuplot.scatter(
                [np.array([1, 2, 3]), np.array([4, 5, 6])], backend=MAB, show=False
            )
            dtuplot.scatter(
                [Matrix([1, 2, 3]), [4, 5, 6], (7, 8, 9), np.array([-2, -1, 0])],
                backend=MAB,
                show=False,
            )

    # testing arguments
    dtuplot.scatter(
        1,
        2,
        3,
        rendering_kw={"alpha": 1, "s": 100, "color": "black"},
        backend=MB,
        show=False,
    )
    dtuplot.scatter(
        1, -1, rendering_kw={"color": "black", "s": 10}, backend=MB, show=False
    )
    dtuplot.scatter(
        1,
        2,
        rendering_kw={"markersize": 10, "color": "r"},
        xlim=[-2, 2],
        ylim=[-2, 2],
        backend=MB,
        show=False,
    )

    # test assertions
    if test_mab:
        with pytest.raises(
            NotImplementedError, match="Mayavi does not support 2D scatter plots!"
        ):
            dtuplot.scatter([1, 2, 3], [4, 5, 6], backend=MAB, show=False)
    with pytest.raises(
        NotImplementedError, match="K3D does not support 2D scatter plots!"
    ):
        dtuplot.scatter([1, 2, 3], [4, 5, 6], backend=KB, show=False)
    with pytest.raises(
        NotImplementedError, match="Bokeh does not support 3D scatter plots!"
    ):
        dtuplot.scatter([1, 2, 3], [4, 5, 6], [7, 8, 9], backend=BB, show=False)

    with pytest.warns(match="non-Expr objects in a Matrix is deprecated."):
        item = Matrix([[[1, 2]]])
    with pytest.raises(
        AssertionError, match="scatterplot only supports 2D and 3D plots"
    ):
        dtuplot.scatter(item, item, item, item, backend=MB, show=False)

    with pytest.raises(ValueError, match="Unknown input found"):
        dtuplot.scatter(
            NotImplementedError,
            NotImplementedError,
            NotImplementedError,
            backend=dtuplot.MB,
            show=False,
        )

    with pytest.raises(
        AssertionError,
        match=re.escape("Points given (single or list of) must be 2D or 3D!"),
    ):
        dtuplot.scatter(np.array([1, 2, 3, 4]), backend=dtuplot.MB, show=False)

    with pytest.raises(ValueError, match="Invalid type of coordinate/point"):
        dtuplot.scatter([dtuplot], backend=dtuplot.MB, show=False)

    with pytest.raises(AssertionError, match="Invalid type of coordinate, recieved"):
        dtuplot.scatter([[dtuplot]], backend=dtuplot.MB, show=False)

    with pytest.raises(
        AssertionError, match="Length of all points in list must match!"
    ):
        dtuplot.scatter([[1, 2, 3], [1, 2]], backend=dtuplot.MB, show=False)


if __name__ == "__main__":
    test_quiver()
