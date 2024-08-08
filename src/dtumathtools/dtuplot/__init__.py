from spb import *
from spb.defaults import (
    cfg,  # can still be imported though not recognized
    get_default_settings,
    set_defaults,
)

from .boundaryplot import plot_boundary
from .quiverplot import Arrow2DSeries, Arrow3DSeries, quiver

# Backends to support the vector plotting functionality.
from .quiverplot_helpers import (
    BBQuiver2DRenderer as BBV2,
)
from .quiverplot_helpers import (
    KBQuiver3DRenderer as KBV3,
)
from .quiverplot_helpers import (
    MABQuiver3DRenderer as MABV3,
)
from .quiverplot_helpers import (
    MBQuiver2DRenderer as MBV2,
)
from .quiverplot_helpers import (
    MBQuiver3DRenderer as MBV3,
)
from .quiverplot_helpers import (
    PBQuiver2DRenderer as PBV2,
)
from .quiverplot_helpers import (
    PBQuiver3DRenderer as PBV3,
)
from .scatterplot import scatter

MB.renderers_map.update(
    {
        Arrow2DSeries: MBV2,
        Arrow3DSeries: MBV3,
    }
)
PB.renderers_map.update(
    {
        Arrow2DSeries: PBV2,
        Arrow3DSeries: PBV3,
    }
)
BB.renderers_map.update(
    {
        Arrow2DSeries: BBV2,
    }
)
KB.renderers_map.update(
    {
        Arrow3DSeries: KBV3,
    }
)
MAB.renderers_map.update({Arrow3DSeries: MABV3})

# Update Mayavi functionality to support scatter plotting
from spb.series import List3DSeries

from .scatterplot import Point3DRenderer

MAB.renderers_map.update({List3DSeries: Point3DRenderer})
