from sympy.external import import_module
from spb.functions import plot_list, plot3d_list


def scatter(*args, **kwargs):

    np = import_module("numpy")
    warnings = import_module("warnings")

    def warning_formatter(msg, *args, line=None, **kwargs):
        return str(msg)

    warnings.formatwarning = warning_formatter

    # format all arguments
    dim = 0
    args = list(args)
    for i in range(len(args)):
        if type(args[i]) in (list, tuple):
            args[i] = np.array(args[i])
            dim += 1
        elif type(args[i]) == np.ndarray:
            if len(args[i].shape) > 1:
                warnings.warn(
                    f"np.array with more than 1 dimension ({len(args[i].shape)} dimensions was found) has been flattened!"
                )
            args[i] = args[i].flatten()
            dim += 1
        elif type(args[i]) in [float, int]:
            args[i] = np.array([args[i]])
            dim += 1

    assert dim in [2, 3], "scatterplot only supports 2D and 3D plots"
    if dim == 2:
        return plot_list(*args, is_point=True, **kwargs)
    else:
        return plot3d_list(*args, is_point=True, **kwargs)
