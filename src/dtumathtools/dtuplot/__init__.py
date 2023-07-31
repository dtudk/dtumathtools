from spb import *
from .quiverplot import quiver, Arrow2DSeries, Arrow3DSeries
from .scatterplot import scatter
from .boundaryplot import plot_boundary
from spb.defaults import get_default_settings, cfg, set_defaults

# Backends to support the vector plotting functionality.
from .quiverplot_helpers import (
    MBQuiver2DRenderer as MBV2,
    MBQuiver3DRenderer as MBV3,
    PBQuiver2DRenderer as PBV2,
    PBQuiver3DRenderer as PBV3,
    BBQuiver2DRenderer as BBV2,
    KBQuiver3DRenderer as KBV3,
    MABQuiver3DRenderer as MABV3
)

MB.renderers_map.update({
    Arrow2DSeries: MBV2,
    Arrow3DSeries: MBV3,
})
PB.renderers_map.update({
    Arrow2DSeries: PBV2,
    Arrow3DSeries: PBV3,
})
BB.renderers_map.update({
    Arrow2DSeries: BBV2,
})
KB.renderers_map.update({
    Arrow3DSeries: KBV3,
})
MAB.renderers_map.update({
    Arrow3DSeries: MABV3
})

# Update Mayavi functionality to support scatter plotting
from .scatterplot import Point3DRenderer
from spb.series import List3DSeries
MAB.renderers_map.update({
    List3DSeries: Point3DRenderer
})