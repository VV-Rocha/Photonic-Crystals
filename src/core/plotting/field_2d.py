import numpy as np
import matplotlib.pyplot as plt

from .plot.plot_2d import _plot2d


def plot_2d(
    box,
    plot_config,
    beam = "beam_1",
    transparent=False,
):
    fig, axs = plt.subplots(1, 2)
    
    _plot2d(
        xx = box.mesh.xx * plot_config.units_factor,
        yy = box.mesh.yy * plot_config.units_factor,
        field = box.beams[beam].get_intensity(),
        extent = plot_config.extent,
        vlims = plot_config.vlims,
        fig = fig,
        axs = axs[0],
        cmap = plot_config.cmap,
        axis_labels = plot_config.axis_labels(),
        colorbar_label = plot_config.colorbar_label,
        zscale = plot_config.zscale,
    )
    
    _plot2d(
        xx = box.mesh.xx * plot_config.units_factor,
        yy = box.mesh.yy * plot_config.units_factor,
        field = box.beams[beam].get_angle(),
        extent = plot_config.extent,
        vlims = [-np.pi, np.pi],
        fig = fig,
        axs = axs[1],
        cmap = "coolwarm",
        axis_labels = plot_config.axis_labels(),
        colorbar_label = r"$\phi\, \left(rads\right)$",
        zscale = plot_config.zscale,
    )

    fig.tight_layout()
    fig.savefig(
        box.storage.get_directory("Figure/") + beam + "_2d.png", dpi=300, transparent=transparent,
    )