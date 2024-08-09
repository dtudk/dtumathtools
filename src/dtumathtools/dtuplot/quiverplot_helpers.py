# Have not been happy with how quivers are handled in plotly.
# This code works around the limitations using the (very nice)
# vector plotting functionality of plotly (instead of the arrow).

# Plotly
from spb.backends.base_renderer import Renderer
from spb.backends.plotly.renderers.vector2d import (
    _draw_vector2d_helper as PB_draw_vector2d_helper,
)
from spb.backends.plotly.renderers.vector2d import (
    _update_vector2d_helper as PB_update_vector2d_helper,
)
from spb.backends.plotly.renderers.vector3d import (
    _draw_vector3d_helper as PB_draw_vector3d_helper,
)
from spb.backends.plotly.renderers.vector3d import (
    _update_vector3d_helper as PB_update_vector3d_helper,
)
from spb.series import VectorBase
from sympy import latex
from sympy.external import import_module

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
        # Line color needed for Mayavi
        self._line_color = kwargs.get("line_color", None)
        # _sal argument saved here and passed to matplotlib backend (if used)
        self._sal = kwargs.get("_sal", False)

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
        return np.array(
            [start, end]
        ).T  # [np.array([v]) for v in list(self.start) + list(self.direction)]


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




def PB_draw_quiver2d_helper(renderer, data):
    start, end = data.T
    direction = end - start
    xx, yy = start
    uu, vv = direction
    return PB_draw_vector2d_helper(renderer, ([xx], [yy], [uu], [vv]))


def PB_update_quiver2d_helper(renderer, data, handle):
    start, end = data.T
    direction = end - start
    xx, yy = start
    uu, vv = direction
    return PB_update_vector2d_helper(renderer, ([xx], [yy], [uu], [vv]), handle)


class PBQuiver2DRenderer(Renderer):
    draw_update_map = {PB_draw_quiver2d_helper: PB_update_quiver2d_helper}


def PB_draw_quiver3d_helper(renderer, data):
    start, end = data.T
    direction = end - start
    xx, yy, zz = start
    uu, vv, ww = direction
    return PB_draw_vector3d_helper(renderer, (xx, yy, zz, uu, vv, ww))


def PB_update_quiver3d_helper(renderer, data, handle):
    start, end = data.T
    direction = end - start
    xx, yy, zz = start
    uu, vv, ww = direction
    return PB_update_vector3d_helper(renderer, (xx, yy, zz, uu, vv, ww), handle)


class PBQuiver3DRenderer(Renderer):
    draw_update_map = {PB_draw_quiver3d_helper: PB_update_quiver3d_helper}

