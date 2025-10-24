from functools import wraps

import matplotlib.pyplot as plt

def dimensions_length(func):
    @wraps(func)
    def wrapper(self, extent_plot, *args, **kwargs):
        if type(extent_plot) is list:
            extent_plot = [self.adimensionalize_length(extent_plot[i]) for i in range(len(extent_plot))]
        else:
            extent_plot = self.adimensionalize_length(extent_plot)
            extent_plot = [(-1)**(i+1) * extent_plot for i in range(4)]
        return func(self, extent_plot, *args, **kwargs)
    return wrapper

def construct_figure(func):
    @wraps(func)
    def wrapper(intensity, extent, vlims, fig=None, axs=None, alpha=1., cmap=None, axis_labels=("x","y"), colorbar_label=None, zorder=None, norm=None, scale=None,):
        if (fig is None) and (axs is None):
            fig, axs = plt.subplots(1)
        fig, axs = func(intensity, extent, vlims, fig, axs, alpha, cmap, axis_labels, colorbar_label, zorder, norm)
        return fig, axs
    return wrapper

def self_scale(func):
    @wraps(func)
    def wrapper(self, extent, scale_factor):
        if scale_factor == None:
            scale_factor = self.scale_factor
        return func(self, extent, scale_factor)
    return wrapper