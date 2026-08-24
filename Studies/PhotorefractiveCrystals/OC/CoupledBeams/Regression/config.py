storage_config = {
    "home": "./Data/",
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
    "lz": 20e-3,
    "noise": .05,
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

beams_config = {
    "beam_1": {
        "envelope_config": {
            "I": 50.,
            "width": 600e-6,
            "center": (0, 0),
            "exponent": 4,
        },
        "landscape_config": {}
    },
    "beam_2": {
        "envelope_config": {
            "I": 50.,
            "width": 600e-6,
            "center": (0, 0),
            "exponent": 4,
        },
        "landscape_config": {
            # "f": tbf,  # float value
            "size": 200e-6,
            # "encoding": tbf,  # "amplitude" or "phase"
        }
    }
}