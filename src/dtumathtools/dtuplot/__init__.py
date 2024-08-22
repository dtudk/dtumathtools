from spb import *
from spb.defaults import (
    cfg,  # can still be imported though not recognized
    get_default_settings,
    set_defaults,
)

from .boundaryplot import plot_boundary
from .quiverplot import Arrow2DSeries, Arrow3DSeries, quiver

# Change plotting function and renderer for plotly when
# plotting quivers/arrows. This allows for plotting of 
# 3D vectors.

from .quiverplot_helpers import (
    PBQuiver2DRenderer as PBV2,
    Arrow2DSeries as PB_Arrow2DSeries,
)
from .quiverplot_helpers import (
    PBQuiver3DRenderer as PBV3,
    Arrow3DSeries as PB_Arrow3DSeries,
)
from .scatterplot import scatter

PB.renderers_map.update(
    {
        PB_Arrow2DSeries: PBV2,
        PB_Arrow3DSeries: PBV3,
    }
)
