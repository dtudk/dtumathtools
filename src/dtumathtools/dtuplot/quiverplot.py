from sympy import latex
from sympy.external import import_module
from spb.backends.base_backend import Plot as BP
from spb.defaults import TWO_D_B, THREE_D_B, cfg
from spb.functions import _set_labels
from spb.series import BaseSeries
from spb.utils import (
    _plot_sympify,
    _unpack_args_extended,
    _split_vector,
    _is_range,
    _instantiate_backend,
)


class ArrowSeries(BaseSeries):
    """Represent a vector field."""

    is_vector = True
    is_slice = False
    is_streamlines = False
    _allowed_keys = []

    def __init__(self, start, direction, label, **kwargs):

        self.start = start
        self.direction = direction

        self._label = f"{start}->{direction}" if label is None else label
        self._latex_label = latex(f"{start}->{direction}") if label is None else label

        self.expr = kwargs.get("expr", "")
        self.use_cm = kwargs.get("use_cm", True)
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

    if len(args) == 4:
        args = [[args[0], args[1]], [args[2], args[3]]]
    if len(args) == 6:
        args = [[args[0], args[1], args[2]], [args[3], args[4], args[5]]]

    assert len(args) in [
        2,
        3,
    ], f"Error! Expected 2 or 3 arguments for quiver, but got {len(args)}!"

    try:
        args = np.array(args, dtype=float)
        assert args.shape[-1] in [2, 3]
    except:
        raise f"Error! Wrong format used in quiver. \
        Got {args[0]} as starting point(s) and {args[1]} as ending point(s)!"

    # want structure to be [list of starts, list of ends]
    # where list of starts could be [start1, start2, ...], either 2D or 3D points
    if len(args.shape) == 2:
        args = args[:, None, :]

    labels = kwargs.pop("label", [])
    assert type(labels) == list, f"Error! Label must be a list!"
    assert len(labels) in [
        0,
        args.shape[1],
    ], f"Error! Number of labels must be equal to number of arrows, or empty list!"
    if labels == []:
        labels = [None] * args.shape[1]

    kwargs.setdefault("legend", True)
    params = kwargs.get("params", None)
    is_interactive = False if params is None else True
    kwargs["is_interactive"] = is_interactive
    if is_interactive:
        from spb.interactive import iplot

        kwargs["is_vector"] = True
        return iplot(*args, **kwargs)

    series = [
        ArrowSeries(start, stop, label=label, **kwargs)
        for start, stop, label in zip(args[0, :, :], args[1, :, :], labels)
    ]

    rendering_kw = kwargs.pop("rendering_kw", None)

    # if 2D
    if args.shape[-1] == 2:
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
    return _instantiate_backend(Backend, *series, **kwargs)
