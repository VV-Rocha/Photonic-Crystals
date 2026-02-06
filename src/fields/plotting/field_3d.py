import matplotlib.pyplot as plt
import numpy as np

from .utils import Extent, Axis

def _plot3d_field(
        xx,
        yy,
        intensity,
        vlims,
        alpha,
        cmap,
        axis_labels,
        colorbar_label,
        # zorder,
    ):
    fig = plt.figure()
    axs = fig.add_subplot(111, projection='3d')
    
    print(">", vlims)        
    
    # Plot the 2D field
    im = axs.plot_surface(
        xx,
        yy,
        intensity,
        alpha=alpha,
        cmap=cmap,
        # zorder=zorder,
        vmin=vlims[0],
        vmax=vlims[1]
    )
        
    # Add colorbar
    cbar = fig.colorbar(im)
    cbar.set_label(colorbar_label)
        
    # # Set axis labels
    axs.set_xlabel(axis_labels[0])
    axs.set_ylabel(axis_labels[1])
    axs.set_zlabel(axis_labels[2])
        
    return fig, axs


class PlotCoupledFields3D(Extent, Axis):
    def __init__(
        self,
        plot3d_config: dict,
        *args,
        **kwargs,
    ):
        self.rcount = plot3d_config["rcount"]
        super().__init__(*args, **kwargs)
        
    def plot3d_field(
        self,
        zorder = None,
        alpha: float = .8,
        cmap: str = "turbo",
        filename: str | None = None,
    ):
        fig, axs = _plot3d_field(
            self.dimensionalize_length(self.x[self.xx_indices])*self.scale_factor,
            self.dimensionalize_length(self.y[self.yy_indices])*self.scale_factor,
            intensity = self.get_intensity()[self.xx_indices, self.yy_indices],
            vlims=self.vlims,
            alpha=alpha,
            cmap=cmap,
            axis_labels=self.axis_labels,
            colorbar_label=self.colorbar_label,
            # zorder=zorder,
        )
        
        if filename is not None:
            fig.savefig(self.get_directory()+ filename + ".png", dpi=300, transparent=True)
            
        return fig, axs
    
    def plot3d_field1(
        self,
        zorder = None,
        alpha: float = .8,
        cmap: str = "turbo",
        filename: str | None = None,
    ):
        fig, axs = _plot3d_field(
            self.x[self.xx_indices],
            self.y[self.yy_indices],
            intensity=self.get_intensity1[self.xx_indices, self.yy_indices],
            extent=self.extent_plot,
            vlims=self.vlims,
            alpha=alpha,
            cmap=cmap,
            axis_labels=self.axis_labels,
            colorbar_label=self.colorbar_label,
            zorder=zorder,
        )
        
        if filename is not None:
            fig.savefig(self.get_directory1()+ filename + ".png", dpi=300, transparent=True)
            
        return fig, axs
    
    def set_axis_labels(self,):
            """ Set axis labels for plotting."""
            super().set_axis_labels()
            self.axis_labels = (*self.axis_labels, r"I $\left(mW \cdot cm^{-2}\right)$")            