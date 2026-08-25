import numpy as np
import matplotlib.pyplot as plt

import nlse_toolbox

import config
config = {k: v for k, v in vars(config).items() if not k.startswith("_")}

def initialize_objects(configs):
    storage = nlse_toolbox.core.StorageField(configs["storage_config"])
    
    mesh = nlse_toolbox.core.Mesh2D(configs["simulation_config"])
    
    beams = {
        "beam_1": nlse_toolbox.fields.Gaussian(
            **configs["beams_config"]["beam_1"],
        ),
        "beam_2": nlse_toolbox.fields.ContinuousFeatureGaussian(
            **configs["beams_config"]["beam_2"],
        )
    }
    
    media = nlse_toolbox.core.PhotorefractiveCrystal(
        configs["crystal_config"],
    )
    
    model = nlse_toolbox.core.WavevectorPhotorefractiveModel()
    
    solver = nlse_toolbox.core.SplitStepSolver(
        solver_config = configs["solver_config"],
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
    config,
):
    # change storage directory
    config["storage_config"]["home"] += f"feature_{feature}/"
        
    # change feature
    config["beams_config"]["beam_2"]["landscape_config"]["f"] = X[feature]
    
    objects = initialize_objects(config)
        
    simulation_box = nlse_toolbox.core.AnalogousTime2DSimulationBox(**objects)
    
    simulation_box.init(
        ref_beam="beam_1",
        config_module = config,
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
    config,
):    
    _home_directory = config["storage_config"]["home"] + encoding + "/"
    
    config["beams_config"]["beam_2"]["landscape_config"]["encoding"] = encoding
    for feature in range(len(X)):
        clean_storage_directory(_home_directory, config)
        
        single_feature_solve(
            X,
            feature,
            config,
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
            config = config,
        )