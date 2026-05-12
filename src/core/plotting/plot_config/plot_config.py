from .config import PlottingConfig

from .methods.axis import Axis
from .methods.cmap import CMap
from .methods.vlims import VLims
from .methods.colorbar import Colorbar
from .methods.extent import Extent
from .methods.zscale import ZScale
from .methods.alpha import Alpha


class PlotConfigMethods(
    PlottingConfig,
    Extent,
    VLims,
    CMap,
    Axis,
    Colorbar,
    ZScale,
    Alpha,
):
    pass