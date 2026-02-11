# Imports
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("../../../../../")
import src

from src.core.boxes.simulation import SimulationBoxMethods

from src.core.engines.solvers.nls.eq_coefs.models import CoupledWavevectorPhotorefractiveModel

from src.core.engines.solvers.nls.solver_2d.coupled_solver import CoupledSplitStepSolver

from src.fields.oc_fields_2d import CoupledAmplitudeEncodingSingleFeatureGaussian2D
from src.fields.plotting.field_2d import PlotCoupledFields2D


Defocusing = False

if Defocusing:
    base_dir = "./Data/SpeckleProbe/Amplitude/Defocusing/"
else:
    base_dir = "./Data/SpeckleProbe/Amplitude/Focusing/"


inheritance = {
    PlotCoupledFields2D,
    CoupledSplitStepSolver,
    CoupledAmplitudeEncodingSingleFeatureGaussian2D,
    CoupledWavevectorPhotorefractiveModel,
}

storage_config = {"home": base_dir,
                  "store": "last",
                  "extension": ".h5",
                  "stride": 1
                  }

simulation_config = {"Nx": 2*1024,
                     "Ny": 2*1024,
                     "Nz": 128,
                     "lx": 3.*1e-3,
                     "ly": 3.*1e-3,
                     "lz": 1*20e-3,
                     "noise": .05,
                     }

crystal_config = {"n": 2.36,
                  "n1": 2.36,
                  "electro_optic_coef": 250e-12,
                  "electro_optic_coef1": 250e-12,
                  "tension": 400,
                  "Isat": 25.,
                  "alpha": 0.,
                  "alpha1": 0.,
                  "Lx": 5e-3,
                  "Ly": 5e-3,
                  "Lz": 20e-3,
                  }

beam_config = {"wavelength": 633e-9,
               "wavelength1": 532e-9,
               "c": (-1)**(Defocusing+1) * 1.,
               "c1": (-1)**(Defocusing+1) * 1.,
               }

probe_envelope_config = {
    "I": 50,
    "width": 600e-6,
    "center": (0,0),
    "exponent": 4.,
}

encoding_envelope_config = {
    "I": 50.,
    "width": 600e-6,
    "center": (0,0),
    "exponent": 4.,
}

probe_landscape_config = {}

device_config = {
    "device": 0,
    "backend": "cuda",
}

class SimulationBox(*inheritance, SimulationBoxMethods):
    def __init__(
        self,
        crystal_config,
        beam_config,
        simulation_config,
        device_config,
        modulation_config,
        storage_config,
    ):
        super().__init__(
            crystal_config = crystal_config,
            beam_config = beam_config,
            simulation_config = simulation_config,
            device_config = device_config,
            modulation_config = modulation_config,
            storage_config = storage_config,
        )
        self.store_configs(
            crystal_config,
            beam_config,
            simulation_config,
            device_config,
            modulation_config,
            storage_config,
        )

M = 64
x = np.linspace(0, 1, M)

random = np.random.uniform(-np.pi, np.pi, (simulation_config["Nx"]//8, simulation_config["Ny"]//8))
random = np.repeat(random, 8, axis=0)
random = np.repeat(random, 8, axis=1)

for i in range(64):
    storage_config = {
        "home": base_dir + f"data/feature_{i}",
        "store": "last",
        "extension": ".h5",
        "stride": 1
    }

    encoding_mask_config = {
        "feature": x[i],
        "size": 200e-6,
    }


    modulation_config = {
        "landscape_config": probe_landscape_config,
        "envelope_config": probe_envelope_config,
        "landscape1_config": encoding_mask_config,
        "envelope1_config": encoding_envelope_config,
    }

    simbox = SimulationBox(
        crystal_config = crystal_config,
        beam_config = beam_config,
        simulation_config = simulation_config,
        device_config = device_config,
        modulation_config = modulation_config,
        storage_config = storage_config,
    )

    simbox.init()

    simbox.field *= np.exp(1.j * random)
    simbox.set_scale(scale="milimeter")
    simbox.plot_2d_fields(filename="input_fields")
    
    simbox.solve()
    
    simbox.plot_2d_fields(filename="output_fields")
    print(f"Feature: {i+1}/{M}")



extent = .15e-3
extent = [(-1)**(i+1) * extent for i in range(4)]
simbox.set_extent(extent)

simbox.plot_2d_coupled(alpha=.5, filename="coupled_fields")