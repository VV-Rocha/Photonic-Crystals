import numpy as np
from typing import Tuple

from .decorators import dimensions_length

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
    
    # @dimensions_length
    def set_extent(
        self,
        extent_plot: float | list = None,
        scale: str | None = None,
    ):
        """ Set extent for plotting.

        Args:
            extent_plot (float | list): Extent to be set.
            scale (str | None, optional): Scale type. Options: "micrometer", "milimeter", "meter", "adimensional". Defaults to None.
        """
        if extent_plot is None:
            extent_plot = self.extent
        if scale != None:
            self.set_scale(scale)
        self.extent_plot = extent_plot
        self.extent_plot = self.adimensionalize_extent()
        self.set_window()

    def scaled_extent_plot(self,):
        return [self.extent_plot[i]*self.scale_factor for i in range(4)]

    def dimensionalize_extent(self,):
        """ Dimensionalize extent for plotting."""
        return list([self.dimensionalize_length(self.extent_plot[i]) for i in range(4)])

    def adimensionalize_extent(self,):
        """ Adimensionalize extent for plotting."""
        return list([self.adimensionalize_length(self.extent_plot[i]) for i in range(4)])

class Axis:
    """ Class to handle axis labels for plotting."""
    def init_axis(self,):
        """ Initialize axis labels for plotting."""
        self.set_axis_labels()

    def set_axis_labels(self,):
        """ Set axis labels for plotting."""
        labels = ("x", "y")
        self.axis_labels = tuple(labels[i] + " (" + self.scale_str + ")" for i in range(2))