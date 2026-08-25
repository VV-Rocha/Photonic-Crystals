import numpy as np
import matplotlib.pyplot as plt

import nlse_toolbox

import periodic_configs
periodic_configs = {k: v for k, v in vars(periodic_configs).items() if not k.startswith("_")}
import aperiodic_configs
aperiodic_configs = {k: v for k, v in vars(aperiodic_configs).items() if not k.startswith("_")}
import plot_config


def solve(configs):
    # define storage
    storage = nlse_toolbox.core.StorageField(configs["storage_config"])

    # define mesh
    mesh = nlse_toolbox.core.Mesh2D(configs["simulation_config"])

    # define beams
    beams = {
        "beam_1": nlse_toolbox.fields.Gaussian(
            **configs["beams_config"]["beam_1"],
        ),
        "beam_2": nlse_toolbox.fields.MoireLatticeGaussian(
            **configs["beams_config"]["beam_2"],
        ),
    }

    media = nlse_toolbox.core.PhotorefractiveCrystal(configs["crystal_config"])

    model = nlse_toolbox.core.WavevectorPhotorefractiveModel()

    solver = nlse_toolbox.core.SplitStepSolver(
        solver_config = configs["solver_config"],
    )

    # define SimulationBox
    simulation_box = nlse_toolbox.core.AnalogousTime2DSimulationBox(
        mesh = mesh,
        beams = beams,
        media = media,
        model = model,
        solver = solver,
        storage = storage,
    )
    
    simulation_box.init(
        config_module = configs,
        ref_beam = "beam_1",
    )

    simulation_box.solve()
    
    return simulation_box


def plot_2d(box1, box2, plot_obj, beam="beam_1", transparent=False):
    nlse_toolbox.core.plot_2d(
        box1,
        plot_obj,
        beam = beam,
        transparent = transparent,
    )
    nlse_toolbox.core.plot_2d(
        box2,
        plot_obj,
        beam = beam,
        transparent = transparent,
    )


def plot_3d(box1, box2, plot_obj, beam="beam_1"):
    nlse_toolbox.core.plot_3d(
        box1,
        plot_obj,
        beam = beam,
    )
    nlse_toolbox.core.plot_3d(
        box2,
        plot_obj,
        beam = beam,
    )


def main():
    box_periodic = solve(periodic_configs)
    box_aperiodic = solve(aperiodic_configs)

    plot_obj = nlse_toolbox.core.PlotConfigMethods(plot_config.plot_config)
    beam = "beam_1"
    vmin = np.min([box_periodic.beams[beam].get_intensity(), box_aperiodic.beams[beam].get_intensity()])
    vmax = np.max([box_periodic.beams[beam].get_intensity(), box_aperiodic.beams[beam].get_intensity()])
    plot_obj.set_vlims(vmin, vmax)
    
    plot_obj.set_extent(plot_config.plot_config["extent"])
    plot_obj.set_cmap("rainbow")
    plot_obj.set_axis_labels(
        xaxis_label = "x",
        yaxis_label = "y",
        zaxis_label = "I (mW)",
        units=True,
    )
    plot_obj.set_colorbar_label("I (mW)")
    plot_obj.set_zscale()

    plot_2d(
        box_periodic,
        box_aperiodic,
        plot_obj = plot_obj,
        beam = beam,
    )
    
    plot_obj.set_alpha(1.)
    plot_obj.set_cmap("turbo")
    
    plot_3d(
        box_periodic,
        box_aperiodic,
        plot_obj = plot_obj,
        beam = "beam_1",
    )


if __name__ == "__main__":
    main()