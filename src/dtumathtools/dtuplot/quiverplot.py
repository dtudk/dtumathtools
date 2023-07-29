from spb import MB, PB, BB
from spb.defaults import THREE_D_B, TWO_D_B
from spb.functions import _set_labels
from spb.series import VectorBase
from spb.utils import _instantiate_backend
from sympy import Matrix, latex, symbols
from sympy.external import import_module
from spb.backends.base_backend import Plot
from numpy import ndarray

np = import_module("numpy")


class ArrowSeries(VectorBase):
    """Represent a vector field."""

    is_vector = True
    is_slice = False
    is_streamlines = False
    _allowed_keys = []

    def __init__(self, start, direction, label=None, **kwargs):
        # Ranges must be given for VectorBase, even though they are None
        super().__init__(
            [start, direction], ranges=start.shape[-1] * [None], label=label, **kwargs
        )

        self.start = start
        self.direction = direction

        self._label = f"{start}->{direction}" if label is None else label
        self._latex_label = latex(f"{start}->{direction}") if label is None else label

        # Standard for 'use_cm' should be False
        self.use_cm = kwargs.get("use_cm", False)
        # Linked colormap using vector2d renderer
        self.use_quiver_solid_color = not self.use_cm

    def __str__(self):
        # Overwrite the VectorBase __str__ as it assumes things
        # about variables that does not hold for this class.
        return self._str_helper(
            f"Arrow Series with start point {self.start}, and direction {self.direction}"
        )

    def get_data(self):
        # This format works for both MB and PB
        # Has to translate to start/end and transpose
        # such that the x,y,z lims match the arrow
        # compensation for this in arrow done in 
        # quiverplot_helpers.
        start = np.array(self.start)
        end = start + np.array(self.direction)
        return np.array([start, end]).T# [np.array([v]) for v in list(self.start) + list(self.direction)]


# Specify 2D class such that this can be linked with renderer
class Arrow2DSeries(ArrowSeries):
    is_2Dvector = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Specify 3D class such that this can be linked with renderer
class Arrow3DSeries(ArrowSeries):
    is_3Dvector = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def quiver(*args, **kwargs):
    """Create a plot with a vector.

    Args:
        start (MatrixBase, np.ndarray, list, float): The starting coordinates (2D or 3D) of the vector. Can be given in multitude of ways/inputs.
        direction (MatrixBase, ndarray, list, float): The direction (2D or 3D) of the vector. Can be given in multitude of ways/inputs.
        rendering_kw (dict, optional): A dictionary forwarded to dtuplot.plot(), see SPB docs for reference.
        color (str, optional): A string to set the color of the vector with. With no argument color = 'blue'.
        show (bool, optional): Boolean, if 'True': show plot, other just return object without plotting. Defaults to 'True'.

    Returns:
        Plot: The vector plot.
    """
    # format if numbers are entered directly instead of lists
    num_single = 0
    args = list(args)
    for i in range(len(args)):
        if type(args[i]) in [int, float]:
            num_single += 1
        else:
            try:
                args[i] = float(args[i])
                num_single += 1
            except:
                break
    if num_single == 4:
        if len(args) > 4:
            args = [[args[0], args[1]], [args[2], args[3]], *args[4:]]
        else:
            args = [[args[0], args[1]], [args[2], args[3]]]
    elif num_single == 6:
        if len(args) > 6:
            args = [[args[0], args[1], args[2]], [args[3], args[4], args[5]], *args[6:]]
        else:
            args = [[args[0], args[1], args[2]], [args[3], args[4], args[5]]]
    elif num_single != 0:
        raise ValueError(f"Error! Wrong format used in quiver. Got {num_single} arguments that could be start or direction vector coordinates!")

    # split arguments into vectors and other arguments
    point_args = []
    otherargs = []
    for i in range(len(args)):
        if type(args[i]) in [list, np.ndarray, tuple, type(Matrix())]:
            newpoint = np.array(args[i]).flatten()
            point_args.append(newpoint)
        elif type(args[i]) == dict:
            kwargs.setdefault("rendering_kw", args[i])
        else:
            otherargs.append(args[i])
    assert (
        len(point_args) == 2
    ), f"Error! Start and direction vectors must be provided (only two vectors)!"

    try:
        point_args = np.array(point_args, dtype=float)
        assert point_args.shape[-1] in [
            2,
            3,
        ], "Error! Start and direction vectors must be 2D or 3D!"
        args = otherargs
    except:
        raise ValueError(f"Error! Wrong format used in quiver. Got {point_args[0]} as starting point(s) and {point_args[1]} as ending point(s)!")

    # want structure to be [list of starts, list of ends]
    # where list of starts could be [start1, start2, ...], either 2D or 3D points
    if len(point_args.shape) == 2:
        point_args = point_args[:, None, :]

    labels = kwargs.pop("label", [])
    if type(labels) == str:
        labels = [labels]
    assert type(labels) == list, f"Error! Label must be a list or a string!"
    assert len(labels) in [
        0,
        point_args.shape[1],
    ], f"Error! Number of labels must be equal to number of arrows, or empty list!"
    if labels == []:
        labels = [None] * point_args.shape[1]

    kwargs.setdefault("legend", True)
    # params are directly linked with interactive plots
    # if present, the BaseSeries will activate the 'is_interactive' flag
    params = kwargs.get("params", None)
    is_interactive = False if params is None else True
    if is_interactive:
        raise NotImplementedError("Interactive quiver plots are not yet implemented!")
        from spb.interactive import iplot

        kwargs["is_vector"] = True
        return iplot(*args, **kwargs)

    # rendering_kw needs to be passed to the plotting backend, but not
    # to the series. Thus pulled out here.
    rendering_kw = kwargs.pop("rendering_kw", None)
    # normalize argument needs to be passed to series object, but not to
    # backend. Otherwise warning will be raised. Thus pulled out here.
    normalize = kwargs.pop("normalize", False)

    # if 2D
    if point_args.shape[-1] == 2:
        Backend = kwargs.pop("backend", TWO_D_B)
        Series = Arrow2DSeries

        # Specific for matplotlib backend
        if Backend == MB:
            # Create if it does not exist
            if rendering_kw is None:
                rendering_kw = {}
            # Update values for length of vector to fit
            rendering_kw.setdefault("angles", "xy")
            rendering_kw.setdefault("scale_units", "xy")
            rendering_kw.setdefault("scale", 1)
        elif Backend == PB:
            if rendering_kw is None:
                rendering_kw = {}
            rendering_kw.setdefault("scale", 1)
            rendering_kw.setdefault("scaleratio", 1)
        elif Backend == BB:
            if rendering_kw is None:
                rendering_kw = {}
            mag = np.linalg.norm(point_args[-1].flatten(),2)
            rendering_kw.setdefault("scale", mag)
            rendering_kw.setdefault("pivot", "tail")
    else:
        Backend = kwargs.pop("backend", THREE_D_B)
        Series = Arrow3DSeries
        
        if Backend == PB:
            if rendering_kw is None:
                rendering_kw = {}
            rendering_kw.setdefault("sizeref", 1)
            rendering_kw.setdefault("sizemode", "scaled")

    series = [
        Series(start, stop,*otherargs, label=label, normalize=normalize, **kwargs)
        for start, stop, label in zip(point_args[0, :, :], point_args[1, :, :], labels)
    ]

    _set_labels(series, labels, rendering_kw)

    # if multiple arrows are given, plot them all in one plot
    show = kwargs.pop("show", True)
    B = _instantiate_backend(Backend, series[0], show=False, **kwargs)
    for i in range(1, len(series)):
        B.extend(_instantiate_backend(Backend, series[i], show=False, **kwargs))
    if show:
        B.show()
    return B
