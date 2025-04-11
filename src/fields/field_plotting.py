from functools import wraps

class Plotting2D:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def if_subplot(plotting_function):
        @wraps(plotting_function)
        
        def wrapper(self, ax, *args, **kwargs):
            if isinstance(ax, self.__class__._Axes):
                return plotting_function(self, ax, *args, **kwargs)
            
            fig = self.__class__._figure()
            gs = self.__class__._gridspec.GridSpec(nrows = 1,
                                                ncols = 1,
                                                figure = fig,
                                                )
            ax = fig.add_subplot(gs[0,0])  # % TODO: Do I need to use the [0,0] indices.
            return plotting_function(self, ax, *args, **kwargs)
            
        return wrapper

    @if_subplot
    def plotting_intensity(self,
                           ax,
                           fig,
                           field,
                           extent,
                           scientific_notation_power,
                           show: bool = False,
                           get_figax: bool = True,
                           ):
        ax.imshow(self.__class__._abs(field)**2,
                  extent = extent * 10**(-scientific_notation_power),
                  )
        if get_figax:
            return fig, ax
        
    @if_subplot
    def plotting_phase(self,
                           ax,
                           fig,
                           field,
                           extent,
                           scientific_notation_power,
                           show: bool = False,
                           get_figax: bool = True,
                           ):
        ax.imshow(self.__class__._angle(field),
                  extent = extent * 10**(-scientific_notation_power),
                  )
        if get_figax:
            return fig, ax
    
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

    def plot_field_3d(self, ax, scientific_notation_power):
        X, Y = self.__class__._meshgrid(self.__class__._linspace(self.extent[0], self.extent[1], self.field.shape[0]),
                                       self.__class__._linspace(self.extent[2], self.extent[3], self.field.shape[1]))

        X *= 10**(-scientific_notation_power)
        Y *= 10**(-scientific_notation_power)

        surf = ax.plot_surface(X,
                               Y,
                               self.__class__._abs(self.field)**2,
                               linewidth=0,
                               antialiased=False,
                               cmap="viridis",
                               alpha=.8
                               )
        
        ax.set_zlim(0, 1)# 0.03)
        
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
    """Add plotting functionality."""
    @cache_import_CoupledPlotting
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def axis_labels(self, ax, scientific_notation_power):
        ax.set_xlabel(fr"$x \left(10^{{{scientific_notation_power}}} m\right)$")
        ax.set_ylabel(fr"$y \left(10^{{{scientific_notation_power}}} m\right)$")        
        return ax

    def plot_fields(self,
                    scientific_notation_power=-3,
                    show: bool = True,
                    ):
        """2x2 grid of intensity fields (top row) and phase profile (bottom row).

        Args:
            scientific_notation_power (int, optional): _description_. Defaults to -3.
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

        self.plotting_intensity(ax00,
                                fig,
                                self.field,
                                self.extent,
                                scientific_notation_power,
                                show = False,
                                get_figax = True,
                                )
        self.plotting_phase(ax10,
                            fig,
                            self.field,
                            self.extent,
                            scientific_notation_power,
                            show = False,
                            get_figax = True,
                            )
        self.plotting_intensity(ax01,
                                fig,
                                self.field1,
                                self.extent1,
                                scientific_notation_power,
                                show = False,
                                get_figax = True,
                                )
        self.plotting_phase(ax11,
                            fig,
                            self.field1,
                            self.extent1,
                            scientific_notation_power,
                            show = False,
                            get_figax = True,
                            )
        
        ax00 = self.axis_labels(ax00, scientific_notation_power)
        ax10 = self.axis_labels(ax10, scientific_notation_power)
        ax01 = self.axis_labels(ax01, scientific_notation_power)
        ax11 = self.axis_labels(ax11, scientific_notation_power)
            
        fig.tight_layout()
        
        if show:
            fig.show()
    
    def plot_input_output_3d(self, scientific_notation_power=-3, show: bool = True):
        fig = self.__class__._figure()
        
        gs = self.__class__._gridspec.GridSpec(nrows = 2,
                                               ncols = 3,
                                               figure = fig,
                                               width_ratios=[1, 1, 1],  # Make the right column (3D plot) twice as wide
                                               wspace=0.4,           # Horizontal spacing
                                               hspace=0.3            # Vertical spacing
                                               )
        
        ax_input_intensity = fig.add_subplot(gs[0, 0])
        ax_output_intensity = fig.add_subplot(gs[1, 0])
        ax_3d_intensity = fig.add_subplot(gs[:, 1:], projection='3d')
    
        ## 2d intensity fields
        self.plotting_intensity(ax_input_intensity,
                                fig,
                                self.input_field,
                                self.extent,
                                scientific_notation_power,
                                show = False,
                                get_figax = True,
                                )
        self.plotting_intensity(ax_output_intensity,
                                fig,
                                self.field,
                                self.extent,
                                scientific_notation_power,
                                show = False,
                                get_figax = True,
                                )
        
        self.plot_field_3d(ax_3d_intensity, scientific_notation_power)
        
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
        
        if show:
            fig.show()