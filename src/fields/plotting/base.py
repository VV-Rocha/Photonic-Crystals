import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def plot2d(
    intensity,
    extent,
    vlims,
    fig,
    axs,
    alpha,
    cmap,
    axis_labels,
    colorbar_label,
    zorder,
    norm,
):
    if norm == None:
        norm = None
    elif norm.lower() == "log":
        norm = LogNorm(vmin=vlims[0]+10e-16, vmax=vlims[1])
    else:
        norm = None

    im = axs.imshow(
        intensity,
        extent = extent,
        norm = norm,
        alpha=alpha,
        cmap=cmap,
        zorder=zorder,
        vmin=vlims[0],
        vmax=vlims[1]
    )
    
    axs.set_xlabel(axis_labels[0])
    axs.set_ylabel(axis_labels[1])
    
    fig.colorbar(im, ax=axs, label=colorbar_label)
    
    return fig, axs