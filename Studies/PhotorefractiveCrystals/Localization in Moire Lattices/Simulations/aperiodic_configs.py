import numpy as np


storage_config = {
    "home": "./Data/Aperiodic/",
    "store": "last",
    "extension": ".h5",
    "stride": 1
}

solver_config = {
    "device": 0,
    "backend": "0",#"cuda",
}

simulation_config = {
    "Nx": 2*1024,
    "Ny": 2*1024,
    "Nz": 1*200,
    "lx": 1.5*1e-3,
    "ly": 1.5*1e-3,
    "lz": 1*20e-3,
    "noise": .05,
    "device": 0,
    "backend": "cuda",
}

periodic_lattice_config = {
    "angle": np.atan(1/np.sqrt(3)),
    "angle1": 0.,
    "a": .25*np.pi*27e-6,
    "a1": .25*np.pi*27e-6,
    "p": 1.,
    "p1": 1.,
}

state_structure_config = None

state_modulation_config = {
    "I": .3,
    "width": 11.5e-6,
    "center": (0,0),
    "exponent": 1.,
}

crystal_config = {
    "shared": {
        "Isat": 3.75,
        "tension": 400,
        "Lx": 5e-3,
        "Ly": 5e-3,
        "Lz": 20e-3,
    },
    "beam_properties": {
        "beam_1": {
            "wavelength": 633e-9,
            "n": 2.36,
            "electro_optic_coef":250e-12,
            "alpha": 0.,
            "c": -1.,
        },
        "beam_2": {
            "wavelength": 532e-9,
            "n": 2.36,
            "electro_optic_coef":250e-12,
            "alpha": 0.,
            "c": -.1,
        },
    }
}

lattice_modulation_config = {
    "I": crystal_config["shared"]["Isat"]*16,
    "width": 700e-6,
    "center": (0,0),
    "exponent": 4.,
}