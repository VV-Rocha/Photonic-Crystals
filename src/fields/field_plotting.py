from numpy import min, max, ndarray, where, nonzero, linspace, meshgrid

from functools import wraps

from typing import Tuple

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class Plotting2D:
    """Method for plotting 2D ax of """
    # % TODO: As is, the methods inside this class require an ax and figure to be given in order to plot. Add methods to plot a single figure without the requirement of giving the method an ax and figure. This would allow the plotting of a figure without having to call figure outside this class.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def plotting_intensity(self,
                           field: ndarray,
                           extent: ndarray,
                           scientific_notation_power: int | float,
                           ax,
                           fig,
                           show: bool = False,
                           cmap: str = "viridis",
                           vlims: Tuple[float, float] | None = None,
                           ):
        """Plots the intensity field in a single axis of figure.

        Args:
            field (ndarray): Numpy array with the 2d field distributions.
            extent (ndarray): Numpy array of length 4 with the form [x_min, x_max, y_min, y_max].
            scientific_notation_power (int | float): power of the scientific notation of the axis.
            ax (matplotlib axis): Figure axis to plot the image.
            fig (matplotlib figure): Matplotlib figure.
            cmap (str, optional): Colormap used in the figure. Defaults to "viridis".
            vlims (Tuple[float, float] | None, optional): Sets the minimum and maximum of the colorbar. In the case of None defaults to the colorbar between the minimum and the maximum. Defaults to None.

        Returns:
            figure: matplotlib figure
            ax: figure axis
        """
        im = ax.imshow(field,
                       extent = extent * 10**(-scientific_notation_power),
                       cmap = cmap,
                       vmin = None if (vlims is None) else vlims[0],
                       vmax = None if (vlims is None) else vlims[1],
                       )
        fig.colorbar(im, ax=ax)
                
    def plotting_phase(self,
                       field: ndarray,
                       extent: ndarray,
                       scientific_notation_power: int | float,
                       ax,
                       fig,
                       cmap: str = "bwr",
                       ):
        """Plots the phase profile of the field in a single axis of figure

        Args:
            field (ndarray): Numpy array with the 2d field distributions.
            extent (ndarray): Numpy array of length 4 with the form [x_min, x_max, y_min, y_max].
            scientific_notation_power (int | float): power of the scientific notation of the axis.
            ax (matplotlib axis): Figure axis to plot the image.
            fig (matplotlib figure): Matplotlib figure.
            cmap (str, optional): Colormap used in the figure. Defaults to "bwr".
        """
        im = ax.imshow(field,
                       extent = extent * 10**(-scientific_notation_power),
                       cmap = cmap,
                       )
        fig.colorbar(im, ax=ax)
        
def cache_import_init(init_func):
    @wraps(init_func)
    def wrapper(*args, **kwargs):
        from numpy import linspace, meshgrid
        Plotting3D._linspace = linspace
        Plotting3D._meshgrid = meshgrid
        return init_func(*args, **kwargs)
    return wrapper

class Plotting3D:
    # % TODO: Generalize this method for both fields.
    # % TODO: Controlability through input parameters.
    @cache_import_init
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_zlim(func):
        """If zlim is int or float defaults to a tuple (0, zlim).
        If zlim is None defaults to a tuple between the minimum and maximum of the intensity field.
        """
        @wraps(func)
        def wrapper(self, field, zlim = None, *args, **kwargs):
            if (type(zlim) is float) or (type(zlim) is int):
                zlim = (0, zlim)
            elif zlim is None:
                zlim = (min(field), max(field))
            return func(self, field, zlim, *args, **kwargs)
        return wrapper

    @default_zlim
    def plot_intensity_3d(self,
                          field: ndarray,
                          zlim: Tuple[float, float],
                          extent: ndarray,
                          scientific_notation_power: int | float,
                          ax,
                          fig,
                          cmap: str = "viridis",
                          xylim: ndarray | None = None, # if None extent is used else xylim is used [x_min, x_max, y_min, y_max]
                          link_zlim_vmax: bool = False,
                          rccount: Tuple[int, int] = (50, 50),
                          ):
        """Plot the 3d intensity field onto an axis.

        Args:
            field (ndarray): Numpy array with the 2d field distributions.
            zlim (Tuple[float, float]): Limits on the third axis given by the magnitude of the field.
            extent (ndarray): Numpy array of length 4 with the form [x_min, x_max, y_min, y_max].
            scientific_notation_power (int | float): power of the scientific notation of the axis.
            ax (matplotlib axis): Figure axis to plot the image.
            fig (matplotlib figure): Matplotlib figure.
            cmap (str, optional): Colormap used in the figure. Defaults to "viridis".
            xylim (ndarray | None): XY limits to be plotted. If array [x_min, x_max, y_min, y_max] in fundamental units of the system (usually meters). If None the extent limits of the Box is used. Defaults to None.
            link_zlim_vmax: (bool | None): If True the zlim maximum value is used as vmax of the plot. Defaults to False.
            rccount (Tuple[int, int] | None): Number of points to be used in plotting the 3d plot. If None is given defaults to (50, 50). Defaults to None.
        """

        
        if xylim is not None:
            # 1D coordinate vectors
            X = linspace(extent[0], extent[1], field.shape[0])
            Y = linspace(extent[2], extent[3], field.shape[1])

            # Boolean masks
            ix = (X >= xylim[0]) & (X <= xylim[1])
            iy = (Y >= xylim[2]) & (Y <= xylim[3])

            # Find the contiguous index ranges
            ix0, ix1 = nonzero(ix)[0][[0, -1]]
            iy0, iy1 = nonzero(iy)[0][[0, -1]]

            # Slice the field and grid
            field = field[ix0:ix1+1, iy0:iy1+1]
            X = X[ix0:ix1+1]#, iy0:iy1+1]
            Y = Y[iy0:iy1+1]#Y[ix0:ix1+1, iy0:iy1+1]
            
            X, Y = meshgrid(X, Y)
            
        else:
            X, Y = meshgrid(linspace(extent[0], extent[1], field.shape[0]),
                            linspace(extent[2], extent[3], field.shape[1]),
                            )    

        # axis scientific notation
        X *= 10**(-scientific_notation_power)
        Y *= 10**(-scientific_notation_power)
        
        vmin = 0.
        if link_zlim_vmax is True:
            vmax = zlim[1]
        else:
            vmax = max(field)
        
        surf = ax.plot_surface(X,
                               Y,
                               field,
                               linewidth = 0,
                               antialiased = False,
                               cmap = cmap,
                               alpha = .8,
                               rcount=rccount[0],     # draw every row
                               ccount=rccount[1],     # draw every column
                               vmin=vmin,
                               vmax=vmax,
                               )

        fig.colorbar(surf,
                     shrink=0.5,
                     aspect=10,
                     label='Intensity',
                     )

        ax.set_zlim(zlim[0], zlim[1])
        
        # Label axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Intensity')
        
        
def cache_ioff(init_func):
    @wraps(init_func)
    def wrapper(self, *args, **kwargs):
        plt.ioff()  # Turn off show
        return init_func(self, *args, **kwargs)
    return wrapper

class FieldPlotting(Plotting2D, Plotting3D):
    @cache_ioff
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def axis_labels(self, ax, scientific_notation_power):
        ax.set_xlabel(fr"$x \left(10^{{{scientific_notation_power}}} m\right)$")
        ax.set_ylabel(fr"$y \left(10^{{{scientific_notation_power}}} m\right)$")        
        return ax
    
    def plot_field(self,
                    scientific_notation_power=-3,
                    show: bool = True,
                    cmap_intensity = "viridis",
                    ):
        scientific_notation = 10**scientific_notation_power

        fig = plt.figure()

        gs = gridspec.GridSpec(nrows = 1,
                                               ncols = 2,
                                               figure = fig,
                                               )

        ax0 = fig.add_subplot(gs[0])
        ax1 = fig.add_subplot(gs[1])

        self.plotting_intensity(self.get_intensity(),
                                self.extent,
                                scientific_notation_power,
                                ax0,
                                fig,
                                cmap = cmap_intensity,
                                )
        self.plotting_phase(self.get_angle(),
                            self.extent,
                            scientific_notation_power,
                            ax1,
                            fig,
                            )
        
        ax0 = self.axis_labels(ax0, scientific_notation_power)
        ax1 = self.axis_labels(ax1, scientific_notation_power)
            
        fig.tight_layout()
        
        if show:
            fig.show()
    
    def plot_3d(self,
                   zlim: float | Tuple[float, float],
                   scientific_notation_power: float,
                   cmap_3d: str = "viridis",
                   xylim: ndarray | None = None,
                   ):
        """Plot the input and output 2d intensity fields and a 3d plot of the output intensity.

        Args:
            zlim (float | Tuple[float, float]): Limits on the third axis given by the magnitude of the field.
            scientific_notation_power (float, optional): power of the scientific notation of the axis.
            field_number (int, optional): If 0 plots the first field if 1 plots the second field. Defaults to 0.
            cmap_2d (str, optional): Colormap used in the 2d plot. Defaults to "viridis".
            cmap_3d (str, optional): Colormap used in the 3d plot. Defaults to "viridis".
        """
        # initialize figure
        fig = plt.figure()
        # set the grid
        gs = gridspec.GridSpec(nrows = 1,
                                               ncols = 1,
                                               figure = fig,
                                               )
        
        ax_3d_intensity = fig.add_subplot(gs, projection='3d')
    
        # 3d intensity field
        self.plot_intensity_3d(self.get_intensity(),
                               zlim,
                               self.extent,
                               scientific_notation_power,
                               ax_3d_intensity,
                               fig,
                               cmap = cmap_3d,
                               xylim = xylim,
                               ) 
        
        ax_3d_intensity.set_title("Output 3d Intensity")
        ax_3d_intensity.set_xlabel(fr"$x \left(10^{{{scientific_notation_power}}} m\right)$")
        ax_3d_intensity.set_ylabel(fr"$y \left(10^{{{scientific_notation_power}}} m\right)$")    
        
        fig.tight_layout()
        
        fig.show()
    
class CoupledPlotting(Plotting2D, Plotting3D):
    """Add plotting functionality to coupled field notebooks."""
    @cache_ioff
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def axis_labels(self, ax, scientific_notation_power):
        ax.set_xlabel(fr"$x \left(10^{{{scientific_notation_power}}} m\right)$")
        ax.set_ylabel(fr"$y \left(10^{{{scientific_notation_power}}} m\right)$")        
        return ax

    # % TODO: plot_fields is not the most descriptive name since we plot the intensity and not the sqrt.
    def plot_fields(self,
                    scientific_notation_power=-3,
                    show: bool = True,
                    cmap_intensity = "viridis",
                    ):
        """2x2 grid of intensity fields (top row) and phase profile (bottom row).

        Args:
            scientific_notation_power (int, optional): power of the scientific notation of the axis. Defaults to -3.
        """
        
        scientific_notation = 10**scientific_notation_power

        fig = plt.figure()

        gs = gridspec.GridSpec(nrows = 2,
                                               ncols = 2,
                                               figure = fig,
                                               )

        ax00 = fig.add_subplot(gs[0, 0])
        ax01 = fig.add_subplot(gs[0, 1])
        ax10 = fig.add_subplot(gs[1, 0])
        ax11 = fig.add_subplot(gs[1, 1])

        self.plotting_intensity(self.get_intensity(),
                                self.extent,
                                scientific_notation_power,
                                ax00,
                                fig,
                                cmap = cmap_intensity,
                                )
        self.plotting_phase(self.get_angle(),
                            self.extent,
                            scientific_notation_power,
                            ax10,
                            fig,
                            )
        self.plotting_intensity(self.get_intensity1(),
                                self.extent1,
                                scientific_notation_power,
                                ax01,
                                fig,
                                cmap = cmap_intensity,
                                )
        self.plotting_phase(self.get_angle1(),
                            self.extent1,
                            scientific_notation_power,
                            ax11,
                            fig,
                            )
        
        ax00 = self.axis_labels(ax00, scientific_notation_power)
        ax10 = self.axis_labels(ax10, scientific_notation_power)
        ax01 = self.axis_labels(ax01, scientific_notation_power)
        ax11 = self.axis_labels(ax11, scientific_notation_power)
            
        fig.tight_layout()
        
        if show:
            fig.show()
    
    # % TODO: Decorator to set a default zlim between the min and max of np.abs(field)**2.
    def plot_IO_3d(self,
                   zlim: float | Tuple[float, float],
                   scientific_notation_power: float,
                   field_number: int = 0, # if 1 print second beam
                   cmap_2d: str = "viridis",
                   cmap_3d: str = "viridis",
                   xylim: ndarray | None = None,
                   link_zlim_vmax: bool = False,
                   savefig: str | None = None,
                   ):
        """Plot the input and output 2d intensity fields and a 3d plot of the output intensity.

        Args:
            zlim (float | Tuple[float, float]): Limits on the third axis given by the magnitude of the field.
            scientific_notation_power (float, optional): power of the scientific notation of the axis.
            field_number (int, optional): If 0 plots the first field if 1 plots the second field. Defaults to 0.
            cmap_2d (str, optional): Colormap used in the 2d plot. Defaults to "viridis".
            cmap_3d (str, optional): Colormap used in the 3d plot. Defaults to "viridis".
        """
        # initialize figure
        fig = plt.figure()
        # set the grid
        gs = gridspec.GridSpec(nrows = 2,
                                               ncols = 3,
                                               figure = fig,
                                               width_ratios=[1, 1, 1],
                                               wspace = 0.4,
                                               hspace = 0.3,
                                               )
        
        ax_input_intensity = fig.add_subplot(gs[0, 0])
        ax_output_intensity = fig.add_subplot(gs[1, 0])
        ax_3d_intensity = fig.add_subplot(gs[:, 1:], projection='3d')
    
        # 2d intensity fields
        self.plotting_intensity(self.get_intensity() if (field_number == 0) else self.get_intensity1(),
                                self.extent if (field_number == 0) else self.extent1,
                                scientific_notation_power,
                                ax_input_intensity,
                                fig,
                                cmap= cmap_2d,
                                vlims = zlim if link_zlim_vmax else None,
                                )
        self.plotting_intensity(self.get_intensity() if (field_number == 0) else self.get_intensity1(),
                                self.extent if (field_number == 0) else self.extent1,
                                scientific_notation_power,
                                ax_output_intensity,
                                fig,
                                cmap = cmap_2d,
                                vlims = zlim if link_zlim_vmax else None,
                                )
        # 3d intensity field
        self.plot_intensity_3d(self.get_intensity() if (field_number == 0) else self.get_intensity1(),
                               zlim,
                               self.extent if (field_number == 0) else self.extent1,
                               scientific_notation_power,
                               ax_3d_intensity,
                               fig,
                               cmap = cmap_3d,
                               xylim = xylim,
                               link_zlim_vmax = link_zlim_vmax,
                               )
        
        ax_input_intensity.set_title("Input Beam")
        ax_input_intensity.set_xlabel(fr"$x \left(10^{{{scientific_notation_power}}} m\right)$")
        ax_input_intensity.set_ylabel(fr"$y \left(10^{{{scientific_notation_power}}} m\right)$")    
        
        ax_output_intensity.set_title("Output Beam")
        ax_output_intensity.set_xlabel(fr"$x \left(10^{{{scientific_notation_power}}} m\right)$")
        ax_output_intensity.set_ylabel(fr"$y \left(10^{{{scientific_notation_power}}} m\right)$")    
        
        ax_3d_intensity.set_title("Output 3d Intensity")
        ax_3d_intensity.set_xlabel(fr"$x \left(10^{{{scientific_notation_power}}} m\right)$")
        ax_3d_intensity.set_ylabel(fr"$y \left(10^{{{scientific_notation_power}}} m\right)$")    
        
        fig.tight_layout()
        
        fig.show()
        
        if type(savefig) is str:
            fig.savefig(savefig, dpi=300, transparent=True)