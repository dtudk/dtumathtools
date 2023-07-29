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
    BBQuiver2DRenderer as BBV2
)
# K3D
from spb.backends.k3d.renderers.vector3d import Vector3DRenderer as KBV3
# Mayavi
from spb.backends.mayavi.renderers.vector3d import Vector3DRenderer as MABV3

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