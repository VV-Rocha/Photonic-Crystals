import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("../../../../src/")

import core as sim
import fields

import periodic_configs
import aperiodic_configs
import plot_config


def solve(configs):
    # define storage
    storage = sim.StorageField(configs.storage_config)

    # define mesh
    mesh = sim.Mesh2D(configs.simulation_config)

    # define beams
    beams = {
        "beam_1": fields.Gaussian(
            landscape_config = configs.state_structure_config,
            envelope_config = configs.state_modulation_config,
        ),
        "beam_2": fields.MoireLatticeGaussian(
            landscape_config = configs.periodic_lattice_config,
            envelope_config = configs.lattice_modulation_config,
        ),
    }

    media = sim.PhotorefractiveCrystal(configs.crystal_config)

    model = sim.WavevectorPhotorefractiveModel()

    solver = sim.SplitStepSolver(
        solver_config = configs.solver_config,
    )

    # define SimulationBox
    simulation_box = sim.AnalogousTime2DSimulationBox(
        mesh = mesh,
        beams = beams,
        media = media,
        model = model,
        solver = solver,
        storage = storage,
    )
    
    simulation_box.init(
        ref_beam = "beam_1",
    )

    simulation_box.solve()
    
    return simulation_box


def plot_2d(box1, box2, plot_obj, beam="beam_1", transparent=False):
    sim.plot_2d(
        box1,
        plot_obj,
        beam = beam,
        transparent = transparent,
    )
    sim.plot_2d(
        box2,
        plot_obj,
        beam = beam,
        transparent = transparent,
    )


def plot_3d(box1, box2, plot_obj, beam="beam_1"):
    sim.plot_3d(
        box1,
        plot_obj,
        beam = beam,
    )
    sim.plot_3d(
        box2,
        plot_obj,
        beam = beam,
    )


def main():
    box_periodic = solve(periodic_configs)
    box_aperiodic = solve(aperiodic_configs)

    plot_obj = sim.PlotConfigMethods(plot_config.plot_config)
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