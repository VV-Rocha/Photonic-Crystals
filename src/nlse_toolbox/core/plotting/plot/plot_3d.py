from .utils import get_extent_region


def _plot3d(
        xx,
        yy,
        z,
        fig,
        axs,
        cmap,
        axis_labels,
        colorbar_label,
        vlims = (None, None),
        alpha = None,
    ):
    axs = fig.add_subplot(111, projection='3d')

    im = axs.plot_surface(
        xx,
        yy,
        z,
        alpha=alpha,
        cmap=cmap,
        vmin=vlims[0],
        vmax=vlims[1],
        rcount = 256,
        ccount = 256,
    )
    
    # Add colorbar
    cbar = fig.colorbar(im)
    cbar.set_label(colorbar_label)
        
    # # Set axis labels
    axs.set_xlabel(axis_labels[0])
    axs.set_ylabel(axis_labels[1])
    axs.set_zlabel(axis_labels[2])
        
    return fig, axs

def _plot_region_3d(
        xx,
        yy,
        z,
        fig,
        axs,
        cmap,
        axis_labels,
        colorbar_label,
        vlims = (None, None),
        alpha = None,
        extent = None,
):
    xx, yy, z = get_extent_region(
        xx,
        yy,
        z,
        extent,
    )
    
    _plot3d(
        xx = xx,
        yy = yy,
        z = z,
        fig = fig,
        axs = axs,
        cmap = cmap,
        axis_labels = axis_labels,
        colorbar_label = colorbar_label,
        vlims = vlims,
        alpha = alpha,
    )