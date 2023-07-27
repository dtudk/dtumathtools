from sympy import latex, Matrix
from sympy.external import import_module
from spb.defaults import TWO_D_B, THREE_D_B
from spb.functions import _set_labels
from spb.series import BaseSeries
from spb.utils import _instantiate_backend


class ArrowSeries(BaseSeries):
    """Represent a vector field."""

    is_vector = True
    is_slice = False
    is_streamlines = False
    _allowed_keys = []

    def __init__(self, start, direction, label=None, **kwargs):

        self.start = start
        self.direction = direction

        self._label = f"{start}->{direction}" if label is None else label
        self._latex_label = latex(f"{start}->{direction}") if label is None else label

        self.expr = kwargs.get("expr", "")
        self.use_cm = kwargs.get("use_cm", False)
        self.color_func = kwargs.get("color_func", None)
        # NOTE: normalization is achieved at the backend side: this allows to
        # obtain same length arrows, but colored with the actual magnitude.
        # If normalization is applied on the series get_data(), the coloring
        # by magnitude would not be applicable at the backend.
        self.normalize = kwargs.get("normalize", False)

        self.rendering_kw = kwargs.get("quiver_kw", kwargs.get("rendering_kw", dict()))

        self._set_use_quiver_solid_color(**kwargs)
        self._init_transforms(**kwargs)

    def _set_use_quiver_solid_color(self, **kwargs):
        # NOTE: this attribute will inform the backend wheter to use a
        # color map or a solid color for the quivers. It is placed here
        # because it simplifies the backend logic when dealing with
        # plot sums.
        self.use_quiver_solid_color = (
            True
            if ("scalar" not in kwargs.keys())
            else (
                False if (not kwargs["scalar"]) or (kwargs["scalar"] is None) else True
            )
        )

    def get_data(self):

        return *self.start, *self.direction


def quiver(*args, **kwargs):

    np = import_module("numpy")

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
        raise f"Error! Wrong format used in quiver. Got {num_single} arguments \
            that could be start or direction vector coordinates!"

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
        raise f"Error! Wrong format used in quiver. \
        Got {point_args[0]} as starting point(s) and {point_args[1]} as ending point(s)!"

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
    params = kwargs.get("params", None)
    is_interactive = False if params is None else True
    kwargs["is_interactive"] = is_interactive
    if is_interactive:
        raise NotImplementedError("Interactive quiver plots are not yet implemented!")
        from spb.interactive import iplot

        kwargs["is_vector"] = True
        return iplot(*args, **kwargs)

    series = [
        ArrowSeries(start, stop, *otherargs, label=label, **kwargs)
        for start, stop, label in zip(point_args[0, :, :], point_args[1, :, :], labels)
    ]

    rendering_kw = kwargs.pop("rendering_kw", None)

    # if 2D
    if point_args.shape[-1] == 2:
        Backend = kwargs.pop("backend", TWO_D_B)
        for i in range(len(series)):
            series[i].rendering_kw["angles"] = "xy"
            series[i].rendering_kw["scale_units"] = "xy"
            series[i].rendering_kw["scale"] = 1
            series[i].is_2Dvector = True
    else:
        Backend = kwargs.pop("backend", THREE_D_B)
        for i in range(len(series)):
            series[i].is_3Dvector = True

    _set_labels(series, labels, rendering_kw)

    # if multiple arrows are given, plot them all in one plot
    show = kwargs.pop("show", True)
    B = _instantiate_backend(Backend, series[0], show=False, **kwargs)
    for i in range(1, len(series)):
        B.extend(_instantiate_backend(Backend, series[i], show=False, **kwargs))
    if show:
        B.show()
    return B
