# Imports
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # registers the 3D projection

import sys
sys.path.append("../../../../")
import src

from src.core.boxes.simulation import SimulationBoxMethods

from src.core.engines.solvers.nls.eq_coefs.models import CoupledWavevectorPhotorefractiveModel

from src.core.engines.solvers.nls.solver_2d.coupled_solver import CoupledSplitStepSolver

from src.fields.fields_2d import SecondMoireLatticeGaussian2D
from src.fields.plotting.field_2d import PlotCoupledFields2D
from src.fields.plotting.field_3d import PlotCoupledFields3D


inheritance = {
    PlotCoupledFields3D,
    PlotCoupledFields2D,
    CoupledSplitStepSolver,
    SecondMoireLatticeGaussian2D,
    CoupledWavevectorPhotorefractiveModel,
}

periodic_storage_config = {"home": "./Data/Periodic/",
                  "store": "stride",
                  "extension": ".h5",
                  "stride": 1
                  }

aperiodic_storage_config = {"home": "./Data/Aperiodic/",
                            "store": "stride",
                            "extension": ".h5",
                            "stride": 1,
                            }

free_storage_config = {"home": "./Data/Free/",
                            "store": "stride",
                            "extension": ".h5",
                            "stride": 1,
                            }

simulation_config = {"Nx": 2*1024,
                     "Ny": 2*1024,
                     "Nz": 1*200,
                     "lx": 1.5*1e-3,
                     "ly": 1.5*1e-3,
                     "lz": 1*20e-3,
                     "noise": .05,
                     "device": 0,
                     "backend": "cuda",
                     }

crystal_config = {"n": 2.36,
                  "n1": 2.36,
                  "electro_optic_coef":250e-12,
                  "electro_optic_coef1": 250e-12,
                  "tension": 400,
                  "Isat": 3.75,
                  "alpha": 0.,
                  "alpha1": 0.,
                  "Lx": 5e-3,
                  "Ly": 5e-3,
                  "Lz": 20e-3,
                  }

beam_config = {"wavelength": 633e-9,
               "wavelength1": 532e-9,
               "c": -1.,
               "c1": -.1,
               }

state_modulation_config = {"I": .3,
                           "width": 11.5e-6,
                           "center": (0,0),
                           "exponent": 1.,
                           }

lattice_modulation_config = {"I": (crystal_config["Isat"])*16.,
                           "width": 700e-6,
                           "center": (0,0),
                           "exponent": 4.,
                           }

state_structure_config = {
    "angle": None,
    "a": None,
    "p": None,
}

periodic_lattice_config = {
    "angle": np.atan(3/4),
    "angle1": None,
    "a": .25*np.pi*27e-6,
    "a1": None,
    "p": 1.,
    "p1": 1.,
}

periodic_lattice_config["eta"] = 45*np.pi/180 + .5*(.5*np.pi - periodic_lattice_config["angle"])
periodic_lattice_config["angle"] += periodic_lattice_config["eta"]
periodic_lattice_config["angle1"] = periodic_lattice_config["eta"]
periodic_lattice_config["a1"] = periodic_lattice_config["a"]

periodic_modulation_config = {
    "landscape_config": state_structure_config,
    "envelope_config": state_modulation_config,
    "landscape1_config": periodic_lattice_config,
    "envelope1_config": lattice_modulation_config,
}

aperiodic_lattice_config = {"angle": np.atan(1/np.sqrt(3)),
                            "angle1": None,
                            "a": .25*np.pi*27e-6,
                            "a1": None,
                            "p": 1.,
                            "p1": 1.,
                           }
aperiodic_lattice_config["eta"] = 45*np.pi/180 + .5*(.5*np.pi - aperiodic_lattice_config["angle"])
aperiodic_lattice_config["angle"] += aperiodic_lattice_config["eta"]
aperiodic_lattice_config["angle1"] = aperiodic_lattice_config["eta"] 
aperiodic_lattice_config["a1"] = aperiodic_lattice_config["a"]

aperiodic_modulation_config = {
    "landscape_config": state_structure_config,
    "envelope_config": state_modulation_config,
    "landscape1_config": aperiodic_lattice_config,
    "envelope1_config": lattice_modulation_config,
}

device_config = {
    "device": 0,
    "backend": "0",#"cuda",
}

free_modulation_config = {"I": 0.,
                           "width": 700e-6,
                           "center": (0,0),
                           "exponent": 4.,
                           }

free_modulation_config = {
    "landscape_config": state_structure_config,
    "envelope_config": state_modulation_config,
    "landscape1_config": aperiodic_lattice_config,
    "envelope1_config": free_modulation_config,
}

plot3d_config = {
    "rcount": (256, 256)
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
        plot3d_config,
    ):
        super().__init__(
            crystal_config = crystal_config,
            beam_config = beam_config,
            simulation_config = simulation_config,
            device_config = device_config,
            modulation_config = modulation_config,
            storage_config = storage_config,
            plot3d_config = plot3d_config,
        )
        self.store_configs(
            crystal_config,
            beam_config,
            simulation_config,
            device_config,
            modulation_config,
            storage_config,
        )

periodic_SimBox = SimulationBox(
    crystal_config = crystal_config,
    beam_config = beam_config,
    simulation_config = simulation_config,
    device_config = device_config,
    modulation_config = periodic_modulation_config,
    storage_config = periodic_storage_config,
    plot3d_config = plot3d_config,
)
print(">>> Done!")
aperiodic_SimBox = SimulationBox(
    crystal_config = crystal_config,
    beam_config = beam_config,
    simulation_config = simulation_config,
    device_config = device_config,
    modulation_config = aperiodic_modulation_config,
    storage_config = aperiodic_storage_config,
    plot3d_config = plot3d_config,
)
print(">>> Done!")
free_SimBox = SimulationBox(
    crystal_config = crystal_config,
    beam_config = beam_config,
    simulation_config = simulation_config,
    device_config = device_config,
    modulation_config = free_modulation_config,
    storage_config = free_storage_config,
    plot3d_config = plot3d_config,
)
print(">>> Done!")
periodic_SimBox.init()
aperiodic_SimBox.init()
free_SimBox.init()

fig, axs = plt.subplots(2,2)
axs[0,0].imshow(np.abs(periodic_SimBox.field)**2)
axs[0,1].imshow(np.angle(periodic_SimBox.field))
axs[1,0].imshow(np.abs(periodic_SimBox.field1)**2)
axs[1,1].imshow(np.angle(periodic_SimBox.field1))
fig.savefig("./input_fields.png", dpi=300)

periodic_SimBox.solve()
aperiodic_SimBox.solve()

fig, axs = plt.subplots(2,2)
axs[0,0].imshow(np.abs(periodic_SimBox.field)**2)
axs[0,1].imshow(np.angle(periodic_SimBox.field))
axs[1,0].imshow(np.abs(periodic_SimBox.field1)**2)
axs[1,1].imshow(np.angle(periodic_SimBox.field1))
fig.savefig("./periodic_output.png", dpi=300)

fig, axs = plt.subplots(2,2)
axs[0,0].imshow(np.abs(aperiodic_SimBox.field)**2)
axs[0,1].imshow(np.angle(aperiodic_SimBox.field))
axs[1,0].imshow(np.abs(aperiodic_SimBox.field1)**2)
axs[1,1].imshow(np.angle(aperiodic_SimBox.field1))
fig.savefig("./aperiodic_output.png", dpi=300)

vmin = np.min([np.abs(periodic_SimBox.field)**2, np.abs(aperiodic_SimBox.field)**2])
vmax = np.max([np.abs(periodic_SimBox.field)**2, np.abs(aperiodic_SimBox.field)**2])


vmin = np.min([
    periodic_SimBox.get_intensity(),
    aperiodic_SimBox.get_intensity(),
    # free_SimBox.get_intensity()
])
vmax = np.max([
    periodic_SimBox.get_intensity(),
    aperiodic_SimBox.get_intensity(),
    # free_SimBox.get_intensity()
])
periodic_SimBox.set_vlims(vmin, vmax)
aperiodic_SimBox.set_vlims(vmin, vmax)
free_SimBox.set_vlims(vmin, vmax)

vmin1 = np.min([
    periodic_SimBox.get_intensity1(),
    aperiodic_SimBox.get_intensity1(),
    # free_SimBox.get_intensity1()
])
vmax1 = np.max([
    periodic_SimBox.get_intensity1(),
    aperiodic_SimBox.get_intensity1(),
    # free_SimBox.get_intensity1()
])
periodic_SimBox.set_vlims1(vmin1, vmax1)
aperiodic_SimBox.set_vlims1(vmin1, vmax1)
free_SimBox.set_vlims1(vmin1, vmax1)

periodic_SimBox.set_scale(scale="milimeter")
aperiodic_SimBox.set_scale(scale="milimeter")
free_SimBox.set_scale(scale="milimeter")

extent = .15e-3
extent = [(-1)**(i+1) *extent for i in range(4)]
periodic_SimBox.set_extent(extent)
aperiodic_SimBox.set_extent(extent)
free_SimBox.set_extent(extent)


periodic_SimBox.plot_2d_coupled(alpha=.5, filename="periodic_coupled_fields")
aperiodic_SimBox.plot_2d_coupled(alpha=.5, filename="aperiodic_coupled_fields")
free_SimBox.plot_2d_coupled(alpha=.5, filename="free_coupled_fields")

# periodic_SimBox.set_vlims(vmin, vmax)
# aperiodic_SimBox.set_vlims(vmin, vmax)
# free_SimBox.set_vlims(vmin, vmax)

periodic_SimBox.plot3d_field(filename="periodic_3d")
aperiodic_SimBox.plot3d_field(filename="aperiodic_3d")
free_SimBox.plot3d_field(filename="free_3d")