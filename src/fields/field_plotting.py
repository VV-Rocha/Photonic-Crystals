from numpy import min, max, ndarray

from functools import wraps

from typing import Tuple

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
                           ):
        """Plots the intensity field in a single axis of figure.

        Args:
            field (ndarray): Numpy array with the 2d field distributions.
            extent (ndarray): Numpy array of length 4 with the form [x_min, x_max, y_min, y_max].
            scientific_notation_power (int | float): power of the scientific notation of the axis.
            ax (matplotlib axis): Figure axis to plot the image.
            fig (matplotlib figure): Matplotlib figure.
            cmap (str, optional): Colormap used in the figure. Defaults to "viridis".

        Returns:
            figure: matplotlib figure
            ax: figure axis
        """
        im = ax.imshow(self.__class__._abs(field)**2,
                  extent = extent * 10**(-scientific_notation_power),
                  cmap = cmap,
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
        im = ax.imshow(self.__class__._angle(field),
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
        from matplotlib.pyplot import figure
        Plotting3D._figure = figure
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
                zlim = (min(self.__class__._abs(field)**2), max(self.__class__._abs(field)**2))
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
        """
        
        X, Y = self.__class__._meshgrid(self.__class__._linspace(extent[0], extent[1], field.shape[0]),
                                       self.__class__._linspace(extent[2], extent[3], field.shape[1]))
        
        # axis scientific notation
        X *= 10**(-scientific_notation_power)
        Y *= 10**(-scientific_notation_power)

        surf = ax.plot_surface(X,
                               Y,
                               self.__class__._abs(field)**2,
                               linewidth = 0,
                               antialiased = False,
                               cmap = cmap,
                               alpha = .8
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
        
        
def cache_import_CoupledPlotting(init_func):
    @wraps(init_func)
    def wrapper(self, *args, **kwargs):
        from numpy import angle
        CoupledPlotting._angle = angle
        from numpy import abs
        CoupledPlotting._abs = abs
        import matplotlib.pyplot as plt
        plt.ioff()  # Turn off show
        CoupledPlotting._figure = plt.figure
        CoupledPlotting._subplots = plt.subplots
        import matplotlib.gridspec as gridspec
        CoupledPlotting._gridspec = gridspec
        from matplotlib.axes import Axes
        CoupledPlotting._Axes = Axes
        return init_func(self, *args, **kwargs)
    return wrapper

class CoupledPlotting(Plotting2D, Plotting3D):
    """Add plotting functionality to coupled field notebooks."""
    @cache_import_CoupledPlotting
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

        fig = self.__class__._figure()

        gs = self.__class__._gridspec.GridSpec(nrows = 2,
                                               ncols = 2,
                                               figure = fig,
                                               )

        ax00 = fig.add_subplot(gs[0, 0])
        ax01 = fig.add_subplot(gs[0, 1])
        ax10 = fig.add_subplot(gs[1, 0])
        ax11 = fig.add_subplot(gs[1, 1])

        self.plotting_intensity(self.field,
                                self.extent,
                                scientific_notation_power,
                                ax00,
                                fig,
                                cmap = cmap_intensity,
                                )
        self.plotting_phase(self.field,
                            self.extent,
                            scientific_notation_power,
                            ax10,
                            fig,
                            )
        self.plotting_intensity(self.field1,
                                self.extent1,
                                scientific_notation_power,
                                ax01,
                                fig,
                                cmap = cmap_intensity,
                                )
        self.plotting_phase(self.field1,
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
        fig = self.__class__._figure()
        # set the grid
        gs = self.__class__._gridspec.GridSpec(nrows = 2,
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
        self.plotting_intensity(self.input_field if (field_number == 0) else self.input_field1,
                                self.extent if (field_number == 0) else self.extent1,
                                scientific_notation_power,
                                ax_input_intensity,
                                fig,
                                cmap= cmap_2d,
                                )
        self.plotting_intensity(self.field if (field_number == 0) else self.field1,
                                self.extent if (field_number == 0) else self.extent1,
                                scientific_notation_power,
                                ax_output_intensity,
                                fig,
                                cmap = cmap_2d,
                                )
        # 3d intensity field
        self.plot_intensity_3d(self.field if (field_number == 0) else self.field1,
                               zlim,
                               self.extent if (field_number == 0) else self.extent1,
                               scientific_notation_power,
                               ax_3d_intensity,
                               fig,
                               cmap = cmap_3d,
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