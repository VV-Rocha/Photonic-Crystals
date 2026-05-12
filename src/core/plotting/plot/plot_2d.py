from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .utils import get_extent_region


def _plot2d(
    xx,
    yy,
    field,
    extent,
    vlims,
    fig,
    axs,
    cmap,
    axis_labels,
    colorbar_label,
    zscale,
    zorder=None,
):
    xx, yy, field = get_extent_region(
        xx,
        yy,
        field,
        extent,
    )
    
    if (zscale==None):
        zscale = None
    elif (zscale.lower()=="log"):
        zscale = LogNorm(vmin=vlims[0]+10e-16, vmax=vlims[1])
    else:
        zscale = None

    im = axs.imshow(
        field,
        extent = extent,
        norm = zscale,
        cmap=cmap,
        zorder=zorder,
        vmin=vlims[0],
        vmax=vlims[1]
    )
    
    axs.set_xlabel(axis_labels[0])
    axs.set_ylabel(axis_labels[1])
    
    divider = make_axes_locatable(axs)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    fig.colorbar(im, cax=cax, label=colorbar_label)
        
    return fig, axs