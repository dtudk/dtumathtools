# dtumathtools

## Description
This package is a collection of easy-to-use commands for plotting using SymPy. It is designed to fit the requirements of the *Mathematics 1* course at the Technical University of Denmark. This includes, but is not limited to:

- Plotting of vector fields and vectors
- 2D plotting of SymPy functions
- 3D plotting of SymPy functions
- Scatterplots in 2D and 3D

The plotting functions are an extension of `sympy-plot-backends`, and so documentation and examples of plots (for all functions but `dtuplot.scatter()` and `dtuplot.quiver()`) can be found at [sympy-plot-backends.readthedocs.io/](https://sympy-plot-backends.readthedocs.io/en/v2.4.3/index.html). Additional functionality and usage is given through course material.

## Installation
To install dtumathtools using PyPi, run the following command

```shell
pip install dtumathtools
```

Then one can import all the utility by writing

```python
from dtumathtools import *
```

All plotting functionality can be found using `dtuplot.xxx` (including all `spb` plotting functions).

## Usage
Use is designed for the *Mathematics 1* course at the Technical University of Denmark. Any use-case outside this scope is thus not considered, but very welcome!

## Backends
Multiple different backends (plotting libraries) can be used (especially helpful for some 3D plots). Currently, [Matplotlib](https://matplotlib.org/) (MB), [Plotly](https://plotly.com/) (PB), [Bokeh](https://github.com/bokeh/bokeh) (BB, *2D only*), and [K3D-Jupyter](https://github.com/K3D-tools/K3D-jupyter) (KB, *3D only*) are supported ([Mayavi](https://docs.enthought.com/mayavi/mayavi/) (MAB, *3D only*) might be supported in the future). The user can change the backend for a plot using the *backend* keyword argument (eg. `backend=dtuplot.PB`), or change the default (here for 3D, but similar for 2D) using:

```python
dtuplot.cfg["backend_3D"] = "plotly"
dtuplot.set_defaults(dtuplot.cfg)
```

For further descriptions of the strengths and benefits of each, see [this page](https://sympy-plot-backends.readthedocs.io/en/v2.4.3/modules/backends/index.html).

## Contributing
You are very welcome to contribute in the way that makes sense to you! The development team will consider all pull requests at the repo [here](https://github.com/dtudk/dtumathtools). For changes to plotting functionality outside `scatter` and `quiver`, direct queries to [spb](https://github.com/Davide-sd/sympy-plot-backends).

## Authors and acknowledgment
The project would have never gotten off the ground without Jakob Lemvig and his engagement with SymPy in Mathematics 1. Thank you to Ulrik Engelund Pedersen for trusting us with this task. Finally, a huge thanks to the professors of the course for making great and engaging education: Michael Pedersen and Karsten Schmidt.

## License
Open-source under the BSD license. This means that you are free to use it whatever you like, be it academic, commercial, creating forks or derivatives, as long as you copy the BSD statement if you redistribute it (see the LICENSE file for details).
