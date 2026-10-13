import numpy as np


class BogoliubovExcitations:
    def __init__(
        self,
        landscape_config,
        *args,
        **kwargs,
    ):
        self.excitation_percentage = landscape_config["excitation_percentage"]
        
        super().__init__(*args, **kwargs,)
        
    def landscape_function(
        self,
        mesh,
        seed = None,
        *args,
        **kwargs,
    ):
        if seed is not None:
            rng = np.random.default_rng(seed)
            excitations = rng.standard_normal(mesh.field_shape) * self.excitation_percentage
        else:
            excitations = np.random.randn(*mesh.field_shape) * self.excitation_percentage
        return 1. + excitations