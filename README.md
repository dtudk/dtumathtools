# DTUMathTools

## Description
This package is a collection of easy-to-use commands for plotting using SymPy. It is designed to fit the requirements of *01005 - Advanced Mathematics in Engineering 1* course at the Technical University of Denmark, found [here](https://01005.compute.dtu.dk/). This includes, but is not limited to:

- Plotting of vector fields and vectors
- 2D plotting of SymPy functions
- 3D plotting of SymPy functions
- Scatterplots in 2D and 3D

The plotting functions are an extension of *sympy-plot-backends*, and so documentation and examples of plots (for all functions but *dtuplot.scatter()* and *dtuplot.quiver()*) can be found at [sympy-plot-backends.readthedocs.io/](https://sympy-plot-backends.readthedocs.io/en/latest/)

## Installation
To install mat1plot using PyPi, run the following command

``$ pip install dtumathtools``

Then one can import all the utility by writing

``from dtumathtools import *``

All plotting functionality can be found using *dtuplot.xxx* (including all spb plotting functions).

## Usage
Use is designed for the *01005 - Advanced Mathematics in Engineering 1* course at the Technical University of Denmark. Any use-case outside this scope is thus not considered, but very welcome!

## Contributing
You are very welcome to contribute in the way that makes sense to you! The development team will consider all pull requests, as well as mails directly to the developers ``s194345@student.dtu.dk`` or ``s194042@student.dtu.dk``. For changes to plotting functionality outside *scatter* and *quiver*, direct queries to [spb](https://github.com/Davide-sd/sympy-plot-backends).

## Authors and acknowledgment
The project would have never gotten off the ground without Jakob Lemvig and his engagement with SymPy in Mathematics 1. Thank you to Ulrik Engelund Pedersen for trusting us with this task. Finally, a huge thanks to the professors of the course for making great and engaging education: Micheal Pedersen and Karsten Schmidt.

## License
Open-source under the BSD license. This means that you are free to use it whatever you like, be it academic, commercial, creating forks or derivatives, as long as you copy the BSD statement if you redistribute it (see the LICENSE file for details).

## Project status
This package is in deployment phase. First draft is expected to be finished for January 2023, and the version to be used expected done for February 2023.
