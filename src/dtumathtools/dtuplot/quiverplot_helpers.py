# Following are the helper functions such that data can be read 
# and passed on correctly for all backends

# Matplotlib
from spb.backends.matplotlib.renderers.vector2d import (
    _draw_vector2d_helper as MB_draw_vector2d_helper, 
    _update_vector2d_helper as MB_update_vector2d_helper,
)
from spb.backends.matplotlib.renderers.vector3d import (
    _draw_vector3d_helper as MB_draw_vector3d_helper, 
    _update_vector3d_helper as MB_update_vector3d_helper,
)
from spb.backends.matplotlib.renderers.renderer import MatplotlibRenderer
def MB_draw_quiver2d_helper(renderer, data):
    start, end = data.T
    direction = end-start
    xx,yy = start
    uu,vv = direction
    return MB_draw_vector2d_helper(renderer, (xx,yy,uu,vv))

def MB_update_quiver2d_helper(renderer, data, handle):
    start, end = data.T
    direction = end-start
    xx,yy = start
    uu,vv = direction
    return MB_update_vector2d_helper(renderer, (xx,yy,uu,vv), handle)

class MBQuiver2DRenderer(MatplotlibRenderer):
    _sal = True
    draw_update_map = {
        MB_draw_quiver2d_helper: MB_update_quiver2d_helper
    }

def MB_draw_quiver3d_helper(renderer, data):
    start, end = data.T
    direction = end-start
    xx,yy,zz = start
    uu,vv,ww = direction
    return MB_draw_vector3d_helper(renderer, (xx,yy,zz,uu,vv,ww))

def MB_update_quiver3d_helper(renderer, data, handle):
    start, end = data.T
    direction = end-start
    xx,yy,zz = start
    uu,vv,ww = direction
    return MB_update_vector3d_helper(renderer, (xx,yy,zz,uu,vv,ww), handle)

class MBQuiver3DRenderer(MatplotlibRenderer):
    _sal=True
    draw_update_map = {
        MB_draw_quiver3d_helper: MB_update_quiver3d_helper
    }

# Plotly
from spb.backends.plotly.renderers.vector2d import (
    _draw_vector2d_helper as PB_draw_vector2d_helper, 
    _update_vector2d_helper as PB_update_vector2d_helper,
)
from spb.backends.plotly.renderers.vector3d import (
    _draw_vector3d_helper as PB_draw_vector3d_helper, 
    _update_vector3d_helper as PB_update_vector3d_helper,
)
from spb.backends.base_renderer import Renderer
def PB_draw_quiver2d_helper(renderer, data):
    start, end = data.T
    direction = end-start
    xx,yy = start
    uu,vv = direction
    return PB_draw_vector2d_helper(renderer, ([xx],[yy],[uu],[vv]))

def PB_update_quiver2d_helper(renderer, data, handle):
    start, end = data.T
    direction = end-start
    xx,yy = start
    uu,vv = direction
    return PB_update_vector2d_helper(renderer, ([xx],[yy],[uu],[vv]), handle)

class PBQuiver2DRenderer(Renderer):
    draw_update_map = {
        PB_draw_quiver2d_helper: PB_update_quiver2d_helper
    }

def PB_draw_quiver3d_helper(renderer, data):
    start, end = data.T
    direction = end-start
    xx,yy,zz = start
    uu,vv,ww = direction
    return PB_draw_vector3d_helper(renderer, (xx,yy,zz,uu,vv,ww))

def PB_update_quiver3d_helper(renderer, data, handle):
    start, end = data.T
    direction = end-start
    xx,yy,zz = start
    uu,vv,ww = direction
    return PB_update_vector3d_helper(renderer, (xx,yy,zz,uu,vv,ww), handle)

class PBQuiver3DRenderer(Renderer):
    draw_update_map = {
        PB_draw_quiver3d_helper: PB_update_quiver3d_helper
    }

# Bokeh
from spb.backends.bokeh.renderers.vector2d import (
    _draw_vector2d_helper as BB_draw_vector2d_helper, 
    _update_vector2d_helper as BB_update_vector2d_helper,
)

def BB_draw_quiver2d_helper(renderer, data):
    start, end = data.T
    direction = end-start
    xx,yy = start
    uu,vv = direction
    return BB_draw_vector2d_helper(renderer, (xx,yy,uu,vv))

def BB_update_quiver2d_helper(renderer, data, handle):
    start, end = data.T
    direction = end-start
    xx,yy = start
    uu,vv = direction
    return BB_update_vector2d_helper(renderer, (xx,yy,uu,vv), handle)

class BBQuiver2DRenderer(Renderer):
    draw_update_map = {
        BB_draw_quiver2d_helper: BB_update_quiver2d_helper
    }

# K3D
from spb.backends.k3d.renderers.vector3d import (
    _draw_vector3d_helper as KB_draw_vector3d_helper, 
    _update_vector3d_helper as KB_update_vector3d_helper,
)

def KB_draw_quiver3d_helper(renderer, data):
    start, end = data.T
    direction = end-start
    xx,yy,zz = start
    uu,vv,ww = direction
    return KB_draw_vector3d_helper(renderer, (xx,yy,zz,uu,vv,ww))

def KB_update_quiver3d_helper(renderer, data, handle):
    start, end = data.T
    direction = end-start
    xx,yy,zz = start
    uu,vv,ww = direction
    return KB_update_vector3d_helper(renderer, (xx,yy,zz,uu,vv,ww), handle)

class KBQuiver3DRenderer(Renderer):
    draw_update_map = {
        KB_draw_quiver3d_helper: KB_update_quiver3d_helper
    }

# Mayavi
from spb.backends.mayavi.renderers.vector3d import (
    _draw_vector3d_helper as MAB_draw_vector3d_helper, 
    _update_vector3d_helper as MAB_update_vector3d_helper,
)

def MAB_draw_quiver3d_helper(renderer, data):
    start, end = data.T
    direction = end-start
    xx,yy,zz = start
    uu,vv,ww = direction
    return MAB_draw_vector3d_helper(renderer, (xx,yy,zz,uu,vv,ww))

def MAB_update_quiver3d_helper(renderer, data, handle):
    start, end = data.T
    direction = end-start
    xx,yy,zz = start
    uu,vv,ww = direction
    return MAB_update_vector3d_helper(renderer, (xx,yy,zz,uu,vv,ww), handle)

class MABQuiver3DRenderer(Renderer):
    draw_update_map = {
        MAB_draw_quiver3d_helper: MAB_update_quiver3d_helper
    }