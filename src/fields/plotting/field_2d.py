import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

from .base import plot2d
from .decorators import construct_figure

from .utils import Extent, Axis


@construct_figure
def plot2d_wrapped(
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
    """ Wrapper for plot2d function."""
    return plot2d(
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
    )

class Plot2DField:
    """ Class to handle 2D field plotting."""        
    def init_plot_field(self,):
        """ Initialize plot field parameters."""
        if self.adimensional_flag:
            self.scale = "adimensional"
        else:
            self.scale = "m"
        self.set_scale(self.scale)

    def plot_field_2d(
        self,
        filename=None,
        fig=None,
        axs=None,
        alpha=None,
        cmap=None,
        scale=None,
        extent_plot=None,
        zorder=None,
        norm=None,
    ):
        """ Plot 2D field.

        Args:
            filename (_type_, optional): _description_. Defaults to None.
            fig (_type_, optional): _description_. Defaults to None.
            axs (_type_, optional): _description_. Defaults to None.
            alpha (_type_, optional): _description_. Defaults to None.
            cmap (_type_, optional): _description_. Defaults to None.
            scale (_type_, optional): _description_. Defaults to None.
            extent_plot (_type_, optional): _description_. Defaults to None.
            zorder (_type_, optional): _description_. Defaults to None.
            norm (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        self.set_axis_labels()
        if scale != None:
            self.set_scale(scale)
        if extent_plot is not None:
            self.set_extent(extent_plot)
        
        fig, axs = plot2d_wrapped(
            intensity = self.get_intensity()[self.xx_indices, self.yy_indices],
            extent = self.dimensionalize_extent(),
            vlims = self.vlims,
            fig = fig,
            axs = axs,
            alpha=alpha,
            cmap=cmap,
            axis_labels = self.axis_labels,
            colorbar_label = self.colorbar_label,
            zorder = zorder,
            norm = norm,
        )
        
        if filename is not None:
            fig.savefig(self.get_directory(filename, extension=".png"), dpi=300, transparent=True)
        
        return fig, axs

class PlotField(Plot2DField, Extent, Axis):
    """ Class to handle field plotting."""
    def init_plot_field(self,):
        """ Initialize plot field parameters."""
        self.init_extent()
        self.init_axis()
        
class PlotCoupledFields2D(Plot2DField, Extent, Axis):
    """ Class to handle coupled fields plotting."""
    @property
    def plot_flag(self,):
        return True
        
    def init_plot(self,):
        """ Initialize plot field parameters."""
        self.init_extent()
        self.init_vlims1()
        self.init_axis()

    def plot_2d_fields(
        self,
        filename=None,
    ):
        fig, axs = plt.subplots(2,2)
        fig, axs[0,0] = plot2d_wrapped(
            intensity = self.get_intensity()[self.xx_indices, self.yy_indices],
            extent = self.dimensionalize_extent(),
            vlims = self.vlims,
            fig = fig,
            axs = axs[0,0],
            alpha=None,
            cmap="Greens" if self.wavelength==532e-9 else "Reds",
            axis_labels = self.axis_labels,
            colorbar_label = self.colorbar_label,
            zorder = None,
            norm = None,
        )
        
        fig, axs[0,1] = plot2d_wrapped(
            intensity = np.angle(self.field[self.xx_indices, self.yy_indices]),
            extent = self.dimensionalize_extent(),
            vlims = self.vlims,
            fig = fig,
            axs = axs[0,1],
            alpha=None,
            cmap = "RdBu",
            axis_labels = self.axis_labels,
            colorbar_label = "Phase",
            zorder = None,
            norm = None,
        )
        
        fig, axs[1,0] = plot2d_wrapped(
            intensity = self.get_intensity1()[self.xx_indices, self.yy_indices],
            extent = self.dimensionalize_extent(),
            vlims = self.vlims,
            fig = fig,
            axs = axs[1,0],
            alpha=None,
            cmap="Greens" if self.wavelength1==532e-9 else "Reds",
            axis_labels = self.axis_labels,
            colorbar_label = self.colorbar_label,
            zorder = None,
            norm = None,
        )
        
        fig, axs[1,1] = plot2d_wrapped(
            intensity = np.angle(self.field1[self.xx_indices, self.yy_indices]),
            extent = self.dimensionalize_extent(),
            vlims = self.vlims,
            fig = fig,
            axs = axs[1,1],
            alpha=None,
            cmap = "RdBu",
            axis_labels = self.axis_labels,
            colorbar_label = "Phase",
            zorder = None,
            norm = None,
        )
        
        if filename is not None:
            fig.tight_layout()
            fig.savefig(self.get_directory() + filename + ".png", dpi=300, transparent=True)
        
        return fig, axs
        
    def plot_2d_coupled(
        self,
        alpha=.5,
        filename=None,
        norms=[None, None],
    ):
        """ Plot coupled fields in 2D.

        Args:
            alpha (float, optional): _description_. Defaults to .5.
            filename (_type_, optional): _description_. Defaults to None.
            norms (list, optional): _description_. Defaults to [None, None].

        Returns:
            _type_: _description_
        """
        fig, axs = self.plot_field1_2d(cmap="Greens", zorder=0, norm=norms[1])
        fig, axs = self.plot_field_2d(fig=fig,
                                      axs=axs,
                                      alpha=alpha,
                                      cmap="Reds",
                                      zorder=1,
                                      norm=norms[0],
                                      )

        if filename is not None:
            fig.tight_layout()
            fig.savefig(self.get_directory() + filename + ".png", dpi=300, transparent=True)
        
        return fig, axs
        
    def init_vlims1(
        self,
        vmin=None,
        vmax=None,
        ):
        """ Initialize vlims for first field plotting.

        Args:
            vmin (_type_, optional): lower limit. Defaults to None.
            vmax (_type_, optional): upper limit. Defaults to None.
        """
        self.vlims1 = self.get_vlims(vmin, vmax)
        
    def set_vlims1(
        self,
        vmin: float | None,
        vmax: float | None,
        ):
        """ Set vlims for first field plotting.

        Args:
            vmin (float | None): lower limit.
            vmax (float | None): upper limit.
        """
        self.vlims1 = self.get_vlims(vmin, vmax)
        
    def plot_field1_2d(
        self,
        filename=None,
        fig=None,
        axs=None,
        cmap=None,
        zorder=None,
        norm=None,
        scale=None,
    ):
        """ Plot first field in 2D.

        Args:
            filename (_type_, optional): _description_. Defaults to None.
            fig (_type_, optional): _description_. Defaults to None.
            axs (_type_, optional): _description_. Defaults to None.
            cmap (_type_, optional): _description_. Defaults to None.
            zorder (_type_, optional): _description_. Defaults to None.
            norm (_type_, optional): _description_. Defaults to None.
            scale (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        fig, axs = plot2d_wrapped(
            intensity = self.get_intensity1()[self.xx_indices, self.yy_indices],
            extent = self.dimensionalize_extent(),
            vlims = self.vlims1,
            fig = fig,
            axs = axs,
            alpha = 1.,
            cmap=cmap,
            colorbar_label = self.colorbar_label,
            zorder = zorder,
            norm = norm,
            scale=scale,
        )
        
        if filename is not None:
            fig.savefig(self.get_directory(filename), dpi=300, transparent=True)
            
        return fig, axs