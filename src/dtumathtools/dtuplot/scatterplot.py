from sympy import MatrixBase, Expr, Basic, MutableMatrix, ImmutableMatrix
from sympy.external import import_module
from spb.functions import plot_list, plot3d_list
from spb.backends.base_backend import Plot
import numpy as np
from spb import MB, PB, BB, KB, MAB
from spb.defaults import THREE_D_B, TWO_D_B


def scatter(*args, **kwargs):
    """Create a plot with one/multiple point(s). Similar to plt.scatter.

    Args:
        points (MatrixBase, np.ndarray, list, float): The point(s) to scatter. Format is 'x, y, [z], **kwargs' with x,y,[z] being Matrix, list, float or np.ndarray. If a single Matrix, list or np.ndarray is given, each entry will be treated as seperate a point.
        rendering_kw (dict, optional): A dictionary forwarded to dtuplot.plot(), see SPB docs for reference.
        color (str, optional): A string to set the color of the points with. With no argument color = 'blue'.
        show (bool, optional): Boolean, if 'True': show plot, other just return object without plotting. Defaults to 'True'.

    Returns:
        Plot: The plot containing the points.
    """

    np = import_module("numpy")
    warnings = import_module("warnings")

    def warning_formatter(msg, *args, line=None, **kwargs):
        return str(msg)

    warnings.formatwarning = warning_formatter

    # format all arguments
    dim = 0
    args = list(args)
    if len(args) == 1 and type(args[0]) in [
        list,
        tuple,
        MutableMatrix,
        ImmutableMatrix,
        np.ndarray,
    ]:
        # Single list/tuple/matrix/array given, assume this is list of (single) point(s)
        coords = [[], [], []]
        dim = None
        for i, arg in enumerate(args[0]):
            if (
                type(arg) in [float, int, Expr]
                or np.issubdtype(type(arg), np.integer)
                or np.issubdtype(type(arg), np.floating)
                or isinstance(arg, Basic)
            ):
                # the single arg is a single point
                dim = len(args[0])
                coords[i].append(float(arg))
            elif type(arg) in [list, tuple, MutableMatrix, ImmutableMatrix, np.ndarray]:
                # Unify format
                arg = np.array(arg).flatten()
                # Check dimension
                if dim is None:
                    dim = len(arg)
                else:
                    assert len(arg) == dim, "Length of all points in list must match!"
                # Sort the coordinates into correct bins
                for o, coord in enumerate(arg):
                    assert (
                        type(coord) in [float, int, Expr]
                        or np.issubdtype(type(coord), np.integer)
                        or np.issubdtype(type(coord), np.floating)
                        or isinstance(coord, Basic)
                    ), f"Invalid type of coordinate, recieved {coord} with type {str(type(coord))}"
                    coords[o].append(float(coord))
            else:
                raise ValueError(
                    f"Invalid type of coordinate/point, recieved {arg} with type {str(type(arg))}, but must be one of [list, tuple, Matrix, np.ndarray, int, float, Expr]!"
                )
            assert dim in [2, 3], "Points given (single or list of) must be 2D or 3D!"

        if len(coords[-1]) == 0:
            assert dim == 2, "Unspecified error!"
            del coords[-1]

        args = coords
    else:
        # Probably a list of arguments given!
        for i in range(len(args)):
            if type(args[i]) in (list, tuple, MutableMatrix, ImmutableMatrix):
                # This is x, y, or z argument. List of these coordinates for each point.
                args[i] = np.array(args[i]).flatten()
                dim += 1
            elif type(args[i]) == np.ndarray:
                if len(args[i].shape) > 1:
                    warnings.warn(
                        f"np.array with more than 1 dimension ({len(args[i].shape)} dimensions was found) has been flattened!"
                    )
                args[i] = args[i].flatten()
                dim += 1
            elif type(args[i]) in [float, int]:
                # Single entries for x,y,z given.
                args[i] = np.array([args[i]])
                dim += 1
            else:
                try:
                    # symbolic expression not multiplied fully
                    args[i] = np.array([float(args[i])])
                    dim += 1
                except:
                    raise ValueError(f"Unknown input found: {args[i]}")

    assert dim in [
        2,
        3,
    ], f"scatterplot only supports 2D and 3D plots, but arguments for dimension {dim} was given."
    if dim == 2:
        Backend = kwargs.pop("backend", TWO_D_B)
        if Backend == KB:
            raise NotImplementedError("K3D does not support 2D scatter plots!")
        elif Backend == MAB:
            raise NotImplementedError("Mayavi does not support 2D scatter plots!")
        rendering_kw = kwargs.pop("rendering_kw", {})
        markersize = rendering_kw.pop("s", None)
        if markersize is not None:
            rendering_kw.setdefault("markersize", markersize)
        return plot_list(
            *args, is_point=True, rendering_kw=rendering_kw, backend=Backend, **kwargs
        )
    else:
        Backend = kwargs.pop("backend", THREE_D_B)
        if Backend == BB:
            raise NotImplementedError("Bokeh does not support 3D scatter plots!")
        return plot3d_list(*args, is_point=True, backend=Backend, **kwargs)


# Adjust renderer for Mayavi to support 3D scatter plotting
from spb.backends.mayavi.renderers.line3d import (
    _draw_line3d_helper,
    _update_line3d_helper,
)
from spb.backends.base_renderer import Renderer


def MAB_draw_line3d_helper(renderer, data):
    x, y, z = data
    u = np.ones_like(x)
    return _draw_line3d_helper(renderer, (x, y, z, u))


class Point3DRenderer(Renderer):
    draw_update_map = {MAB_draw_line3d_helper: _update_line3d_helper}
