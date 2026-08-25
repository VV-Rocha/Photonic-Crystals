import numpy as np
import matplotlib.pyplot as plt

from .plot.plot_3d import _plot_region_3d


def plot_3d(
    box,
    plot_config,
    beam = "beam_1",
    transparent = False,
):
    fig, axs = plt.subplots(1)
    
    _plot_region_3d(
        xx = box.mesh.xx * plot_config.units_factor,
        yy = box.mesh.yy * plot_config.units_factor,
        z = box.beams[beam].get_intensity(),
        fig = fig,
        axs = axs,
        cmap = plot_config.cmap,
        axis_labels = plot_config.axis_labels(),
        colorbar_label = plot_config.colorbar_label,
        vlims = plot_config.vlims,
        alpha = plot_config.alpha,
        extent = plot_config.extent,
    )
    
    fig.tight_layout()
    fig.savefig(
        box.storage.get_directory("Figure/") + beam + "_3d.png", dpi=300, transparent=transparent,
    )