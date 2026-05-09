import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("../../../../../src/")

import core as sim
import fields

import config

    
def unpack_configs():
    configs = {
        "storage_config": config.storage_config,
        "simulation_config": config.simulation_config,
        "probe_landscape_config": config.probe_landscape_config,
        "probe_envelope_config": config.probe_envelope_config,
        "pump_landscape_config": config.pump_landscape_config,
        "pump_envelope_config": config.pump_envelope_config,
        "crystal_config": config.crystal_config,
        "solver_config": config.solver_config,
    }
    
    return configs

def initialize_objects(configs):
    storage = sim.StorageField(configs["storage_config"])
    
    mesh = sim.Mesh2D(configs["simulation_config"])
    
    beams = {
        "beam_1": fields.Gaussian(
            landscape_config = configs["probe_landscape_config"],
            envelope_config = configs["probe_envelope_config"],
        ),
        "beam_2": fields.ContinuousFeatureGaussian(
            landscape_config = configs["pump_landscape_config"],
            envelope_config = configs["pump_envelope_config"],
        )
    }
    
    media = sim.PhotorefractiveCrystal(
        configs["crystal_config"]
    )
    
    model = sim.WavevectorPhotorefractiveModel()
    
    solver = sim.SplitStepSolver(
        solver_config = configs["solver_config"]
    )
    
    objects = {
        "mesh": mesh,
        "beams": beams,
        "media": media,
        "model": model,
        "solver": solver,
        "storage": storage,
    }
    
    return objects

def clean_storage_directory(home_directory, configs):
    configs["storage_config"]["home"] = home_directory

def single_feature_solve(
    X,
    feature,
    configs,
):
    # change storage directory
    configs["storage_config"]["home"] += f"feature_{feature}/"
        
    # change feature
    configs["pump_landscape_config"]["f"] = X[feature]
    
    objects = initialize_objects(configs)
        
    simulation_box = sim.AnalogousTime2DSimulationBox(**objects)
        
    simulation_box.init(
        ref_beam="beam_1",
    )
        
    fig, axs = plt.subplots(1, 2)
    axs[0].imshow(np.abs(simulation_box.beams["beam_1"].field)**2)
    axs[1].imshow(np.abs(simulation_box.beams["beam_2"].field)**2)
    fig.savefig(".tmp.png", dpi=300)

    simulation_box.solve()

    fig, axs = plt.subplots(1, 2)
    axs[0].imshow(np.abs(simulation_box.beams["beam_1"].field)**2)
    axs[1].imshow(np.abs(simulation_box.beams["beam_2"].field)**2)
    fig.savefig(".tmp.png", dpi=300)

def main(
    X,  # array with input features [nfeatures, ndimensions]
    encoding,  # "amplitude" or "phase"
):
    configs = unpack_configs()
    
    _home_directory = configs["storage_config"]["home"] + encoding + "/"
    
    configs["pump_landscape_config"]["encoding"] = encoding
    for feature in range(len(X)):
        clean_storage_directory(_home_directory, configs)
        
        single_feature_solve(
            X,
            feature,
            configs,
        )
        
if __name__ == "__main__":
    # get problem
    x = np.linspace(0,1,64)[:, np.newaxis]
    
    encodings = [
        # "amplitude",
        "phase",
    ]
    
    for encoding in encodings:
        main(
            X = x,
            encoding = encoding,
        )