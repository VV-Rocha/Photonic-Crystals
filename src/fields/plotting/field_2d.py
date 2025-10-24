import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

from .base import plot2d
from .decorators import dimensions_length, self_scale, construct_figure


class ScaleMethods:
    """ Methods to handle scaling of lengths."""
    @staticmethod
    def scale_config(scale: str):
        """ Configure scale string and factor.

        Args:
            scale (str): Scale type. Options: "micrometer", "milimeter", "meter", "adimensional".

        Returns:
            Tuple[str, float]: _scale string, scale factor.
        """
        if scale.lower() == "micrometer":
            return r"$\mu m$", 1.e6
        elif scale.lower() == "milimeter":
            return r"$mm$", 1.e3
        elif scale.lower() == "meter":
            return r"$m$", 1.e0
        elif scale.lower() == "adimensional":
            return r"$m$", 1.e0
        
    @staticmethod
    def scale_extent(
        extent: list | np.ndarray,
        scale_factor: float,
        ) -> list:
        """ Scale extent by scale factor.

        Args:
            extent (list | np.ndarray): Extent to be scaled.
            scale_factor (float): Scale factor.

        Returns:
            list: Scaled extent.
        """
        return [extent[i]*scale_factor for i in range(4)]

class Scale(ScaleMethods):
    """ Class to handle scaling of lengths."""
    def set_scale(
        self,
        scale: str,
    ):
        """ Set scale for lengths.

        Args:
            scale (str): Scale type. Options: "micrometer", "milimeter", "meter", "adimensional".
        """
        self.scale = scale
        self.scale_str, self.scale_factor = self.scale_config(self.scale)
        
        self.init_default_extent()

    def init_scale(self,):
        """ Initialize scale to default values (meters)."""
        self.scale_factor = 1.
        self.scale = "meters"
        self.scale_str = r"$m$"

class VLimsMethods:
    """ Methods to handle vlims and colorbar labels."""
    def init_vlims(
        self,
        vmin: float | None=None,
        vmax: float | None=None,
        ) -> Tuple[float | None, float | None]:
        """ Initialize vlims for plotting.

        Args:
            vmin (float | None, optional): lower limit. Defaults to None.
            vmax (float | None, optional): upper limit. Defaults to None.

        Returns:
            Tuple[float | None, float | None]: vlims tuple.
        """
        return self.get_vlims(vmin, vmax)

    def init_colorbar_label(self,):
        """ Initialize colorbar label for plotting."""
        return "Intensity " + r"$(mW\cdot cm^2)$"
        
    @staticmethod
    def get_vlims(vmin: float | None, vmax: float | None) -> Tuple[float | None, float | None]:
        """ Get vlims tuple for plotting.

        Args:
            vmin (float | None): lower limit.
            vmax (float | None): upper limit.

        Returns:
            Tuple[float | None, float | None]: vlims tuple.
        """
        return (vmin, vmax)

class ExtentMethods:
    """ Methods to handle extent for plotting."""
    pass  ## currently serving as a placeholder for future methods

class Extent(Scale, ExtentMethods, VLimsMethods):
    """ Class to handle extent for plotting."""
    def set_vlims(
        self,
        vmin: float | None,
        vmax: float | None,
        ):
        """ Set vlims for plotting.

        Args:
            vmin (float | None): lower limit.
            vmax (float | None): upper limit.
        """
        self.vlims = self.get_vlims(vmin, vmax)

    def scale_extent(
        self,
        extent: list | np.ndarray,
    ) -> list | np.ndarray:
        """Scale extent by scale factor.

        Args:
            extent (list | np.ndarray): Extent to be scaled.

        Returns:
            list | np.ndarray: Scaled extent.
        """
        return super().scale_extent(extent, self.scale_factor)
  
    def init_default_extent(self,):
        """ Initialize default extent and related parameters."""
        self.vlims = self.init_vlims()
        self.colorbar_label = self.init_colorbar_label()
        
        self.extent_image = [-self.lx/2, self.lx/2, -self.ly/2, self.ly/2]
        self.set_extent(self.extent_image)
        self.xaxis_label = "x (m)" if not self.adimensional_flag else "x (arb. units)"
        self.yaxis_label = "y (m)" if not self.adimensional_flag else "y (arb. units)"
        
        self.x_indices = np.arange(self.Nx).astype(int)
        self.y_indices = np.arange(self.Ny).astype(int)
        self.xx_indices, self.yy_indices = np.meshgrid(self.x_indices, self.y_indices)
        
    def init_extent(self,):
        """ Initialize extent, vlims, and scale for plotting."""
        self.init_scale()
        self.init_vlims()
        
        self.init_default_extent()
        
    def set_window(
        self,
    ):
        """ Set window indices based on extent for plotting."""
        self.x_indices = np.where((self.x>=self.extent_plot[0]) * (self.x<=self.extent_plot[1]))[0]
        self.y_indices = np.where((self.y>=self.extent_plot[2]) * (self.y<=self.extent_plot[3]))[0]
        
        self.xx_indices, self.yy_indices = np.meshgrid(self.x_indices, self.y_indices)
    
    @dimensions_length
    def set_extent(
        self,
        extent_plot: float | list,
        scale: str | None = None,
    ):
        """ Set extent for plotting.

        Args:
            extent_plot (float | list): Extent to be set.
            scale (str | None, optional): Scale type. Options: "micrometer", "milimeter", "meter", "adimensional". Defaults to None.
        """
        if scale != None:
            self.set_scale(scale)
        self.extent_plot = self.scale_extent(extent_plot)
        self.set_window()

    def dimensionalize_extent(self,):
        """ Dimensionalize extent for plotting."""
        return list([self.dimensionalize_length(self.extent_plot[i]) for i in range(4)])

class Axis:
    """ Class to handle axis labels for plotting."""
    def init_axis(self,):
        """ Initialize axis labels for plotting."""
        self.set_axis_labels()

    def set_axis_labels(self,):
        """ Set axis labels for plotting."""
        labels = ("x", "y")
        self.axis_labels = tuple(labels[i] + " (" + self.scale_str + ")" for i in range(2))

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
        
class PlotCoupledFields(Plot2DField, Extent, Axis):
    """ Class to handle coupled fields plotting."""
    @property
    def plot_flag(self,):
        return True
        
    def init_plot(self,):
        """ Initialize plot field parameters."""
        self.init_extent()
        self.init_vlims1()
        self.init_axis()
        
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
        fig, axs = self.plot_field_2d(fig=fig, axs=axs, alpha=alpha*self.get_intensity()/self.get_intensity().max(), cmap="Reds", zorder=1, norm=norms[0])

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
            fig.savefig(self.get_directory1(filename, extension=".png"), dpi=300, transparent=True)
            
        return fig, axs