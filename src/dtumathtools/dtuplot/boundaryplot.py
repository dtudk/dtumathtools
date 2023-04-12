from spb.functions import plot_parametric
from sympy import Matrix

def plot_boundary(param_func: Matrix, *args, **kwargs):
    if len(param_func) == 2:
        bounds = []
        for i, arg in enumerate(args):
            if isinstance(arg, tuple):
                bounds.append(arg)
                if isinstance(arg[1], list):
                    bounds[-1] = (arg[0], *arg[1])
            else:
                rest = args[i+1:]
                args = rest
                break
        else:
            args = []
        if len(bounds) != 2:
            raise ValueError("For 2D-areas two variables are needed to plot boundary")

        show = kwargs.pop('show', True)
        color = kwargs.pop('color', 'blue')
        plot = plot_parametric(show=False)
        for i in range(2):
            plot += plot_parametric(*param_func.subs(bounds[i][0], bounds[i][1]),
                                        (bounds[1-i][0], *bounds[1-i][1:]), 
                                        {'color': color}, *args, 
                                        show=False, **kwargs
            )
            plot += plot_parametric(*param_func.subs(bounds[i][0], bounds[i][2]),
                                        (bounds[1-i][0], *bounds[1-i][1:]), 
                                        {'color': color}, *args, 
                                        show=False, **kwargs
            )
    elif len(param_func) == 3:
        raise NotImplementedError('Volume boundary plots are not yet implemented')

    plot.legend = kwargs.pop('legend', False)
    plot.xlabel = kwargs.pop('xlabel', 'x')
    plot.ylabel = kwargs.pop('ylabel', 'y')
    plot.zlabel = kwargs.pop('zlabel', 'z')
    plot.aspect = kwargs.pop('aspect', 'auto')

    if show:
        plot.show()
        return plot
    else:
        return plot