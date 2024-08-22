from spb import MB, PB, BB, KB, MAB
from spb.defaults import THREE_D_B, TWO_D_B
from spb.plot_functions.functions_2d import _set_labels
from spb.utils import _instantiate_backend
from sympy import Matrix
from sympy.external import import_module
import warnings
from spb.series import Arrow2DSeries, Arrow3DSeries
from .quiverplot_helpers import Arrow2DSeries as PB_Arrow2DSeries, Arrow3DSeries as PB_Arrow3DSeries

np = import_module("numpy")
        
def quiver(*args, **kwargs):
    """Create a plot with a vector.

    Args:
        start (MatrixBase, np.ndarray, list, float): The starting coordinates (2D or 3D) of the vector. Can be given in multitude of ways/inputs.
        direction (MatrixBase, np.ndarray, list, float): The direction (2D or 3D) of the vector. Can be given in multitude of ways/inputs.
        rendering_kw (dict, optional): A dictionary forwarded to dtuplot.plot(), see SPB docs for reference.
        qlim (bool, optional): Boolean relevant only for backend MB. If 'True' (default is False) adjusts xlim and ylim (and zlim) to the quiver.
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
        raise ValueError(
            f"Error! Wrong format used in quiver. Got {num_single} arguments that could be start or direction vector coordinates!"
        )

    # split arguments into vectors and other arguments
    point_args = []
    otherargs = []
    for i in range(len(args)):
        if type(args[i]) in [list, np.ndarray, tuple, type(Matrix())]:
            newpoint = np.array(args[i]).flatten()
            point_args.append(newpoint)
        elif isinstance(args[i], dict):
            kwargs.setdefault("rendering_kw", args[i])
        else:
            otherargs.append(args[i])
    assert (
        len(point_args) == 2
    ), "Error! Start and direction vectors must be provided (only two vectors)!"

    try:
        point_args = np.array(point_args, dtype=float)
        assert point_args.shape[-1] in [
            2,
            3,
        ], "Error! Start and direction vectors must be 2D or 3D!"
        args = otherargs
    except:
        raise ValueError(
            f"Error! Wrong format used in quiver. Got {point_args[0]} as starting point(s) and {point_args[1]} as ending point(s)!"
        )

    # want structure to be [list of starts, list of ends]
    # where list of starts could be [start1, start2, ...], either 2D or 3D points
    if len(point_args.shape) == 2:
        point_args = point_args[:, None, :]

    # rendering_kw needs to be passed to the plotting backend, but not
    # to the series. Thus pulled out here.
    # Create if it does not exist
    rendering_kw = kwargs.pop("rendering_kw", {})

    labels = kwargs.pop("label", [])
    # Look in rendering_kw if not found as seperate argument
    labels = rendering_kw.pop("label", []) if labels == [] else labels
    if type(labels) == str:
        labels = [labels]
    assert type(labels) == list, f"Error! Label must be a list or a string!"
    assert len(labels) in [
        0,
        point_args.shape[1],
    ], f"Error! Number of labels must be equal to number of arrows, or empty list!"
    if labels == []:
        labels = [""] * point_args.shape[1]
        kwargs.setdefault("legend", False)
    else:
        # Label is given, so set legend=True as default
        kwargs.setdefault("legend", True)
        # If given as latex code already, do not wrap in additional $ later
        if labels[0][0] == "$":
            kwargs.setdefault("use_latex", False)

    # params are directly linked with interactive plots
    # if present, the BaseSeries will activate the 'is_interactive' flag
    params = kwargs.get("params", None)
    is_interactive = False if params is None else True
    if is_interactive:
        raise NotImplementedError("Interactive quiver plots are not yet implemented!")
        from spb.interactive import iplot

        kwargs["is_vector"] = True
        return iplot(*args, **kwargs)
    # normalize argument needs to be passed to series object, but not to
    # backend. Otherwise warning will be raised. Thus pulled out here.
    normalize = kwargs.pop("normalize", False)
    
    # if 2D
    if point_args.shape[-1] == 2:
        Backend = kwargs.pop("backend", TWO_D_B)

        # Specific arguments for backends
        if Backend == PB:
            rendering_kw.setdefault("scale", 1)
            rendering_kw.setdefault("scaleratio", 1)
            # I do not like how plotly is handled in spb,
            # so for PB, we use the older solution that works well
            Series = PB_Arrow2DSeries
        else:
            Series = Arrow2DSeries
            
        if Backend == KB:
            raise NotImplementedError("K3D backend does not support 2D vector plots!")
        if Backend == MAB:
            raise NotImplementedError(
                "Mayavi backend does not support 2D vector plots!"
            )
    else:
        Backend = kwargs.pop("backend", THREE_D_B)

        if Backend == PB:
            rendering_kw.setdefault("sizeref", 1)
            rendering_kw.setdefault("sizemode", "scaled")
            rendering_kw.setdefault("anchor", "tail")
            # I do not like how plotly is handled in spb (does not work in 3D)
            # so for PB, we use the older solution that works well
            Series = PB_Arrow3DSeries
        else:
            Series = Arrow3DSeries
        if Backend == BB:
            raise NotImplementedError("Bokeh backend does not support 3D vector plots!")

        if Backend == MAB:
            warnings.warn("Mayavi is not currently supported by dtumathtools.")
            display_warning = kwargs.pop("warning", True)
            if display_warning:
                warnings.warn(
                    "Because of the Mayavi backend, the origin of the vector might be slightly off. "+\
                        "To supress this warning, set 'warning=False'"
                )
    
    if "qlim" not in kwargs and "xlim" not in kwargs and "ylim" not in kwargs and point_args.shape[-1] == 3 and Backend == MB:
        warnings.warn("Warning: Limits were not given for a 3D quiver using Matplotlib. "+\
            "The quiver might not be in frame. Consider manually setting the limits, or set 'qlim=True'.")
    # automatically adjust the limits to the quiver. Only relevant for MB.
    # saved in series, which propagates to the renderer when created.
    qlim = kwargs.pop("qlim", False)
    
    # Automatically adjust limits (if not already given) if qlim=True
    if Backend == MB and qlim:
        margin = kwargs.pop("margin", 0.05)
        # lower and upper boundaries of limits
        minlim, maxlim = point_args[0].copy(), point_args[0].copy()
        # tmp = minlim.copy()
        minlim[point_args[1]<0] += point_args[1][point_args[1]<0]
        maxlim[point_args[1]>0] += point_args[1][point_args[1]>0]
        # minlim = tmp
        kwargs.setdefault("xlim", [np.nanmin(minlim[:,0])-margin, np.nanmax(maxlim[:,0])+margin])
        kwargs.setdefault("ylim", [np.nanmin(minlim[:,1])-margin, np.nanmax(maxlim[:,1])+margin])
        if point_args.shape[-1] == 3:
            kwargs.setdefault("zlim", [np.nanmin(minlim[:,2])-margin, np.nanmax(maxlim[:,2])+margin])

    series = [
        Series(
            start,
            stop,
            *otherargs,
            label=label,
            normalize=normalize,
            show_in_legend=False if label=="" else True, # remove legend if no label
            **kwargs,
        )
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
