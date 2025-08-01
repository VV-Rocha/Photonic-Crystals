# Imports
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("../../../../")
import src

from src.core.control import AfPrecisionControl
from src.core.control import CoupledStorageConfig

from src.core.dimensionless import WavevectorScale, Dimensional, LatticeScale

from src.core.media import TwoBeamPhotorefractiveCrystal
from src.core.eq_coefs import CoupledPhotorefractiveCoefs
from src.core.mesh import Mesh2D
from src.core.beams import TwoBeams

from src.fields import NotebookCoupledFields
from src.fields.modulation.moire_lattice import MoireLatticeGaussianCoupledBeamConfig

from src.fields.landscapes.lattices.single_lattices import planewave_lattice
from src.simulators.nls_2d.split_step import CoupledSplitStep

from src.simulators import Solver, SimulationBox

import h5py
import pickle

periodic_storage_config = {"home": "./Data/Periodic/",
                  "store": "last",
                  "extension": ".h5",
                  "object": CoupledStorageConfig,
                  }

aperiodic_storage_config = {"home": "./Data/Aperiodic/",
                            "store": "last",
                            "extension": ".h5",
                            "object": CoupledStorageConfig,
                            }

simulation_config = {"Nx": 2*1024,
                     "Ny": 2*1024,
                     "Nz": 1*200,
                     "lx": 1.5*1e-3,
                     "ly": 1.5*1e-3,
                     "lz": 1*20e-3,
                     "noise": .05,
                     "adim_method": WavevectorScale,
                     "coefs_object": CoupledPhotorefractiveCoefs,
                     "fields": NotebookCoupledFields,
                     "mesh_method": Mesh2D,
                     "solver": Solver,
                     "solver_engine": CoupledSplitStep(),
                     "device": 0,
                     "backend": "0",#"cuda",
                     }

crystal_config = {"n": 2.36,
                  "n1": 2.36,
                  "electro_optic_coef":250e-12,
                  "electro_optic_coef1": 250e-12,
                  "tension": 400,
                  "Isat": 5,
                  "alpha": 0.,
                  "alpha1": 0.,
                  "Lx": 5e-3,
                  "Ly": 5e-3,
                  "Lz": 20e-3,
                  "object": TwoBeamPhotorefractiveCrystal,
                  }

beam_config = {"wavelength": 633e-9,
               "wavelength1": 532e-9,
               "c": -1.,
               "c1": -.1,
               "object": TwoBeams,
               }

state_modulation_config = {"I": .3,
                           "waist": 11.5e-6,
                           "center": (0,0),
                           "exponent": 1.,
                           }

lattice_modulation_config = {"I": (crystal_config["Isat"])*4.,
                           "waist": 600e-6,
                           "center": (0,0),
                           "exponent": 4.,
                           }

state_structure_config = {"angle": None,
                          "a": None,
                          "p": None,
                          "lattice_method": None,}

periodic_lattice_config = {"angle": np.atan(3/4),
                           "angle1": None,
                           "a": np.pi*.25*27e-6,
                           "a1": None,
                           "p": 1.,
                           "p1": 1.,
                           "lattice_method": planewave_lattice,
                           "lattice1_method": planewave_lattice,
                           }

periodic_lattice_config["eta"] = 45*np.pi/180 + .5*(.5*np.pi - periodic_lattice_config["angle"])
periodic_lattice_config["angle"] += periodic_lattice_config["eta"]
periodic_lattice_config["angle1"] = periodic_lattice_config["eta"]
periodic_lattice_config["a1"] = periodic_lattice_config["a"]

periodic_modulation_config = {
    "structure": state_structure_config,
    "modulation": state_modulation_config,
    "structure1": periodic_lattice_config,
    "modulation1": lattice_modulation_config,
    "object": MoireLatticeGaussianCoupledBeamConfig,
}

aperiodic_lattice_config = {"angle": np.atan(1/np.sqrt(3)),
                            "angle1": None,
                            "a": np.pi*.25*27e-6,
                            "a1": None,
                            "p": 1.,
                            "p1": 1.,
                            "lattice_method": planewave_lattice,
                            "lattice1_method": planewave_lattice,
                           }
aperiodic_lattice_config["eta"] = 45*np.pi/180 + .5*(.5*np.pi - aperiodic_lattice_config["angle"])
aperiodic_lattice_config["angle"] += aperiodic_lattice_config["eta"]
aperiodic_lattice_config["angle1"] = aperiodic_lattice_config["eta"] 
aperiodic_lattice_config["a1"] = aperiodic_lattice_config["a"]

aperiodic_modulation_config = {
    "structure": state_structure_config,
    "modulation": state_modulation_config,
    "structure1": aperiodic_lattice_config,
    "modulation1": lattice_modulation_config,
    "object": MoireLatticeGaussianCoupledBeamConfig,
}

precision_config = {"precision": "double",
                    "object": AfPrecisionControl,
                    }

periodic_SimBox = SimulationBox(structure_config=periodic_lattice_config,
                                modulation_config=periodic_modulation_config,
                                medium_config=crystal_config,
                                beam_config=beam_config,
                                simulation_config=simulation_config,
                                storage_config=periodic_storage_config,
                                precision_config=precision_config)

aperiodic_SimBox = SimulationBox(structure_config=aperiodic_lattice_config,
                                modulation_config=aperiodic_modulation_config,
                                medium_config=crystal_config,
                                beam_config=beam_config,
                                simulation_config=simulation_config,
                                storage_config=aperiodic_storage_config,
                                precision_config=precision_config)

periodic_SimBox.solve()
aperiodic_SimBox.solve()

tlim = .5*.25e-3
zlim = (0., np.max((np.max(np.abs(aperiodic_SimBox.input_fields.field)**2), np.max(np.abs(periodic_SimBox.input_fields.field)**2))))
# zlim = (0, 0.04)
periodic_SimBox.input_fields.plot_IO_3d(zlim=zlim, scientific_notation_power=-3, xylim=[-tlim, tlim, -tlim, tlim], link_zlim_vmax=True, cmap_2d="jet", cmap_3d="jet", savefig="./periodic atan(3_4) p2_1.png",)
aperiodic_SimBox.input_fields.plot_IO_3d(zlim=zlim, scientific_notation_power=-3, xylim=[-tlim, tlim, -tlim, tlim], link_zlim_vmax=True, cmap_2d="jet", cmap_3d="jet", savefig="./aperiodic atan(1_sqrt(3)) p2_1.png")

with h5py.File(periodic_storage_config["home"] + 'periodic_config.h5', "w") as h:
    h.create_dataset("simulation_config", data=np.void(pickle.dumps(simulation_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("crystal_config", data=np.void(pickle.dumps(crystal_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("beam_config", data=np.void(pickle.dumps(beam_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("modulation_config", data=np.void(pickle.dumps(modulation_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("precision_config", data=np.void(pickle.dumps(precision_config, protocol=pickle.HIGHEST_PROTOCOL)))
    
    h.create_dataset("periodic_storage_config", data=np.void(pickle.dumps(periodic_storage_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("periodic_lattice_config", data=np.void(pickle.dumps(periodic_lattice_config, protocol=pickle.HIGHEST_PROTOCOL)))
    
with h5py.File(aperiodic_storage_config["home"] + 'aperiodic_config.h5', "w") as h:
    h.create_dataset("simulation_config", data=np.void(pickle.dumps(simulation_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("crystal_config", data=np.void(pickle.dumps(crystal_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("beam_config", data=np.void(pickle.dumps(beam_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("modulation_config", data=np.void(pickle.dumps(modulation_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("precision_config", data=np.void(pickle.dumps(precision_config, protocol=pickle.HIGHEST_PROTOCOL)))
    
    h.create_dataset("aperiodic_storage_config", data=np.void(pickle.dumps(aperiodic_storage_config, protocol=pickle.HIGHEST_PROTOCOL)))
    h.create_dataset("aperiodic_lattice_config", data=np.void(pickle.dumps(aperiodic_lattice_config, protocol=pickle.HIGHEST_PROTOCOL)))